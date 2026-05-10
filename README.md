🚀 AI Resume Tailoring Agent
Overview
The AI Resume Tailoring Agent is a full-stack web application built with Streamlit and powered by Google's Gemini 1.5 Pro Large Language Model. It automates the tedious process of customizing a resume for specific job applications.

By taking a base resume (PDF) and a target Job Description (text), the AI rewrites the professional summary and experience bullet points to align perfectly with the target role's keywords and requirements. Finally, it uses WeasyPrint to instantly generate a beautifully formatted, single-page PDF ready for download.

Project Structure & File Explanations
This project requires three specific files to run properly, especially when deploying to the cloud.

1. app.py (The Core Engine)
This is the main application file. It contains:

The Frontend (Streamlit): Creates the web interface where users input their API key, upload their PDF, and paste the job description.

The Text Extractor (PyPDF2): Reads the uploaded base resume and converts the PDF into raw text so the AI can read it.

The AI Logic (Google Generative AI): Sends a highly engineered prompt to the Gemini model, instructing it to act as an expert recruiter. It forces the AI to output the rewritten resume strictly in JSON format.

The PDF Generator (WeasyPrint): Takes the AI-generated JSON data and injects it into a hard-coded, ATS-friendly HTML/CSS template. It then renders this HTML directly into a high-quality PDF.

2. requirements.txt (Python Dependencies)
This file tells the server which Python libraries need to be installed for app.py to run.

streamlit: For the web framework.

google-generativeai: To communicate with the Gemini AI.

PyPDF2: To read the uploaded PDF.

weasyprint: To convert HTML to PDF.

3. packages.txt (System Dependencies)
Crucial for Streamlit Cloud Deployment. WeasyPrint isn't just a Python library; it relies on underlying Linux system libraries to draw graphics and text (like Pango and Cairo). This file tells the Streamlit Cloud server to install these C-level libraries before running your Python code.

🛠️ How to Run Locally
If you want to test or modify the code on your own computer:

Extract the files into a single folder.

Open your terminal and navigate to that folder.

Install the requirements: ```bash
pip install -r requirements.txt

*(Note: Windows users may need to install GTK3 separately for WeasyPrint to work locally. Mac users can use `brew install pango libffi`).*
Run the application:

Bash
streamlit run app.py
The app will open automatically in your web browser at http://localhost:8501.

☁️ How to Deploy to Streamlit Cloud (Free)
To make this app accessible anywhere via a public URL:

Upload to GitHub: Create a new public repository on your GitHub account and upload the app.py, requirements.txt, and packages.txt files directly to the main branch.

Log into Streamlit: Go to share.streamlit.io and connect your GitHub account.

Deploy: Click "Create app" -> "Yes, I have an app".

Select your repository, ensure the Main file path is app.py, and click Deploy.

Wait a few minutes. Streamlit will read packages.txt to install the Linux rendering tools, then read requirements.txt to install Python tools, and finally launch your app!
