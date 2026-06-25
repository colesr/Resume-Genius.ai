import os
import streamlit as st
import utils

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Resume Match Assistant",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- COLOR PALETTES ----------------
COLORS = {
    "bg_primary": "#fafafa",
    "bg_secondary": "#f5f5f5",
    "bg_tertiary": "#eeeeee",
    "text_primary": "#1a1a1a",
    "text_secondary": "#666666",
    "text_muted": "#999999",
    "accent_primary": "#2c3e50",
    "accent_secondary": "#34495e",
    "accent_tertiary": "#7f8c8d",
    "border_light": "#e0e0e0",
    "border_subtle": "#f0f0f0",
    "success": "#27ae60",
    "warning": "#f39c12",
    "error": "#e74c3c",
    "info": "#3498db",
}

DARK_COLORS = {
    "bg_primary": "#0f0f0f",
    "bg_secondary": "#1a1a1a",
    "bg_tertiary": "#242424",
    "text_primary": "#f5f5f5",
    "text_secondary": "#cccccc",
    "text_muted": "#888888",
    "accent_primary": "#ecf0f1",
    "accent_secondary": "#bdc3c7",
    "accent_tertiary": "#95a5a6",
    "border_light": "#333333",
    "border_subtle": "#262626",
    "success": "#2ecc71",
    "warning": "#f1c40f",
    "error": "#e74c3c",
    "info": "#3498db",
}

# Initialize session state
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

C = DARK_COLORS if st.session_state.dark_mode else COLORS

# ---------------- CUSTOM CSS ----------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

html, body, [data-testid="stAppViewContainer"] {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: {C['bg_primary']} !important;
    color: {C['text_primary']};
}}

.stApp {{
    background-color: {C['bg_primary']} !important;
}}

/* Hide default elements */
#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}
header {{background: transparent !important;}}

/* Sidebar */
section[data-testid="stSidebar"] {{
    background-color: {C['bg_secondary']} !important;
    border-right: 1px solid {C['border_light']} !important;
}}

/* Cards */
.glass-card {{
    background-color: {C['bg_secondary']};
    border: 1px solid {C['border_light']};
    border-radius: 8px;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
    transition: all 0.3s ease;
}}
.glass-card:hover {{
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
    border-color: {C['accent_tertiary']};
    transform: translateY(-2px);
}}

/* Title */
.main-title {{
    font-size: 2.2rem;
    font-weight: 700;
    text-align: center;
    color: {C['text_primary']};
    margin: 20px 0 8px 0;
    letter-spacing: -0.03em;
    font-family: 'Plus Jakarta Sans', sans-serif;
}}
.subtitle {{
    text-align: center;
    color: {C['text_secondary']};
    font-size: 0.95rem;
    margin-bottom: 40px;
}}

/* Buttons */
.stButton button {{
    width: 100%;
    height: 48px;
    border-radius: 6px;
    font-weight: 600;
    letter-spacing: 0.02em;
}}

/* Inputs */
.stTextArea textarea, .stTextInput input, .stSelectbox select {{
    background-color: {C['bg_secondary']} !important;
    color: {C['text_primary']} !important;
    border: 1px solid {C['border_light']} !important;
    border-radius: 6px !important;
}}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {{
    background-color: {C['bg_secondary']};
    padding: 4px;
    border-radius: 6px;
    border: 1px solid {C['border_light']};
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 4px !important;
}}

/* Gauge */
.gauge-container {{
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 140px;
    margin: 10px auto;
    animation: slideInUp 0.6s ease-out backwards;
}}

