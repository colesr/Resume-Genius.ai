# 🤖 AI ATS Analyzer

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![License](https://img.shields.io/badge/License-MIT-green)

An AI-powered resume screening tool that simulates an Applicant Tracking System (ATS)...
An AI-powered resume screening tool that simulates an **Applicant Tracking System (ATS)** using **LLMs** to analyze resumes against job descriptions and generate actionable feedback.

---

## 🚀 Live Demo
🔗 Hugging Face Deployment: https://huggingface.co/spaces/Advaith0911/resume

---

## 📌 Overview
Recruiters often use ATS software to filter resumes before humans even see them.

This project mimics that workflow by:
- Extracting text from resumes (PDF/DOCX)
- Comparing resumes with job descriptions
- Calculating ATS compatibility
- Generating AI-powered feedback
- Suggesting improvements for better shortlisting

In short:  
**Resume + Job Description → ATS Analysis → Score + Feedback**

---

## ✨ Features
✅ Resume upload support (**PDF / DOCX**)  
✅ Job description matching  
✅ ATS score generation  
✅ Skill gap detection  
✅ Resume improvement suggestions  
✅ AI-powered analysis using Groq LLM  
✅ Clean Streamlit UI  

---

## 🏗️ System Architecture

```text
Resume Upload
     ↓
Text Extraction (PDF/DOCX)
     ↓
Preprocessing
     ↓
Groq LLM Analysis
     ↓
ATS Score Generation
     ↓
Feedback & Suggestions
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|-----------|---------|
| Python | Core logic |
| Streamlit | Web UI |
| Groq API | LLM inference |
| PyPDF | PDF text extraction |
| python-docx | DOCX parsing |
| dotenv | Environment management |

---

## 📂 Project Structure

```bash
AI-ATS-Analyzer/
│
├── app.py          # Main Streamlit UI
├── utils.py        # Resume parsing & ATS logic
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 📷 Preview

<p align="center">
<img width="1920" height="1080" alt="Screenshot 2026-06-17 230543" src="https://github.com/user-attachments/assets/7a3c35a1-eb5a-437f-8f35-9a052d7413a4" />

</p>


---

## ⚙️ Installation

### 1. Clone Repository
```bash
git clone https://github.com/advaith-k-0911/AI-ATS-Analyzer.git
cd AI-ATS-Analyzer
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables
Create `.env`

```env
GROQ_API_KEY=your_api_key_here
```

### 4. Run App
```bash
streamlit run app.py
```

---

## 💡 Why This Project?
This project demonstrates practical applications of:
- Generative AI
- NLP
- Resume analysis
- LLM-powered decision support systems

It also showcases how AI can automate early-stage recruitment workflows.

---

## 🎯 Future Improvements
- Multi-resume comparison
- Resume ranking system
- Better UI animations
- Downloadable report (PDF)
- Recruiter dashboard

---

## 👨‍💻 Author
**Advaith K**  
BTech Cybersecurity Student 

GitHub: https://github.com/advaith-k-0911

---

## 📜 License

This project is licensed under the **MIT License**.

You are free to:
- ✅ Use
- ✅ Modify
- ✅ Distribute
- ✅ Use commercially

Just make sure to give proper credit to the original author.

Made with ☕, Python, and sleep deprivation by **Advaith K**
<3
