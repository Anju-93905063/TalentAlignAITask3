import streamlit as st
from extractor import extract_text, extract_sections

st.set_page_config(page_title="TalentAlign AI - Structured Extractor", layout="wide")
st.title("📄 TalentAlign AI – Resume & JD Section Extractor")

col1, col2 = st.columns(2)

with col1:
    resume_file = st.file_uploader("📥 Upload Resume PDF", type="pdf", key="resume")
with col2:
    jd_file = st.file_uploader("📥 Upload Job Description PDF", type="pdf", key="jd")

if resume_file:
    with open("uploaded_resume.pdf", "wb") as f:
        f.write(resume_file.read())
    resume_text = extract_text("uploaded_resume.pdf")
    resume_struct = extract_sections(resume_text)

    st.subheader("📘 Resume Data")
    st.json(resume_struct)

if jd_file:
    with open("uploaded_jd.pdf", "wb") as f:
        f.write(jd_file.read())
    jd_text = extract_text("uploaded_jd.pdf")
    jd_struct = extract_sections(jd_text)

    st.subheader("📗 JD Data")
    st.json(jd_struct)
