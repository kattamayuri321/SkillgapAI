from flask import Flask, jsonify
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

@app.route("/analyze", methods=["GET"])
def analyze():
    user_skills = ["Python", "SQL", "Machine Learning", "HTML"]
    job_skills  = ["Python", "Java", "SQL", "Deep Learning", "CSS"]

    similarity_matrix = [
        [0.9, 0.2, 0.8, 0.1, 0.1],
        [0.1, 0.3, 0.2, 0.1, 0.1],
        [0.2, 0.1, 0.85, 0.6, 0.2],
        [0.1, 0.1, 0.2, 0.1, 0.75]
    ]

    matched = []
    partial = []
    missing = []

    for j, job_skill in enumerate(job_skills):
        scores = [row[j] for row in similarity_matrix]
        max_score = max(scores)

        if max_score >= 0.75:
            matched.append(job_skill)
        elif max_score >= 0.4:
            partial.append(job_skill)
        else:
            missing.append(job_skill)

    total = len(job_skills)

    response = {
        "user_skills": user_skills,
        "job_skills": job_skills,
        "matrix": similarity_matrix,
        "matched": matched,
        "partial": partial,
        "missing": missing,
        "percentages": {
            "matched": round(len(matched) / total * 100),
            "partial": round(len(partial) / total * 100),
            "missing": round(len(missing) / total * 100)
        }
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
