from flask import Flask, request, jsonify
from pdf_utils import extract_text_from_pdf
from skill_extraction import extract_skills_spacy, bert_skill_match

app = Flask(__name__)

@app.route("/extract", methods=["POST"])
def extract():
    resume_pdf = request.files["resume"]
    jd_pdf = request.files["jd"]

    resume_text = extract_text_from_pdf(resume_pdf)
    jd_text = extract_text_from_pdf(jd_pdf)

    resume_skills = extract_skills_spacy(resume_text)
    jd_skills = extract_skills_spacy(jd_text)

    matched_skills = bert_skill_match(resume_skills, jd_skills)

    result = {
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "matched_skills": matched_skills,
        "total_skills": len(resume_skills),
        "matched_count": len(matched_skills),
        "match_percentage": int((len(matched_skills) / max(1, len(jd_skills))) * 100)
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
