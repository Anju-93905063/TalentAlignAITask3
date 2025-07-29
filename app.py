import streamlit as st
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import openai
import os

# Replace with your OpenAI API Key
openai.api_key ="Your open api key"

def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def get_openai_structured_data(text, label):
    prompt = f"""Extract the following information from this {label}:\n
    - Skills\n- Education\n- Work Experience\n- Other relevant points\n\n
    Return it in a readable bullet point format:\n\n{text}"""
    
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def clean_text_with_openai(text):
    prompt = f"Clean the following text by removing irrelevant details and summarizing meaningfully:\n\n{text}"
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def get_cosine_similarity(text1, text2):
    tfidf = TfidfVectorizer()
    vectors = tfidf.fit_transform([text1, text2])
    score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    boosted_score = score * 100 + 20
    return round(min(boosted_score, 100), 2)  # Cap at 100% 

def get_fit_reason(score, resume_structured, jd_structured):
    if score >= 70:
        fit = "✅ Strong Fit"
    elif score >= 60:
        fit = "⚠️ Partial Fit"
    else:
        fit = "❌ Not Fit"

    reason_prompt = f"""Compare the following RESUME and JOB DESCRIPTION and summarize in 2-3 lines why the candidate is a {fit} with score {score}%.
Mention relevant matching and missing points.

RESUME:
{resume_structured}

JOB DESCRIPTION:
{jd_structured}"""

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": reason_prompt}]
    )
    return fit, response.choices[0].message.content.strip()

# Streamlit UI
st.title("📄 Resume Matcher with JD using OpenAI + Cosine Similarity + TF-IDF")

st.markdown("### 🔽 Upload Resume")
resume_file = st.file_uploader("Upload your Resume (PDF)", type="pdf", key="resume")

st.markdown("### 🔽 Upload Job Description")
jd_file = st.file_uploader("Upload the Job Description (PDF)", type="pdf", key="jd")

if resume_file and jd_file:
    resume_raw = extract_text_from_pdf(resume_file)
    jd_raw = extract_text_from_pdf(jd_file)

    resume_cleaned = clean_text_with_openai(resume_raw)
    jd_cleaned = clean_text_with_openai(jd_raw)

    resume_structured = get_openai_structured_data(resume_raw, "resume")
    jd_structured = get_openai_structured_data(jd_raw, "job description")

    # Use structured summaries for comparison
    score = get_cosine_similarity(resume_structured, jd_structured)
    fit, reason = get_fit_reason(score, resume_structured, jd_structured)

    st.subheader("📊 Match Score using Cosine Similarity and TF-IDF Vectors")
    st.markdown(f"### **{score}% — {fit}**")
    st.markdown(f"📝 **Reason:** {reason}")

    with st.expander("📂 Resume - Raw Text"):
        st.text_area("Resume Raw Text", resume_raw, height=300)

    with st.expander("🧹 Resume - Cleaned Text"):
        st.text_area("Resume Cleaned Text", resume_cleaned, height=300)

    with st.expander("📑 Resume - Structured Info"):
        st.markdown(resume_structured)

    with st.expander("📂 JD - Raw Text"):
        st.text_area("JD Raw Text", jd_raw, height=300)

    with st.expander("🧹 JD - Cleaned Text"):
        st.text_area("JD Cleaned Text", jd_cleaned, height=300)

    with st.expander("📑 JD - Structured Info"):
        st.markdown(jd_structured)

else:
    st.warning("Please upload both Resume and Job Description PDFs.")
