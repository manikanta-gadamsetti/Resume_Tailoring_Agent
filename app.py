import streamlit as st
import google.generativeai as genai
import PyPDF2
from weasyprint import HTML
import json
import base64
import os

st.set_page_config(page_title="Resume Tailoring Agent", layout="wide")
st.title("🚀 Manikanta's Custom Resume Tailor")
st.markdown("Upload your base resume, paste a Job Description, and get a tailored PDF.")

# --- SECURE API KEY CONFIGURATION ---
# The app will automatically look for the key in Streamlit's hidden secrets
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except KeyError:
    st.error("🚨 API Key not found! Please configure 'GEMINI_API_KEY' in your Streamlit Cloud Secrets.")
    st.stop()
# ------------------------------------

def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def tailor_resume_content(base_text, jd_text):
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    prompt = f"""
    You are an expert technical recruiter. I will provide my base resume and a Job Description.
    Rewrite my Summary, Experience bullets, and Project bullets to heavily align with the JD's keywords.
    DO NOT invent new experience. Reposition existing experience.

    Base Resume:
    {base_text}

    Job Description:
    {jd_text}

    Output valid JSON ONLY, matching this schema:
    {{
        "summary": "A 3-4 sentence professional summary tailored to the JD.",
        "innodata_bullets": ["bullet 1", "bullet 2", "bullet 3"],
        "maq_bullets": ["bullet 1", "bullet 2", "bullet 3"],
        "skills": "Comma-separated list of technical skills, prioritizing those found in the JD.",
        "medibot_bullets": ["bullet 1", "bullet 2", "bullet 3"],
        "cicd_bullets": ["bullet 1", "bullet 2", "bullet 3"]
    }}
    """
    try:
        response = model.generate_content(prompt)
        json_str = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(json_str)
    except Exception as e:
        st.error(f"Error communicating with AI: {e}")
        return None

def generate_v6_pdf(data):
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <style>
        @page {{ size: A4; margin: 10mm 15mm; background-color: #ffffff; }}
        body {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 9.5pt; line-height: 1.25; color: #000000; }}
        h1 {{ font-size: 18pt; margin: 0 0 4px 0; text-align: center; text-transform: uppercase; letter-spacing: 1px; font-weight: bold; }}
        .contact-info {{ text-align: center; font-size: 8.5pt; margin-bottom: 8px; }}
        h2 {{ font-size: 11pt; border-bottom: 1px solid #000000; padding-bottom: 2px; margin-top: 8px; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.5px; font-weight: bold; }}
        p {{ margin: 0 0 4px 0; text-align: justify; }}
        .job-header {{ margin-bottom: 2px; font-size: 9.5pt; }}
        .job-header .company {{ font-weight: bold; }}
        .job-header .date {{ float: right; font-style: italic; }}
        ul {{ margin-top: 0; margin-bottom: 6px; padding-left: 18px; }}
        li {{ margin-bottom: 2px; text-align: justify; }}
        .skills-list p {{ margin-bottom: 2px; }}
    </style>
    </head>
    <body>
        <h1>Manikanta Gadamsetti</h1>
        <div class="contact-info">
            Hyderabad, India | +91-7989265979 | mkmanikanta799@gmail.com<br>
            LinkedIn | GitHub | Portfolio
        </div>

        <h2>Professional Summary</h2>
        <p>{data.get('summary', '')}</p>

        <h2>Experience</h2>
        <div class="job-header">
            <span class="company">INNODATA PVT LIMITED</span> | AI Analyst, Noida, Uttar Pradesh
            <span class="date">Nov 2025 &ndash; Apr 2026</span>
        </div>
        <ul>
            {''.join([f"<li>{b}</li>" for b in data.get('innodata_bullets', [])])}
        </ul>

        <div class="job-header">
            <span class="company">MAQ SOFTWARE</span> | Associate Systems Engineer, Noida, Uttar Pradesh
            <span class="date">May 2025 &ndash; Aug 2025</span>
        </div>
        <ul>
            {''.join([f"<li>{b}</li>" for b in data.get('maq_bullets', [])])}
        </ul>

        <h2>Technical & Analytical Skills</h2>
        <div class="skills-list">
            <p><strong>Core Skills & Tools:</strong> {data.get('skills', '')}</p>
            <p><strong>Programming & Cloud:</strong> Python, Azure (Data Factory, Synapse), AWS.</p>
            <p><strong>Languages:</strong> English, Telugu, Hindi.</p>
        </div>

        <h2>Projects</h2>
        <div class="job-header">
            <span class="company">MediBot &ndash; AI Medical Diagnosis Chatbot</span>
            <span class="date">Jan 2026</span>
        </div>
        <ul>
            {''.join([f"<li>{b}</li>" for b in data.get('medibot_bullets', [])])}
        </ul>

        <div class="job-header">
            <span class="company">CI/CD Pipeline Automation</span>
            <span class="date">Aug 2025</span>
        </div>
        <ul>
            {''.join([f"<li>{b}</li>" for b in data.get('cicd_bullets', [])])}
        </ul>

        <h2>Certifications</h2>
        <ul>
            <li><strong>Microsoft:</strong> Azure Data Engineer Associate (DP-203), Security & Compliance (SC-900), Azure Fundamentals (AZ-900, DP-900)</li>
            <li><strong>Oracle:</strong> Multicloud Architect, OCI AI Foundations</li>
        </ul>

        <h2>Education</h2>
        <div class="job-header">
            <span class="company">B.Tech, CSE (Cloud Computing)</span> | Manav Rachna International Institute Of Research And Studies
            <span class="date">2025</span>
        </div>
        <div class="job-header">
            <span class="company">12th (Intermediate)</span> | Sasi Junior College (88%)
            <span class="date">2021</span>
        </div>
        <div class="job-header">
            <span class="company">10th</span> | Vignan Global Gen School (65%)
            <span class="date">2019</span>
        </div>
    </body>
    </html>
    """
    pdf_path = "Manikanta_Tailored_Resume.pdf"
    HTML(string=html).write_pdf(pdf_path)
    return pdf_path

col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("1. Upload Base Resume (PDF)", type=["pdf"])
with col2:
    job_desc = st.text_area("2. Paste Job Description Here", height=150)

if st.button("Generate Tailored Resume", type="primary"):
    if uploaded_file and job_desc:
        with st.spinner("AI is analyzing the JD and rewriting your resume..."):
            base_text = extract_text_from_pdf(uploaded_file)
            tailored_json = tailor_resume_content(base_text, job_desc)
            
            if tailored_json:
                pdf_file = generate_v6_pdf(tailored_json)
                
                with open(pdf_file, 'rb') as f:
                    pdf_bytes = f.read()
                
                st.success("Resume tailored successfully!")
                st.download_button(
                    label="⬇️ Download PDF Resume",
                    data=pdf_bytes,
                    file_name="Manikanta_Tailored_Resume.pdf",
                    mime="application/pdf",
                    type="primary"
                )
                st.balloons()
    else:
        st.warning("Please upload a resume and paste a job description.")
