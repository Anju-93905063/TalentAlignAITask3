📄 Resume Matcher using OpenAI + TF-IDF + Cosine Similarity
This Streamlit application helps match a candidate's resume with a job description (JD) using a combination of OpenAI's GPT-3.5, TF-IDF vectorization, and cosine similarity. It gives a smart match score and insights to determine how suitable a resume is for a given job.


🚀 Features
🔽 Upload Resume and Job Description PDFs

📄 Extracts raw text using PyPDF2

🧹 Cleans and summarizes text using OpenAI

🧠 Extracts structured info:

Skills

Education

Work Experience

📊 Calculates match score using TF-IDF and cosine similarity

💡 Generates explanation and fit status (✅ Strong Fit, ⚠️ Partial Fit, ❌ Not Fit)

🛠️ Tech Stack
Python 3.8+

Streamlit – Web UI

PyPDF2 – PDF text extraction

scikit-learn – TF-IDF & similarity scoring

OpenAI GPT-3.5 – Intelligent content extraction and summarization

📦 Installation & Running
1. 🔐 Set Your OpenAI API Key
In app.py, replace the placeholder with your key:


openai.api_key = "your-openai-api-key"
You can also use environment variables:


export OPENAI_API_KEY="your-openai-api-key"
And update app.py:


openai.api_key = os.getenv("OPENAI_API_KEY")
2. ✅ Install Dependencies

pip install -r requirements.txt
3. ▶️ Run the Streamlit App

streamlit run app.py