@keyframes slideInUp {{
    from {{ opacity: 0; transform: translateY(20px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

/* Other components */
.bullet-item, .keyword-badge, .optimizer-card, .copy-area {{
    transition: all 0.25s ease;
}}

.copy-area {{
    background-color: {C['bg_tertiary']};
    border: 1px solid {C['border_light']};
    border-radius: 8px;
    padding: 16px;
    font-family: 'Courier New', monospace;
    white-space: pre-wrap;
    max-height: 400px;
    overflow-y: auto;
}}
</style>
""", unsafe_allow_html=True)

# ---------------- HELPER FUNCTIONS ----------------
def draw_gauge(score, label, delay=0):
    radius = 35
    circumference = 2 * 3.14159 * radius
    stroke_offset = circumference - (circumference * (score / 100))
   
    return f"""
    <div class="gauge-container" style="animation-delay: {delay}s;">
        <svg width="110" height="110" viewBox="0 0 110 110" style="filter: drop-shadow(0 2px 4px rgba(0,0,0,0.08));">
            <circle cx="55" cy="55" r="{radius}" stroke="{C['border_light']}" stroke-width="5" fill="none"/>
            <defs>
                <linearGradient id="gauge-grad-{label.lower()}" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="{C['accent_primary']}"/>
                    <stop offset="100%" stop-color="{C['accent_secondary']}"/>
                </linearGradient>
            </defs>
            <circle cx="55" cy="55" r="{radius}"
                    stroke="url(#gauge-grad-{label.lower()})"
                    stroke-width="5" fill="none"
                    stroke-dasharray="{circumference}"
                    stroke-dashoffset="{stroke_offset}"
                    stroke-linecap="round"
                    style="transition: stroke-dashoffset 1.2s cubic-bezier(0.34, 1.56, 0.64, 1);"/>
        </svg>
        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center;">
            <div style="font-size: 24px; font-weight: 700; color: {C['text_primary']}; font-family: 'Plus Jakarta Sans';">
                {score}%
            </div>
            <div style="font-size: 10px; font-weight: 600; color: {C['text_muted']}; text-transform: uppercase; letter-spacing: 0.08em;">
                {label}
            </div>
        </div>
    </div>
    """

def make_bullet_list(items, is_positive=True):
    icon = "+" if is_positive else "-"
    color = C['success'] if is_positive else C['warning']
    html = ""
    for idx, item in enumerate(items):
        html += f"""
        <div class="bullet-item" style="display:flex; align-items:flex-start; gap:12px; margin-bottom:12px; padding:12px 16px; background:{C['bg_tertiary']}; border-left:3px solid {color}; border-radius:4px;">
            <div style="font-weight:700; color:{color};">{icon}</div>
            <div>{item}</div>
        </div>
        """
    return html

# (Add your other helper functions: make_keyword_badges, make_optimizer_card, etc. if needed)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown(f"""
    <div style='text-align: center; margin-bottom: 20px;'>
        <h2 style='color: {C["text_primary"]}; margin-bottom: 0;'>⚙️ Setup</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.session_state.dark_mode = st.toggle("Dark Mode", value=st.session_state.dark_mode)
    
    env_key = os.getenv("GROQ_API_KEY")
    if env_key:
        st.success("✅ Connected to Groq API")
    else:
        st.warning("⚠️ GROQ_API_KEY not found")

    st.markdown("---")
    st.markdown("### Target Role")
    target_role = st.text_input("Role", placeholder="e.g., Frontend Developer", label_visibility="collapsed")
    experience_level = st.selectbox("Experience Level", 
                                  ["Not specified", "Student / Fresher", "Entry level", "Mid level", "Senior level"], 
                                  label_visibility="collapsed")
    focus_area = st.selectbox("Focus Area", 
                            ["Overall match", "Missing keywords", "Resume wording", "Interview preparation"], 
                            label_visibility="collapsed")

# ---------------- HEADER ----------------
st.markdown(f"""
<div class='main-title'>📄 Resume Match Assistant</div>
<div class='subtitle'>
Analyze your resume against job descriptions and optimize your application
</div>
""", unsafe_allow_html=True)

# ---------------- INPUT SECTION ----------------
st.markdown("### Step 1: Upload Your Materials")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("**📄 Your Resume**")
    uploaded_file = st.file_uploader("Upload resume (.pdf, .docx, .txt)", 
                                   type=["pdf", "docx", "txt"], 
                                   label_visibility="collapsed")
    
    if uploaded_file:
        try:
            with st.spinner("Extracting..."):
                extracted = utils.parse_resume_file(uploaded_file)
                st.session_state.resume_text = extracted
            st.success(f"Loaded: {uploaded_file.name}")
        except Exception as e:
            st.error(f"Error: {e}")
    
    resume_input = st.text_area("Or paste resume text", 
                              value=st.session_state.resume_text, 
                              height=220, 
                              label_visibility="collapsed")

with col2:
    st.markdown("**💼 Job Description**")
    job_desc = st.text_area("Paste job description here", 
                          height=220, 
                          label_visibility="collapsed")

# ---------------- ANALYZE BUTTON ----------------
if st.button("🚀 Analyze & Optimize", type="primary", use_container_width=True):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("GROQ_API_KEY environment variable not set.")
    elif not st.session_state.resume_text.strip():
        st.error("Please provide your resume.")
    elif not job_desc.strip():
        st.error("Please provide a job description.")
    else:
        with st.spinner("Analyzing resume..."):
            try:
                analysis = utils.analyze_resume_ats(
                    resume_text=st.session_state.resume_text,
                    job_desc_text=job_desc,
                    api_key=api_key,
                    target_role=target_role,
                    experience_level=experience_level,
                    focus_area=focus_area
                )
                st.session_state.analysis_results = analysis
                st.success("Analysis complete!")
                st.rerun()
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")

# ---------------- RESULTS ----------------
if st.session_state.analysis_results:
    res = st.session_state.analysis_results
    # ... (rest of your results dashboard code - tabs, gauges, etc.)

    # Example gauge section:
    st.markdown("### Analysis Results")
    gauge_cols = st.columns(4)
    gauge_data = [
        (res.get("ats_score", 0), "ATS Score", 0.0),
        (res.get("match_percentage", 0), "Job Match", 0.1),
        (res.get("formatting_score", 0), "Format", 0.2),
        (res.get("keyword_score", 0), "Keywords", 0.3),
    ]
    
    for col, (score, label, delay) in zip(gauge_cols, gauge_data):
        with col:
            st.markdown(draw_gauge(score, label, delay), unsafe_allow_html=True)

    # Add the rest of your tabs (Overview, Keywords, etc.) here as before

st.caption("Resume Match Assistant • Built with Streamlit")