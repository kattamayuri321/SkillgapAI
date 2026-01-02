import spacy
import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity

# Load models
nlp = spacy.load("en_core_web_sm")
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
bert = BertModel.from_pretrained("bert-base-uncased")

# Skill database
SKILL_DB = [
    "python", "java", "sql", "machine learning", "deep learning",
    "nlp", "data analysis", "excel", "communication",
    "problem solving", "teamwork", "flask", "django"
]

# spaCy-based extraction
def extract_skills_spacy(text):
    text = text.lower()
    skills = []
    for skill in SKILL_DB:
        if skill in text:
            skills.append(skill)
    return list(set(skills))

# BERT embedding
def get_embedding(text):
    tokens = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        output = bert(**tokens)
    return output.last_hidden_state.mean(dim=1)

# BERT semantic matching
def bert_skill_match(resume_skills, jd_skills, threshold=0.7):
    matched = []
    for r in resume_skills:
        r_emb = get_embedding(r)
        for j in jd_skills:
            j_emb = get_embedding(j)
            score = cosine_similarity(r_emb, j_emb)[0][0]
            if score >= threshold:
                matched.append(r)
    return list(set(matched))
