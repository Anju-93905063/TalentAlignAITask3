import fitz
import re

def extract_text(path):
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text.lower()

def extract_sections(text):
    # Basic keyword-based extraction (improveable with NLP later)
    skills = re.findall(r"(skills|technical skills|key skills)[\s:\-]*([\s\S]*?)(experience|education|projects|certifications)", text)
    experience = re.findall(r"(experience|work experience)[\s:\-]*([\s\S]*?)(education|skills|projects|certifications)", text)
    education = re.findall(r"(education|academic background)[\s:\-]*([\s\S]*?)(skills|experience|projects|certifications)", text)

    return {
        "skills": skills[0][1].strip() if skills else "Not Found",
        "experience": experience[0][1].strip() if experience else "Not Found",
        "education": education[0][1].strip() if education else "Not Found"
    }
