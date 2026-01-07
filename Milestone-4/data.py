import pandas as pd

def get_skill_data():
    data = {
        "Skill": ["Python", "Machine Learning", "TensorFlow", "SQL", "Statistics", "Communication", "AWS", "Project Mgmt"],
        "Resume": [92, 88, 75, 65, 78, 85, 30, 55],
        "Job": [95, 90, 85, 80, 85, 90, 75, 70]
    }
    return pd.DataFrame(data)

def get_summary():
    return {
        "overall_match": 72,
        "matched_skills": 6,
        "missing_skills": 4
    }

def get_recommendations():
    return [
        ("AWS Cloud Services", "Complete AWS Certified Solutions Architect course"),
        ("Advanced Statistics", "Enroll in Advanced Statistics for Data Science program"),
        ("Project Management", "Consider PMP certification for leadership skills")
    ]
