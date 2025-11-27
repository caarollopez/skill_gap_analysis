from collections import Counter
import pandas as pd

def compute_skill_gap(rows, user_skills):
    user_skills = set(user_skills)

    for row in rows:
        job_sk = set(row["skills_detected"])
        row["n_skills_job"] = len(job_sk)
        row["n_skills_user_has"] = len(job_sk & user_skills)
        row["match_ratio"] = (
            row["n_skills_user_has"] / row["n_skills_job"]
            if row["n_skills_job"] > 0 else 0
        )

    all_skills = []
    for row in rows:
        all_skills.extend(row["skills_detected"])

    freq = Counter(all_skills)

    missing = [
        {
            "skill": skill,
            "count": count,
            "priority": count
        }
        for skill, count in freq.most_common()
        if skill not in user_skills
    ]

    return rows, missing
