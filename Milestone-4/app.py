import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
from fpdf import FPDF
from data import get_skill_data, get_summary, get_recommendations

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Skill Gap Analysis Dashboard", layout="wide")

# ---------------- HEADER ----------------
st.markdown("""
<div style="background-color:#4e8df5;padding:20px;border-radius:10px">
<h2 style="color:white;">Milestone 4: Dashboard and Report Export Module (Weeks 7–8)</h2>
<p style="color:white;">
Dashboard and Report Export : Streamlit interface for end-to-end comparison · 
Interactive graphs and scores · Downloadable reports in PDF/CSV formats
</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------------- LOAD DATA ----------------
df = get_skill_data()
summary = get_summary()
recommendations = get_recommendations()

# ---------------- TOP BUTTONS ----------------
col1, col2, col3 = st.columns([6, 1, 1])
with col2:
    st.button("🔄 Refresh")
with col3:
    st.button("⚙ Settings")

# ---------------- MAIN LAYOUT ----------------
left, right = st.columns([2, 1])

# ================= LEFT SIDE =================
with left:
    st.subheader("Skill Match Overview")

    c1, c2, c3 = st.columns(3)
    c1.metric("Overall Match", f"{summary['overall_match']}%")
    c2.metric("Matched Skills", summary["matched_skills"])
    c3.metric("Missing Skills", summary["missing_skills"])

    # -------- BAR CHART (Resume vs Job) --------
    skills = df["Skill"]
    x = np.arange(len(skills))
    width = 0.35

    fig, ax = plt.subplots()
    ax.bar(x - width/2, df["Resume"], width, label="Resume Skills")
    ax.bar(x + width/2, df["Job"], width, label="Job Requirements")

    ax.set_ylabel("Match Percentage")
    ax.set_xlabel("Skills")
    ax.set_ylim(0, 100)
    ax.set_xticks(x)
    ax.set_xticklabels(skills, rotation=45)
    ax.legend()

    st.pyplot(fig)

    # -------- SKILL SCORE SUMMARY --------
    score_cols = st.columns(4)
    scores = [
        ("Python", 92, "green"),
        ("Machine Learning", 88, "green"),
        ("SQL", 65, "orange"),
        ("AWS", 30, "red")
    ]

    for i, (skill, val, color) in enumerate(scores):
        score_cols[i].markdown(
            f"<h3 style='color:{color}'>{val}%</h3><p>{skill}</p>",
            unsafe_allow_html=True
        )

    # -------- SKILL COMPARISON (TWO COLORS) --------
    st.subheader("Skill Comparison (Resume vs Job)")

    for _, row in df.iterrows():
        st.write(row["Skill"])

        col_r, col_j = st.columns(2)

        with col_r:
            st.caption("Resume")
            st.progress(int(row["Resume"]))

        with col_j:
            st.caption("Job Requirement")
            st.progress(int(row["Job"]))

# ================= RIGHT SIDE =================
with right:
    st.subheader("Role View")
    role = st.radio("", ["Job Seeker", "Recruiter"], horizontal=True)

    # -------- RADAR CHART (Resume vs Job) --------
    categories = [
        "Technical Skills",
        "Soft Skills",
        "Experience",
        "Education",
        "Certifications"
    ]

    resume_values = [85, 78, 70, 75, 65]
    job_values = [90, 85, 80, 80, 75]

    radar = go.Figure()

    radar.add_trace(go.Scatterpolar(
        r=resume_values + [resume_values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name='Resume Profile'
    ))

    radar.add_trace(go.Scatterpolar(
        r=job_values + [job_values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name='Job Requirements'
    ))

    radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True
    )

    st.plotly_chart(radar, use_container_width=True)

    # -------- UPSKILLING RECOMMENDATIONS --------
    st.subheader("Upskilling Recommendations")
    for title, desc in recommendations:
        st.markdown(f"**{title}**  \n{desc}")

# ---------------- DOWNLOAD SECTION ----------------
st.write("---")

# -------- CSV DOWNLOAD --------
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇ Download CSV Report",
    csv,
    "skill_gap_report.csv",
    "text/csv"
)

# -------- PDF DOWNLOAD --------
def generate_pdf(dataframe):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, "Skill Gap Analysis Report", ln=True)

    for _, row in dataframe.iterrows():
        pdf.cell(
            200, 8,
            f"{row['Skill']} - Resume: {row['Resume']}%, Job: {row['Job']}%",
            ln=True
        )

    return pdf.output(dest="S").encode("latin-1")

pdf_data = generate_pdf(df)

st.download_button(
    "⬇ Download PDF Report",
    pdf_data,
    "skill_gap_report.pdf",
    "application/pdf"
)
