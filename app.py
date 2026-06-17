import os
import json
import textwrap
import streamlit as st
import utils
# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="AI ATS Resume Analyzer Pro",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ---------------- CUSTOM CSS ----------------
# Standard styles to construct a premium Glassmorphic dark mode application
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
/* Main App styling */
html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', sans-serif;
    color: #f1f5f9;
}
.stApp {
    background: transparent !important;
    background-size: 200% 200%;
}
[data-testid="stAppViewContainer"],
section[data-testid="stSidebar"],
header,
[data-testid="stToolbar"] {
    position: relative;
    z-index: 2;
}
/* Sidebar Custom Styling */
section[data-testid="stSidebar"] {
    background-color: rgba(9, 13, 22, 0.6) !important;
    backdrop-filter: blur(15px) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
}
section[data-testid="stSidebar"] div[role="radiogroup"] {
    gap: 8px;
}
/* Glassmorphic Container Card */
.glass-card {
    background: rgba(255, 255, 255, 0.03);
    border-radius: 20px;
    padding: 24px;
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
    margin-bottom: 24px;
}
.glass-card-header {
    font-size: 1.25rem;
    font-weight: 700;
    color: #f8fafc;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 10px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    padding-bottom: 12px;
}
/* Main title styling */
.main-title {
    font-size: 2.75rem;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-top: 10px;
    margin-bottom: 5px;
    letter-spacing: -0.02em;
}
.subtitle {
    text-align: center;
    color: #94a3b8;
    font-size: 1.1rem;
    margin-bottom: 35px;
    font-weight: 400;
}
/* Buttons */
.stButton button {
    width: 100%;
    height: 52px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.1) !important;
    font-size: 16px;
    font-weight: 600;
    color: white !important;
    background: linear-gradient(90deg, #3b82f6, #6366f1, #8b5cf6) !important;
    background-size: 200% auto;
    transition: all 0.4s ease;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.25);
}
.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(99, 102, 241, 0.45);
    background-position: right center;
    border-color: rgba(255,255,255,0.2) !important;
}
.stButton button:active {
    transform: translateY(1px);
}
/* Text Areas and Inputs */
.stTextArea textarea, .stTextInput input {
    background-color: rgba(255, 255, 255, 0.03) !important;
    color: #f1f5f9 !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    transition: all 0.3s ease !important;
    font-size: 14px !important;
    line-height: 1.6 !important;
    padding: 14px !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 15px rgba(99, 102, 241, 0.25) !important;
    background-color: rgba(255, 255, 255, 0.05) !important;
}
/* Tab styling override for high-end look */
.stTabs [data-baseweb="tab-list"] {
    gap: 12px;
    background-color: rgba(255, 255, 255, 0.02) !important;
    padding: 6px;
    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.06);
    margin-bottom: 24px;
}
.stTabs [data-baseweb="tab"] {
    height: 46px;
    white-space: pre;
    background-color: transparent !important;
    border-radius: 10px !important;
    color: #94a3b8 !important;
    border: 1px solid transparent !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    padding: 0 20px !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: #f8fafc !important;
    background-color: rgba(255, 255, 255, 0.04) !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, rgba(59, 130, 246, 0.15), rgba(99, 102, 241, 0.15)) !important;
    color: #818cf8 !important;
    border: 1px solid rgba(99, 102, 241, 0.25) !important;
}
/* File Uploader styling */
[data-testid="stFileUploader"] {
    background: rgba(255, 255, 255, 0.02);
    border: 1px dashed rgba(255, 255, 255, 0.12);
    border-radius: 16px;
    padding: 20px;
    transition: all 0.3s ease;
}
[data-testid="stFileUploader"]:hover {
    border-color: #6366f1;
    background: rgba(255, 255, 255, 0.04);
}
/* Hiding default Streamlit footers and menus for clean look */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {background: transparent !important;}
/* Expander custom look */
.stList {
    background: rgba(255, 255, 255, 0.02) !important;
    border-radius: 12px;
}
.stAlert {
    background-color: rgba(255, 255, 255, 0.02) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 14px !important;
    color: #cbd5e1 !important;
}
/* Copy box */
.copy-area {
    background: rgba(0, 0, 0, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 16px;
    font-family: 'Courier New', Courier, monospace;
    font-size: 13.5px;
    color: #e2e8f0;
    max-height: 400px;
    overflow-y: auto;
    white-space: pre-wrap;
    line-height: 1.5;
}
</style>
""", unsafe_allow_html=True)
# ---------------- HELPER UI FUNCTIONS ----------------
def draw_gauge(score, label, color1, color2):
    """Generates a beautiful SVG gauge with custom gradient colors."""
    gradient_id = f"grad-{label.lower().replace(' ', '-')}"
    stroke_offset = 251 - int(251 * (score / 100))
    return textwrap.dedent(f"""
    <div style="position: relative; display: flex; flex-direction: column; align-items: center; justify-content: center; width: 130px; margin: 10px auto;">
        <svg width="110" height="110" viewBox="0 0 100 100" style="transform: rotate(-90deg);">
            <defs>
                <linearGradient id="{gradient_id}" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="{color1}" />
                    <stop offset="100%" stop-color="{color2}" />
                </linearGradient>
            </defs>
            <!-- Background circle -->
            <circle cx="50" cy="50" r="40" stroke="rgba(255,255,255,0.03)" stroke-width="7" fill="none" />
            <!-- Progress circle -->
            <circle cx="50" cy="50" r="40" stroke="url(#{gradient_id})" stroke-width="7" fill="none"
                    stroke-dasharray="251" stroke-dashoffset="{stroke_offset}"
                    stroke-linecap="round" style="transition: stroke-dashoffset 1s ease-in-out;" />
        </svg>
        <div style="position: absolute; top: 32px; left: 0; right: 0; text-align: center; font-size: 18px; font-weight: 800; color: #f8fafc; font-family: 'Inter', sans-serif;">
            {score}%
        </div>
        <div style="margin-top: 10px; font-size: 11px; font-weight: 700; color: #94a3b8; font-family: 'Inter', sans-serif; text-align: center; text-transform: uppercase; letter-spacing: 0.08em;">
            {label}
        </div>
    </div>
    """).strip()
def make_bullet_list(items, is_positive=True):
    """Renders checklist/caution list cards for dashboard."""
    icon = "✓" if is_positive else "⚠"
    color = "#10b981" if is_positive else "#f59e0b"
    bg_color = "rgba(16, 185, 129, 0.04)" if is_positive else "rgba(245, 158, 11, 0.04)"
    border_color = "rgba(16, 185, 129, 0.12)" if is_positive else "rgba(245, 158, 11, 0.12)"
    
    html = ""
    for item in items:
        html += (
            f'<div style="display: flex; align-items: flex-start; gap: 12px; margin-bottom: 12px; padding: 12px 16px; background: {bg_color}; border: 1px solid {border_color}; border-radius: 12px;">'
            f'<div style="color: {color}; font-weight: bold; font-size: 15px; margin-top: 1px; line-height: 1;">{icon}</div>'
            f'<div style="color: #cbd5e1; font-size: 13.5px; font-family: Inter, sans-serif; line-height: 1.5; font-weight: 400;">{item}</div>'
            '</div>'
        )
    return html
def make_keyword_badges(keywords):
    """Renders structured tag grid for keywords."""
    html = '<div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; margin-bottom: 15px;">'
    for kw_data in keywords:
        kw = kw_data.get("keyword", "")
        status = kw_data.get("status", "Present")
        importance = kw_data.get("importance", "Medium")
        
        if status == "Present":
            bg = "rgba(16, 185, 129, 0.06)"
            border = "1px solid rgba(16, 185, 129, 0.2)"
            color = "#34d399"
            icon = "✓"
        else:
            bg = "rgba(239, 68, 68, 0.06)"
            border = "1px dashed rgba(239, 68, 68, 0.25)"
            color = "#f87171"
            icon = "✗"
            
        imp_badge = f'<span style="font-size: 8px; font-weight: 700; opacity: 0.7; margin-left: 6px; padding: 2px 5px; background: rgba(255,255,255,0.08); border-radius: 4px; text-transform: uppercase;">{importance}</span>'
        
        html += (
            f'<div style="display: inline-flex; align-items: center; padding: 6px 14px; background: {bg}; border: {border}; border-radius: 20px; font-size: 12.5px; color: {color}; font-family: Inter, sans-serif; font-weight: 500;">'
            f'<span style="margin-right: 6px; font-weight: bold; font-size: 11px;">{icon}</span> {kw} {imp_badge}'
            '</div>'
        )
    html += '</div>'
    return html
def make_optimizer_card(original, optimized, rationale):
    """Renders side-by-side comparison optimization card."""
    return (
        '<div style="background: rgba(255, 255, 255, 0.01); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 16px; padding: 20px; margin-bottom: 16px; backdrop-filter: blur(10px);">'
        '<div style="display: flex; flex-direction: column; gap: 12px;">'
        '<div>'
        '<span style="font-size: 10px; font-weight: 700; text-transform: uppercase; color: #f87171; background: rgba(239, 68, 68, 0.08); padding: 3px 8px; border-radius: 6px; letter-spacing: 0.05em;">Original Resume Phrase</span>'
        f'<p style="color: #94a3b8; font-size: 13.5px; margin-top: 6px; line-height: 1.5; font-family: Inter, sans-serif;">{original}</p>'
        '</div>'
        '<div style="border-top: 1px solid rgba(255,255,255,0.04); padding-top: 12px;">'
        '<span style="font-size: 10px; font-weight: 700; text-transform: uppercase; color: #34d399; background: rgba(16, 185, 129, 0.08); padding: 3px 8px; border-radius: 6px; letter-spacing: 0.05em;">AI-Optimized Version</span>'
        f'<p style="color: #f8fafc; font-size: 13.5px; font-weight: 500; margin-top: 6px; line-height: 1.5; font-family: Inter, sans-serif; border-left: 3px solid #6366f1; padding-left: 10px;">{optimized}</p>'
        '</div>'
        '<div style="background: rgba(255, 255, 255, 0.02); padding: 10px 14px; border-radius: 8px; font-size: 12px; color: #64748b; font-family: Inter, sans-serif;">'
        f'<span style="font-weight: 600; color: #94a3b8;">ATS Reason:</span> {rationale}'
        '</div>'
        '</div>'
        '</div>'
    )
# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("<div style='text-align: center; margin-bottom: 20px;'><h2 style='color: white; margin-bottom: 0;'>⚙️ Control Center</h2><span style='color: #64748b; font-size: 12px;'>ATS Optimizer Pro</span></div>", unsafe_allow_html=True)
    
    # API Key Configuration
    st.markdown("### 🔑 API Authentication")
    env_key = os.getenv("GROQ_API_KEY")
    
    if env_key:
        st.success("API Key loaded from Environment")
        api_key = env_key
    else:
        api_key = st.text_input("Enter Groq API Key", type="password", help="You can get a free API key from console.groq.com")
        if not api_key:
            st.warning("Please enter API Key to proceed")
            
    st.markdown("---")
    
    # Model Selection
    st.markdown("### 🧠 LLM Tuning")
    target_role = st.text_input("Target Job Title (Optional)", placeholder="e.g. Senior Frontend Engineer", help="Providing this optimizes tailoring filters.")
    model_choice = st.selectbox("Inference Model", ["llama-3.3-70b-versatile", "llama3-70b-8192"], index=0)
    temperature = st.slider("Temperature", 0.0, 1.0, 0.2, 0.05, help="Lower values yield more structured and consistent audits.")
    
    st.markdown("---")
    st.markdown("""
    <div style="color: #64748b; font-size: 12px; line-height: 1.5;">
        <strong>How it works:</strong><br>
        1. Upload your Resume (PDF/Word/Text).<br>
        2. Paste the target Job Description.<br>
        3. The AI reviews ATS compatibility, calculates scores, identifies missing keywords, and optimizes your wording.
    </div>
    """, unsafe_allow_html=True)
# ---------------- HEADER ----------------
st.markdown("""
<div class='main-title'>🤖 AI ATS Resume Analyzer Pro</div>
<div class='subtitle'>
Audit Resume Compliance • Map Critical Keywords • Tailor Application Material
</div>
""", unsafe_allow_html=True)
# Initialize Session State for analysis results
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
# ---------------- INPUT CARD ----------------
col1, col2 = st.columns([1, 1], gap="large")
with col1:
    st.markdown("""
    <div class="glass-card-header">
        <span>📄 Resume Repository</span>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload your resume (.pdf, .docx, .txt)", type=["pdf", "docx", "txt"])
    
    if uploaded_file is not None:
        try:
            with st.spinner("Extracting content from file..."):
                extracted_text = utils.parse_resume_file(uploaded_file)
                st.session_state.resume_text = extracted_text
            st.success(f"Successfully loaded {uploaded_file.name} ({len(extracted_text)} characters)")
        except Exception as e:
            st.error(f"Error parsing resume: {str(e)}")
            
    # Allow fallback paste text area
    resume_input = st.text_area("Or paste Resume content manually", value=st.session_state.resume_text, height=220, placeholder="Paste plain text here...")
    if resume_input != st.session_state.resume_text:
        st.session_state.resume_text = resume_input
with col2:
    st.markdown("""
    <div class="glass-card-header">
        <span>💼 Target Job Specification</span>
    </div>
    """, unsafe_allow_html=True)
    
    job_desc = st.text_area("Paste the job description you are applying for", height=325, placeholder="Paste job description requirements, qualifications, and core duties here...")
# ---------------- ANALYZE TRIGGER ----------------
st.markdown("<div style='margin-top: 10px; margin-bottom: 30px;'>", unsafe_allow_html=True)
trigger_cols = st.columns([1, 2, 1])
with trigger_cols[1]:
    analyze_btn = st.button("🚀 Analyze & Optimize Resume")
st.markdown("</div>", unsafe_allow_html=True)
if analyze_btn:
    if not api_key:
        st.error("Missing Authentication: Please provide a valid Groq API Key.")
    elif not st.session_state.resume_text.strip():
        st.error("Missing Input: Please upload or paste a Resume.")
    elif not job_desc.strip():
        st.error("Missing Input: Please paste the Job Description.")
    else:
        with st.spinner("Analyzing resume against criteria using Llama-3.3-70B..."):
            try:
                # Compile job description with additional role context if available
                full_jd = job_desc
                if target_role.strip():
                    full_jd = f"Target Role: {target_role}\n\nJob Description:\n{job_desc}"
                    
                analysis = utils.analyze_resume_ats(
                    resume_text=st.session_state.resume_text,
                    job_desc_text=full_jd,
                    api_key=api_key
                )
                st.session_state.analysis_results = analysis
                st.success("Analysis complete!")
            except Exception as e:
                st.error(f"Audit Failed: {str(e)}")
# ---------------- DASHBOARD & RESULTS DISPLAY ----------------
if st.session_state.analysis_results:
    res = st.session_state.analysis_results
    
    # 1. Main Dashboard Indicators
    st.markdown("""
    <div class="glass-card">
        <div class="glass-card-header">🚀 Compliance & Match Diagnostics</div>
        <div style="display: flex; flex-wrap: wrap; justify-content: space-around; width: 100%; margin: 10px 0;">
    """, unsafe_allow_html=True)
    
    # Layout circles side-by-side using Streamlit columns
    gauge_cols = st.columns(4)
    with gauge_cols[0]:
        st.markdown(draw_gauge(res.get("ats_score", 0), "ATS SCORE", "#3b82f6", "#8b5cf6"), unsafe_allow_html=True)
    with gauge_cols[1]:
        st.markdown(draw_gauge(res.get("match_percentage", 0), "JOB MATCH", "#10b981", "#059669"), unsafe_allow_html=True)
    with gauge_cols[2]:
        st.markdown(draw_gauge(res.get("formatting_score", 0), "FORMAT COMPLIANCE", "#f59e0b", "#d97706"), unsafe_allow_html=True)
    with gauge_cols[3]:
        st.markdown(draw_gauge(res.get("keyword_score", 0), "KEYWORD DENSITY", "#ec4899", "#db2777"), unsafe_allow_html=True)
        
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. Tabs for granular reports
    tab_overview, tab_keywords, tab_optimization, tab_cover_letter, tab_interview = st.tabs([
        "📈 Executive Summary", 
        "🔍 Keyword & Skills Audit", 
        "🛠️ Bullet Optimizer", 
        "✉️ Cover Letter Builder", 
        "🗣️ Mock Interview Prep"
    ])
    
    # --- TAB 1: EXECUTIVE SUMMARY ---
    with tab_overview:
        col_sum, col_list = st.columns([1, 1.1], gap="large")
        
        with col_sum:
            st.markdown("### 📊 Fit Assessment")
            st.markdown(textwrap.dedent(f"""
            <div style="background: rgba(255,255,255,0.01); border: 1px solid rgba(255,255,255,0.05); border-radius: 16px; padding: 20px; line-height: 1.7; color: #cbd5e1; font-size: 14.5px;">
                {res.get('analysis_summary', 'No summary provided.')}
            </div>
            """).strip(), unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### ⚙️ ATS Parsing Checks")
            checks_html = ""
            for check in res.get("ats_compatibility_checks", []):
                chk_name = check.get("check", "")
                chk_status = check.get("status", "Passed")
                chk_feedback = check.get("feedback", "")
                
                status_color = "#34d399" if chk_status == "Passed" else ("#fbbf24" if chk_status == "Warning" else "#f87171")
                status_symbol = "●"
                
                checks_html += f"""
<div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.03); padding: 10px 0;">
    <div>
        <div style="font-size: 13.5px; font-weight: 600; color: #f8fafc;">{chk_name}</div>
        <div style="font-size: 12px; color: #94a3b8;">{chk_feedback}</div>
    </div>
    <div style="color: {status_color}; font-weight: bold; font-size: 13px; display: flex; align-items: center; gap: 6px;">
        <span>{status_symbol}</span>
        <span style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em;">{chk_status}</span>
    </div>
</div>
"""
            st.markdown(
                f"""
<div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 20px;">
{checks_html}
</div>
""",
                unsafe_allow_html=True
            )
            
        with col_list:
            st.markdown("### 🟢 Core Alignments")
            st.markdown(make_bullet_list(res.get("key_strengths", []), is_positive=True), unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 🟡 Critical Action Items")
            st.markdown(make_bullet_list(res.get("critical_issues", []), is_positive=False), unsafe_allow_html=True)
    # --- TAB 2: KEYWORD & SKILLS AUDIT ---
    with tab_keywords:
        st.markdown("### 🏷️ Job Description Keyword Matrix")
        st.markdown("Below is a breakdown of critical skills and terms found in the job description, mapped against your resume's vocabulary.")
        
        keywords_list = res.get("keyword_analysis", [])
        present_kws = [k for k in keywords_list if k.get("status") == "Present"]
        missing_kws = [k for k in keywords_list if k.get("status") != "Present"]
        
        col_pres, col_miss = st.columns(2)
        
        with col_pres:
            st.markdown(f"#### 🟢 Present Keywords ({len(present_kws)})")
            if present_kws:
                st.markdown(make_keyword_badges(present_kws), unsafe_allow_html=True)
            else:
                st.info("No matching keywords identified.")
                
        with col_miss:
            st.markdown(f"#### 🔴 Missing Keywords ({len(missing_kws)})")
            if missing_kws:
                st.markdown(make_keyword_badges(missing_kws), unsafe_allow_html=True)
            else:
                st.success("Excellent! All critical job keywords are present in your resume.")
                
        st.markdown("---")
        st.markdown("### 🕳️ Core Competency & Skills Gaps")
        
        gaps = res.get("skills_gap", [])
        if gaps:
            for gap in gaps:
                skill_name = gap.get("skill", "")
                category = gap.get("category", "Skill")
                desc = gap.get("gap_description", "")
                
                st.markdown(textwrap.dedent(f"""
                <div style="background: rgba(239, 68, 68, 0.02); border: 1px solid rgba(239, 68, 68, 0.12); border-radius: 12px; padding: 16px; margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span style="font-weight: 700; color: #ef4444; font-size: 14.5px;">{skill_name}</span>
                        <span style="font-size: 10px; font-weight: 700; text-transform: uppercase; color: #f8fafc; background: rgba(255,255,255,0.06); padding: 3px 8px; border-radius: 6px; letter-spacing: 0.05em;">{category}</span>
                    </div>
                    <div style="color: #cbd5e1; font-size: 13px; line-height: 1.5;">{desc}</div>
                </div>
                """).strip(), unsafe_allow_html=True)
        else:
            st.success("No structural skills gaps identified.")
    # --- TAB 3: BULLET OPTIMIZER ---
    with tab_optimization:
        st.markdown("### 🛠️ ATS Keyword Injection & Phrasing Optimization")
        st.markdown("Replace weak phrasing with high-impact, quantified accomplishments tailored to the job description requirements.")
        
        snippets = res.get("optimized_resume_snippets", [])
        if snippets:
            for snip in snippets:
                orig = snip.get("original", "")
                opt = snip.get("optimized", "")
                rat = snip.get("rationale", "")
                st.markdown(make_optimizer_card(orig, opt, rat), unsafe_allow_html=True)
        else:
            st.info("No phrasing optimizations suggested. Your bullet points look solid!")
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 💡 Formatting & Content Improvement Guidelines")
        st.markdown("Apply these general improvements to increase layout scanners reading accuracy:")
        for advice in res.get("improvement_suggestions", []):
            st.markdown(textwrap.dedent(f"""
            <div style="display: flex; gap: 10px; margin-bottom: 10px; font-size: 13.5px; color: #cbd5e1;">
                <span style="color: #6366f1;">•</span>
                <span>{advice}</span>
            </div>
            """).strip(), unsafe_allow_html=True)
    # --- TAB 4: COVER LETTER BUILDER ---
    with tab_cover_letter:
        st.markdown("### ✉️ Tailored Cover Letter")
        st.markdown("A highly customized cover letter generated to bridge your resume's highlights with the role's primary goals.")
        
        cl_text = res.get("cover_letter", "")
        if cl_text:
            st.markdown(f'<div class="copy-area">{cl_text}</div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            col_cl1, col_cl2 = st.columns([1, 1])
            with col_cl1:
                # Text download option
                st.download_button(
                    label="💾 Download Cover Letter (.txt)",
                    data=cl_text,
                    file_name="tailored_cover_letter.txt",
                    mime="text/plain"
                )
            with col_cl2:
                st.info("💡 Highlight and copy the text directly from the container above to paste into your word processor.")
        else:
            st.info("No cover letter generated.")
    # --- TAB 5: MOCK INTERVIEW PREP ---
    with tab_interview:
        st.markdown("### 🗣️ Custom Mock Interview Questions")
        st.markdown("Based on identified qualifications gaps between your experience and requirements, prepare answers for these challenging interview prompts.")
        
        questions = res.get("interview_questions", [])
        if questions:
            for idx, q_item in enumerate(questions):
                q = q_item.get("question", "")
                rationale = q_item.get("rationale", "")
                
                with st.expander(f"❓ Question {idx+1}: {q[:100]}..."):
                    st.markdown(textwrap.dedent(f"""
                    <div style="padding: 10px 0;">
                        <p style="font-size: 14.5px; font-weight: 600; color: #f8fafc; margin-bottom: 8px;">{q}</p>
                        <div style="background: rgba(99, 102, 241, 0.04); border: 1px solid rgba(99, 102, 241, 0.12); padding: 15px; border-radius: 12px; margin-top: 10px;">
                            <span style="font-size: 10.5px; font-weight: 700; text-transform: uppercase; color: #818cf8; display: block; margin-bottom: 4px;">Why they are asking:</span>
                            <span style="font-size: 13px; color: #cbd5e1; line-height: 1.5;">{rationale}</span>
                        </div>
                    </div>
                    """).strip(), unsafe_allow_html=True)
        else:
            st.info("No tailored interview questions generated.")
# ---------------- AURORA + MOUSE-REACTIVE BACKGROUND INJECTION ----------------
# We append ambient layers to the parent DOM so the background stays behind Streamlit widgets.
# It runs an animated aurora, a soft cursor light, and floating mouse-reactive particles.
# We wrap it in a try-catch block to run safely if CORS blocks parent context.
st.components.v1.html(
    """
    <script>
    try {
        const parentDoc = window.parent.document;
        const parentWin = window.parent;

        if (parentWin.__atsBgCleanup) {
            parentWin.__atsBgCleanup();
        }
        if (parentWin.__antigravityLoop) {
            parentWin.cancelAnimationFrame(parentWin.__antigravityLoop);
            parentWin.__antigravityLoop = null;
        }
        ['ats-aurora-layer', 'ats-cursor-glow', 'antigravity-canvas'].forEach((id) => {
            const oldEl = parentDoc.getElementById(id);
            if (oldEl) oldEl.remove();
        });

        if (!parentDoc.getElementById('ats-aurora-style')) {
            const style = parentDoc.createElement('style');
            style.id = 'ats-aurora-style';
            style.textContent = `
                html, body {
                    background: #090d16 !important;
                }
                #ats-aurora-layer,
                #ats-cursor-glow,
                #antigravity-canvas {
                    position: fixed;
                    inset: 0;
                    pointer-events: none;
                }
                #ats-aurora-layer {
                    z-index: 0;
                    inset: -18vh -12vw;
                    background:
                        radial-gradient(ellipse at 18% 22%, rgba(56, 189, 248, 0.28), transparent 32%),
                        radial-gradient(ellipse at 78% 12%, rgba(192, 132, 252, 0.24), transparent 30%),
                        radial-gradient(ellipse at 65% 82%, rgba(20, 184, 166, 0.18), transparent 34%),
                        conic-gradient(from 210deg at 50% 46%, rgba(14, 165, 233, 0.0), rgba(99, 102, 241, 0.24), rgba(192, 132, 252, 0.22), rgba(45, 212, 191, 0.16), rgba(14, 165, 233, 0.0));
                    filter: blur(42px) saturate(1.35);
                    opacity: 0.86;
                    transform: translate3d(0, 0, 0) rotate(0deg) scale(1.04);
                    animation: atsAuroraDrift 18s ease-in-out infinite alternate;
                }
                #ats-aurora-layer::after {
                    content: "";
                    position: absolute;
                    inset: 10vh 8vw;
                    background:
                        linear-gradient(115deg, transparent 10%, rgba(125, 211, 252, 0.10) 36%, transparent 58%),
                        linear-gradient(55deg, transparent 16%, rgba(167, 139, 250, 0.12) 42%, transparent 70%);
                    filter: blur(18px);
                    opacity: 0.75;
                    animation: atsAuroraRibbon 12s ease-in-out infinite alternate;
                }
                #ats-cursor-glow {
                    z-index: 1;
                    width: 360px;
                    height: 360px;
                    left: 50%;
                    top: 50%;
                    inset: auto;
                    border-radius: 999px;
                    background: radial-gradient(circle, rgba(125, 211, 252, 0.26) 0%, rgba(129, 140, 248, 0.17) 28%, rgba(192, 132, 252, 0.08) 46%, transparent 68%);
                    filter: blur(3px);
                    mix-blend-mode: screen;
                    opacity: 0.55;
                    transform: translate3d(-50%, -50%, 0);
                    transition: opacity 240ms ease;
                    will-change: transform, opacity;
                }
                body.ats-mouse-idle #ats-cursor-glow {
                    opacity: 0.22;
                }
                #antigravity-canvas {
                    z-index: 1;
                    width: 100vw;
                    height: 100vh;
                    opacity: 0.82;
                    mix-blend-mode: screen;
                }
                [data-testid="stAppViewContainer"],
                section[data-testid="stSidebar"],
                header,
                [data-testid="stToolbar"] {
                    position: relative !important;
                    z-index: 2 !important;
                }
                @keyframes atsAuroraDrift {
                    0% {
                        transform: translate3d(-2vw, -1vh, 0) rotate(-3deg) scale(1.03);
                    }
                    50% {
                        transform: translate3d(2vw, 2vh, 0) rotate(3deg) scale(1.09);
                    }
                    100% {
                        transform: translate3d(4vw, -2vh, 0) rotate(-1deg) scale(1.05);
                    }
                }
                @keyframes atsAuroraRibbon {
                    0% {
                        transform: translate3d(-3vw, 1vh, 0) skewX(-8deg);
                        opacity: 0.48;
                    }
                    100% {
                        transform: translate3d(3vw, -2vh, 0) skewX(8deg);
                        opacity: 0.82;
                    }
                }
            `;
            parentDoc.head.appendChild(style);
        }

        const appRoot = parentDoc.querySelector('.stApp') || parentDoc.body;
        if (!parentDoc.getElementById('ats-aurora-layer')) {
            const aurora = parentDoc.createElement('div');
            aurora.id = 'ats-aurora-layer';
            appRoot.prepend(aurora);
        }
        if (!parentDoc.getElementById('ats-cursor-glow')) {
            const cursorGlow = parentDoc.createElement('div');
            cursorGlow.id = 'ats-cursor-glow';
            appRoot.appendChild(cursorGlow);
        }
        
        if (!parentDoc.getElementById('antigravity-canvas')) {
            const canvas = parentDoc.createElement('canvas');
            canvas.id = 'antigravity-canvas';
            canvas.style.position = 'fixed';
            canvas.style.top = '0';
            canvas.style.left = '0';
            canvas.style.width = '100vw';
            canvas.style.height = '100vh';
            canvas.style.zIndex = '1';
            canvas.style.pointerEvents = 'none';
            canvas.style.background = 'transparent';
            appRoot.appendChild(canvas);
            const ctx = canvas.getContext('2d');
            let width = canvas.width = parentWin.innerWidth;
            let height = canvas.height = parentWin.innerHeight;
            const mouse = { x: width / 2, y: height / 2, active: false };
            const smoothMouse = { x: width / 2, y: height / 2 };
            const cursorGlow = parentDoc.getElementById('ats-cursor-glow');
            let idleTimer = null;
            let animationActive = true;
            const cleanupCallbacks = [];
            const addParentListener = (eventName, handler) => {
                parentWin.addEventListener(eventName, handler);
                cleanupCallbacks.push(() => parentWin.removeEventListener(eventName, handler));
            };
            parentDoc.body.classList.add('ats-mouse-idle');
            const handleMouseMove = (e) => {
                mouse.x = e.clientX;
                mouse.y = e.clientY;
                mouse.active = true;
                parentDoc.body.classList.remove('ats-mouse-idle');
                if (idleTimer) {
                    parentWin.clearTimeout(idleTimer);
                }
                idleTimer = parentWin.setTimeout(() => {
                    parentDoc.body.classList.add('ats-mouse-idle');
                    mouse.active = false;
                }, 1200);
            };
            const handleMouseLeave = () => {
                mouse.active = false;
                parentDoc.body.classList.add('ats-mouse-idle');
            };
            const handleResize = () => {
                width = canvas.width = parentWin.innerWidth;
                height = canvas.height = parentWin.innerHeight;
            };
            addParentListener('mousemove', handleMouseMove);
            addParentListener('mouseleave', handleMouseLeave);
            addParentListener('resize', handleResize);
            const particles = [];
            const particleCount = 75;
            for (let i = 0; i < particleCount; i++) {
                particles.push({
                    x: Math.random() * width,
                    y: Math.random() * height,
                    radius: Math.random() * 2 + 0.5,
                    color: `rgba(99, 102, 241, ${Math.random() * 0.25 + 0.1})`, // soft indigo
                    vx: (Math.random() - 0.5) * 0.3,
                    vy: -(Math.random() * 0.5 + 0.15), // float upwards (anti-gravity)
                    baseVy: -(Math.random() * 0.5 + 0.15),
                    seed: Math.random() * 100
                });
            }
            function animate() {
                if (!animationActive) {
                    return;
                }
                smoothMouse.x += (mouse.x - smoothMouse.x) * 0.08;
                smoothMouse.y += (mouse.y - smoothMouse.y) * 0.08;
                if (cursorGlow) {
                    cursorGlow.style.left = `${smoothMouse.x}px`;
                    cursorGlow.style.top = `${smoothMouse.y}px`;
                }

                ctx.clearRect(0, 0, width, height);
                // Update and draw particles
                for (let i = 0; i < particles.length; i++) {
                    const p = particles[i];
                    p.y += p.vy;
                    p.x += p.vx + Math.sin(p.y * 0.005 + p.seed) * 0.15;
                    if (mouse.active) {
                        const dx = p.x - mouse.x;
                        const dy = p.y - mouse.y;
                        const dist = Math.sqrt(dx * dx + dy * dy);
                        const threshold = 170;
                        if (dist < threshold) {
                            const force = (threshold - dist) / threshold;
                            const angle = Math.atan2(dy, dx);
                            // Smooth push away (repulsive field)
                            p.vx += Math.cos(angle) * force * 0.55;
                            p.vy += Math.sin(angle) * force * 0.55;
                        }
                    }
                    p.vx *= 0.94;
                    p.vy = p.vy * 0.94 + p.baseVy * 0.06;
                    // Boundaries wrap around
                    if (p.y < -10) {
                        p.y = height + 10;
                        p.x = Math.random() * width;
                        p.vx = (Math.random() - 0.5) * 0.3;
                        p.vy = p.baseVy;
                    }
                    if (p.x < -10) p.x = width + 10;
                    if (p.x > width + 10) p.x = -10;
                    ctx.beginPath();
                    ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
                    ctx.fillStyle = p.color;
                    ctx.fill();
                }
                // Connect adjacent particles with subtle lines
                for (let i = 0; i < particles.length; i++) {
                    for (let j = i + 1; j < particles.length; j++) {
                        const p1 = particles[i];
                        const p2 = particles[j];
                        const dx = p1.x - p2.x;
                        const dy = p1.y - p2.y;
                        const dist = Math.sqrt(dx * dx + dy * dy);
                        if (dist < 100) {
                            ctx.beginPath();
                            ctx.moveTo(p1.x, p1.y);
                            ctx.lineTo(p2.x, p2.y);
                            const alpha = (100 - dist) / 100 * 0.08;
                            ctx.strokeStyle = `rgba(56, 189, 248, ${alpha})`; // soft sky blue lines
                            ctx.lineWidth = 0.5;
                            ctx.stroke();
                        }
                    }
                }
                parentWin.__antigravityLoop = parentWin.requestAnimationFrame(animate);
            }
            parentWin.__atsBgCleanup = () => {
                animationActive = false;
                cleanupCallbacks.forEach((cleanup) => cleanup());
                if (idleTimer) {
                    parentWin.clearTimeout(idleTimer);
                    idleTimer = null;
                }
                if (parentWin.__antigravityLoop) {
                    parentWin.cancelAnimationFrame(parentWin.__antigravityLoop);
                    parentWin.__antigravityLoop = null;
                }
                ['ats-aurora-layer', 'ats-cursor-glow', 'antigravity-canvas'].forEach((id) => {
                    const el = parentDoc.getElementById(id);
                    if (el) el.remove();
                });
            };
            if (!parentWin.__antigravityLoop) {
                animate();
            }
        }
    } catch (e) {
        console.warn("Could not inject custom background canvas on parent DOM: Same-origin sandbox restriction.", e);
    }
    </script>
    """,
    height=0,
    width=0
)
