import streamlit as st
import pandas as pd

from core.api_client import load_or_fetch_jobs
from core.skills_extraction import clean_html, extract_skills, skills_list
from core.analysis import compute_skill_gap

st.set_page_config(page_title="SkillGap", layout="wide")
st.title("SkillGap – Skill Match & Job Analysis")

st.sidebar.header("Job Search Parameters")

role = st.sidebar.text_input("Role", "data analyst")
location = st.sidebar.text_input("Location", "Madrid")
country = st.sidebar.text_input("Country code", "es")

date_posted = st.sidebar.selectbox("Posted date", ["all", "today", "3days", "week", "month"])
remote = st.sidebar.checkbox("Only remote?")
work_from_home = True if remote else None

radius = st.sidebar.number_input("Radius (km)", min_value=0.0, value=0.0)
radius_val = radius if radius > 0 else None

st.sidebar.header("Your Skills")
user_skills = st.sidebar.multiselect("Select your skills", options=skills_list)

if st.sidebar.button("Search"):
    with st.spinner("Fetching and analyzing..."):
        data = load_or_fetch_jobs(
            role, location, country,
            date_posted=date_posted,
            work_from_home=work_from_home,
            radius=radius_val
        )

        job_results = data.get("data", [])

        rows = []
        for job in job_results:
            desc = clean_html(job.get("job_description", ""))
            skills = extract_skills(desc)

            rows.append({
                "job_id": job.get("job_id"),
                "title": job.get("job_title"),
                "company": job.get("employer_name"),
                "city": job.get("job_city"),
                "skills_detected": skills,
            })

        rows, missing = compute_skill_gap(rows, user_skills)

        df = pd.DataFrame(rows).sort_values("match_ratio", ascending=False)
        st.subheader("Job Matches")
        st.dataframe(df)

        st.subheader("Top Missing Skills")
        if missing:
            st.table(pd.DataFrame(missing).head(10))
        else:
            st.success("You have all required skills for these jobs!")
