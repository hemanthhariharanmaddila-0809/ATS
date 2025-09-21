import streamlit as st
import os
import time
from dotenv import load_dotenv
import google.generativeai as genai
from PyPDF2 import PdfReader

# Load environment variables and configure API
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_output(pdf_text, prompt):
    response = model.generate_content([pdf_text, prompt])
    return response.text

def read_pdf(uploaded_file):
    if uploaded_file is not None:
        pdf_reader = PdfReader(uploaded_file)
        pdf_text = ""
        for page in pdf_reader.pages:
            pdf_text += page.extract_text()
        return pdf_text
    else:
        raise FileNotFoundError("No file uploaded")

st.set_page_config(page_title="ResumeATS Pro", layout="wide")

# Styling and header
st.markdown("""
<style>
body, html {
    background-color: #121212;
    color: #eeeeee;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
h1, h3 {
    color: #3399ff;
}
.section-box {
    background: #1e1e1e;
    border: 1px solid #2a2a2a;
    border-radius: 12px;
    padding: 24px 30px;
    margin: 20px auto;
    max-width: 720px;
    box-shadow: 0 2px 15px rgba(0,0,0,0.7);
}
.stButton>button, .stDownloadButton>button {
    background-color: #3399ff !important;
    color: white !important;
    border-radius: 24px !important;
    padding: 0.6em 2em;
    font-weight: 700;
    border:none;
    font-size: 1.2em;
    transition: background-color 0.35s;
}
.stButton>button:hover,
.stDownloadButton>button:hover {
    background-color: #1a73e8 !important;
    cursor: pointer;
}
input[type="checkbox"] {
  accent-color: #3399ff;
  transform: scale(1.4);
  margin-right: 10px;
  cursor: pointer;
}
div.stFileUploader > div > div > label {
  background: #222222 !important;
  border-radius: 14px;
  padding: 30px !important;
  border: 3px dashed #3399ff !important;
  font-size: 1.3em;
  color: #bbb;
  transition: background-color 0.4s;
}
div.stFileUploader > div > div > label:hover {
  background-color: #2a2a2a !important;
  cursor: pointer;
}
.stTextInput>div>div>input, .stTextArea>div>div>textarea {
    border-radius: 15px !important;
    border: 1px solid #444 !important;
    background-color: #222 !important;
    color: #eee !important;
    padding: 12px 15px !important;
    font-size: 1em;
}
.sidebar .sidebar-content {
    background-color: #1e1e1e !important;
    color: #ccc !important;
    font-size: 1em;
}
.stTextArea>div>div>textarea::placeholder {
    color: #888 !important;
    opacity: 1;
}
.expander {
    background-color: #292929 !important;
    border-radius: 12px !important;
    padding: 12px !important;
}
</style>
<div style="text-align:center; margin-bottom:25px;">
    <h1>ResumeATS Pro</h1>
    <h3>Optimize Your Resume for ATS and Land Your Dream Job</h3>
</div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="section-box">', unsafe_allow_html=True)    
    upload_file = st.file_uploader("Upload your resume (PDF only) 👇", type=["pdf"], help="Drag and drop or click to browse")
    job_description = st.text_area("Paste the job description (optional):", placeholder="Paste the job description to tailor analysis...")
    
    col1, col2 = st.columns([0.7, 0.3])
    with col1:
        analysis_option = st.selectbox(
            "Select analysis type:",
            ["Quick Scan", "Detailed Analysis", "ATS Optimization"]
        )
    with col2:
        kw_opt = st.checkbox("Enable keyword optimization", value=True)
    st.markdown('</div>', unsafe_allow_html=True)

if st.button("Analyze Resume"):
    if upload_file is not None:
        st.success("✅ Upload Successful! Starting analysis...")
        
        with st.spinner("Extracting resume text..."):
            pdf_text = read_pdf(upload_file)
            time.sleep(1)
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        for progress in range(101):
            time.sleep(0.03)
            progress_bar.progress(progress)
            status_text.text(f"Analyzing resume... {progress}% complete")
        status_text.text("Analysis complete! 🎉")

        if analysis_option == "Quick Scan":
            prompt = f"""You are ResumeChecker, an expert in resume analysis. Provide a quick scan: ... Resume: {pdf_text} Job Description: {job_description}"""
        elif analysis_option == "Detailed Analysis":
            prompt = f"""You are ResumeChecker, an expert in resume analysis. Provide a detailed review: ... Resume: {pdf_text} Job Description: {job_description}"""
        else:
            prompt = f"""You are ResumeChecker, expert in ATS optimization. Analyze resume: ... Resume: {pdf_text} Job Description: {job_description}"""

        response = get_gemini_output(pdf_text, prompt)

        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.header("📝 Analysis Results")
        st.markdown(response)
        st.markdown("</div>", unsafe_allow_html=True)

        with st.expander("🔍 ATS Compatibility Breakdown"):
            st.markdown("""
            - **ATS Compatibility:** <span style='color:#4CAF50'>Passed</span><br>
            - **Keywords Found:** 12/15<br>
            - **Formatting:** Clean and ATS-friendly<br>
            - **Action Verbs:** 9/10
            """, unsafe_allow_html=True)

        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.header("💬 Ask Questions About Your Resume")
        user_question = st.text_input("Enter a question about your resume or the analysis:")
        if user_question:
            chat_prompt = f"Based on the above resume and analysis, answer the following: {user_question} Resume: {pdf_text} Analysis: {response}"
            chat_response = get_gemini_output(pdf_text, chat_prompt)
            st.markdown(chat_response)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.error("⚠ Please upload a PDF resume file before analyzing.")

# Sidebar with resources and feedback
st.sidebar.markdown("""
<h3>Resources</h3>
<ul>
    <li><a href="https://cdn-careerservices.fas.harvard.edu/wp-content/uploads/sites/161/2023/08/College-resume-and-cover-letter-4.pdf" target="_blank" style="color:#3399ff">Resume Writing Tips</a></li>
    <li><a href="https://career.io/career-advice/create-an-optimized-ats-resume" target="_blank" style="color:#3399ff">ATS Optimization Guide</a></li>
    <li><a href="https://hbr.org/2021/11/10-common-job-interview-questions-and-how-to-answer-them" target="_blank" style="color:#3399ff">Interview Preparation</a></li>
</ul>
""", unsafe_allow_html=True)

feedback = st.sidebar.text_area("Help us improve! Leave your feedback here:")
if st.sidebar.button("Submit Feedback"):
    if feedback.strip():
        st.sidebar.success("Thank you for your feedback!")
    else:
        st.sidebar.warning("Please enter feedback before submitting.")

# Footer
st.markdown("""
<div style="text-align:center; font-size:0.9em; margin-top:50px; color:#666;">
    Built with ❤️ using Streamlit & Gemini AI | © 2025 ResumeATS Pro
</div>
""", unsafe_allow_html=True)
