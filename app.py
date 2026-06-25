import os
import json
import textwrap
import streamlit as st
import utils

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Resume Match Assistant",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- MINIMALIST COLOR PALETTE ----------------
# Elegant, refined color scheme with high contrast and minimal saturation
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

# Dark mode override (optional toggle in sidebar)
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

# Default to light mode
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

C = DARK_COLORS if st.session_state.dark_mode else COLORS

# ---------------- CUSTOM CSS - MINIMALIST DESIGN ----------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

/* Root styling */
html, body, [data-testid="stAppViewContainer"] {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    color: {C['text_primary']};
    background-color: {C['bg_primary']};
}}

.stApp {{
    background-color: {C['bg_primary']} !important;
}}

/* Hide default Streamlit elements */
#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}
header {{background: transparent !important;}}

/* ===== MINIMALIST SIDEBAR ===== */
section[data-testid="stSidebar"] {{
    background-color: {C['bg_secondary']} !important;
    border-right: 1px solid {C['border_light']} !important;
}}

/* ===== MINIMALIST CARDS ===== */
.glass-card {{
    background-color: {C['bg_secondary']};
    border: 1px solid {C['border_light']};
    border-radius: 8px;
    padding: 24px;
    margin-bottom: 24px;
    transition: all 0.3s ease;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}}

.glass-card:hover {{
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
    border-color: {C['accent_tertiary']};
    transform: translateY(-2px);
}}

.glass-card-header {{
    font-size: 1.1rem;
    font-weight: 600;
    color: {C['text_primary']};
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 12px;
    border-bottom: 1px solid {C['border_subtle']};
    padding-bottom: 12px;
    letter-spacing: -0.02em;
}}

/* ===== MINIMALIST TITLE ===== */
.main-title {{
    font-size: 2.2rem;
    font-weight: 700;
    text-align: center;
    color: {C['text_primary']};
    margin-top: 20px;
    margin-bottom: 8px;
    letter-spacing: -0.03em;
    font-family: 'Plus Jakarta Sans', sans-serif;
}}

.subtitle {{
    text-align: center;
    color: {C['text_secondary']};
    font-size: 0.95rem;
    margin-bottom: 40px;
    font-weight: 400;
    letter-spacing: -0.01em;
}}

/* ===== MINIMALIST BUTTONS ===== */
.stButton button {{
    width: 100%;
    height: 48px;
    border-radius: 6px;
    border: 1.5px solid {C['accent_primary']} !important;
    font-size: 15px;
    font-weight: 600;
    color: white !important;
    background-color: {C['accent_primary']} !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
    cursor: pointer;
    letter-spacing: 0.02em;
}}

.stButton button:hover {{
    background-color: {C['accent_secondary']} !important;
    border-color: {C['accent_secondary']} !important;
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
    transform: translateY(-1px);
}}

.stButton button:active {{
    transform: translateY(0);
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}}

/* ===== MINIMALIST INPUTS ===== */
.stTextArea textarea, 
.stTextInput input,
.stSelectbox select {{
    background-color: {C['bg_secondary']} !important;
    color: {C['text_primary']} !important;
    border-radius: 6px !important;
    border: 1px solid {C['border_light']} !important;
    transition: all 0.25s ease !important;
    font-size: 14px !important;
    line-height: 1.6 !important;
    padding: 12px 14px !important;
}}

.stTextArea textarea:focus, 
.stTextInput input:focus,
.stSelectbox select:focus {{
    border-color: {C['accent_primary']} !important;
    box-shadow: 0 0 0 3px rgba(44, 62, 80, 0.06) !important;
    background-color: {C['bg_secondary']} !important;
}}

/* ===== MINIMALIST TABS ===== */
.stTabs [data-baseweb="tab-list"] {{
    gap: 4px;
    background-color: {C['bg_secondary']};
    padding: 4px;
    border-radius: 6px;
    border: 1px solid {C['border_light']};
    margin-bottom: 24px;
}}

.stTabs [data-baseweb="tab"] {{
    height: 44px;
    white-space: pre;
    background-color: transparent !important;
    border-radius: 4px !important;
    color: {C['text_secondary']} !important;
    border: none !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
    padding: 0 18px !important;
    font-size: 13px !important;
}}

.stTabs [data-baseweb="tab"]:hover {{
    color: {C['text_primary']} !important;
    background-color: {C['bg_tertiary']} !important;
}}

.stTabs [aria-selected="true"] {{
    background-color: {C['bg_primary']} !important;
    color: {C['accent_primary']} !important;
    border-bottom: 2px solid {C['accent_primary']} !important;
}}

/* ===== MINIMALIST FILE UPLOADER ===== */
[data-testid="stFileUploader"] {{
    background-color: {C['bg_secondary']};
    border: 1px dashed {C['border_light']};
    border-radius: 8px;
    padding: 24px;
    transition: all 0.25s ease;
}}

[data-testid="stFileUploader"]:hover {{
    border-color: {C['accent_primary']};
    background-color: {C['bg_tertiary']};
}}

/* ===== MINIMALIST ALERTS ===== */
.stAlert {{
    background-color: {C['bg_secondary']} !important;
    border: 1px solid {C['border_light']} !important;
    border-radius: 8px !important;
    color: {C['text_secondary']} !important;
    border-left: 4px solid {C['accent_tertiary']} !important;
}}

/* ===== MINIMALIST COPY AREA ===== */
.copy-area {{
    background-color: {C['bg_tertiary']};
    border: 1px solid {C['border_light']};
    border-radius: 8px;
    padding: 16px;
    font-family: 'Courier New', Courier, monospace;
    font-size: 13px;
    color: {C['text_primary']};
    max-height: 400px;
    overflow-y: auto;
    white-space: pre-wrap;
    line-height: 1.6;
}}

/* ===== MINIMALIST GAUGE ===== */
.gauge-container {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 140px;
    margin: 10px auto;
    animation: slideInUp 0.6s ease-out backwards;
}}

@keyframes slideInUp {{
    from {{
        opacity: 0;
        transform: translateY(20px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

/* ===== MINIMALIST EXPANDERS ===== */
.stExpander {{
    background-color: {C['bg_secondary']} !important;
    border: 1px solid {C['border_light']} !important;
    border-radius: 6px !important;
    margin-bottom: 12px !important;
}}

.stExpander:hover {{
    border-color: {C['accent_tertiary']} !important;
}}

/* ===== MINIMALIST BULLET LIST ===== */
.bullet-item {{
    display: flex;
    align-items: flex-start;
    gap: 12px;
    margin-bottom: 12px;
    padding: 12px 16px;
    background-color: {C['bg_tertiary']};
    border-left: 3px solid {C['accent_tertiary']};
    border-radius: 4px;
    transition: all 0.25s ease;
}}

.bullet-item:hover {{
    background-color: {C['bg_secondary']};
    border-left-color: {C['accent_primary']};
    transform: translateX(4px);
}}

.bullet-icon {{
    font-weight: 700;
    font-size: 16px;
    min-width: 20px;
    text-align: center;
    margin-top: 2px;
}}

.bullet-text {{
    color: {C['text_secondary']};
    font-size: 13.5px;
    line-height: 1.5;
    font-weight: 400;
}}

/* ===== MINIMALIST KEYWORD BADGE ===== */
.keyword-badge {{
    display: inline-flex;
    align-items: center;
    padding: 6px 12px;
    background-color: {C['bg_tertiary']};
    border: 1px solid {C['border_light']};
    border-radius: 20px;
    font-size: 12px;
    color: {C['text_primary']};
    font-family: 'Inter', sans-serif;
    margin-right: 8px;
    margin-bottom: 8px;
    transition: all 0.2s ease;
}}

.keyword-badge:hover {{
    border-color: {C['accent_primary']};
    background-color: {C['bg_secondary']};
    transform: scale(1.05);
}}

.keyword-badge.present {{
    border-color: {C['success']};
    background-color: rgba(39, 174, 96, 0.08);
    color: {C['success']};
}}

.keyword-badge.missing {{
    border-color: {C['error']};
    background-color: rgba(231, 76, 60, 0.08);
    color: {C['error']};
}}

/* ===== MINIMALIST OPTIMIZER CARD ===== */
.optimizer-card {{
    background-color: {C['bg_secondary']};
    border: 1px solid {C['border_light']};
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 16px;
    transition: all 0.3s ease;
}}

.optimizer-card:hover {{
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
    border-color: {C['accent_tertiary']};
}}

.optimizer-section {{
    margin-bottom: 14px;
}}

.optimizer-section:last-child {{
    margin-bottom: 0;
}}

.optimizer-label {{
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding: 3px 8px;
    border-radius: 4px;
    display: inline-block;
    margin-bottom: 6px;
}}

.optimizer-label.original {{
    background-color: rgba(231, 76, 60, 0.08);
    color: {C['error']};
}}

.optimizer-label.optimized {{
    background-color: rgba(39, 174, 96, 0.08);
    color: {C['success']};
}}

.optimizer-text {{
    font-size: 13.5px;
    line-height: 1.6;
    color: {C['text_secondary']};
}}

.optimizer-text.optimized {{
    color: {C['text_primary']};
    font-weight: 500;
    border-left: 3px solid {C['accent_primary']};
    padding-left: 12px;
}}

.optimizer-rationale {{
    background-color: {C['bg_tertiary']};
    padding: 12px 14px;
    border-radius: 6px;
    font-size: 12px;
    color: {C['text_secondary']};
    margin-top: 12px;
}}

/* ===== WORKFLOW GUIDE ANIMATION ===== */
@keyframes pulse-gentle {{
    0%, 100% {{
        opacity: 1;
    }}
    50% {{
        opacity: 0.7;
    }}
}}

.workflow-highlight {{
    animation: pulse-gentle 2s ease-in-out infinite;
}}

/* ===== RESPONSIVE LAYOUT ===== */
@media (max-width: 768px) {{
    .main-title {{
        font-size: 1.8rem;
    }}
    
    .glass-card {{
        padding: 16px;
    }}
}}
</style>
""", unsafe_allow_html=True)

# ---------------- HELPER UI FUNCTIONS ----------------

def draw_gauge(score, label, delay=0):
    """Draws a minimalist, elegant gauge with subtle animation."""
    radius = 35
    circumference = 2 * 3.14159 * radius
    stroke_offset = circumference - (circumference * (score / 100))
    
    svg = f"""
    <div class="gauge-container" style="animation-delay: {delay}s;">
        <svg width="110" height="110" viewBox="0 0 110 110" style="filter: drop-shadow(0 2px 4px rgba(0,0,0,0.08));">
            <!-- Background circle -->
            <circle cx="55" cy="55" r="{radius}" stroke="{C['border_light']}" stroke-width="5" fill="none"/>
            
            <!-- Progress circle with subtle gradient -->
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
                    style="transition: stroke-dashoffset 1.2s cubic-bezier(0.34, 1.56, 0.64, 1); transform-origin: 55px 55px;"/>
        </svg>
        
        <div style="position: absolute; margin-top: 22px; text-align: center;">
            <div style="font-size: 24px; font-weight: 700; color: {C['text_primary']}; font-family: 'Plus Jakarta Sans';">
                {score}%
            </div>
            <div style="font-size: 10px; font-weight: 600; color: {C['text_muted']}; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 4px;">
                {label}
            </div>
        </div>
    </div>
    """
    return svg.strip()

def make_bullet_list(items, is_positive=True):
    """Renders minimalist bullet list items."""
    icon = "✔️" if is_positive else "⚠"
    color = C['success'] if is_positive else C['warning']
    
    html = ""
    for idx, item in enumerate(items):
        animation_delay = idx * 0.08
        html += f"""
        <div class="bullet-item" style="animation: slideInUp 0.5s ease-out {animation_delay}s backwards;">
            <div class="bullet-icon" style="color: {color};">{icon}</div>
            <div class="bullet-text">{item}</div>
        </div>
        """
    return html

def make_keyword_badges(keywords):
    """Renders minimalist keyword badge grid."""
    html = '<div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; margin-bottom: 15px;">'
    for idx, kw_data in enumerate(keywords):
        kw = kw_data.get("keyword", "")
        status = kw_data.get("status", "Present")
        
        badge_class = "present" if status == "Present" else "missing"
        icon = "✓" if status == "Present" else "✗"
        animation_delay = (idx % 8) * 0.06
        
        html += f"""
        <div class="keyword-badge {badge_class}" style="animation: slideInUp 0.4s ease-out {animation_delay}s backwards;">
            <span style="margin-right: 6px; font-weight: 700;">{icon}</span>
            <span>{kw}</span>
        </div>
        """
    html += '</div>'
    return html

def make_optimizer_card(original, optimized, rationale):
    """Renders minimalist side-by-side comparison card."""
    return f"""
    <div class="optimizer-card">
        <div class="optimizer-section">
            <div class="optimizer-label original">Original</div>
            <p class="optimizer-text">{original}</p>
        </div>
        
        <div class="optimizer-section">
            <div class="optimizer-label optimized">Optimized</div>
            <p class="optimizer-text optimized">{optimized}</p>
        </div>
        
        <div class="optimizer-rationale">
            <strong>Why this helps:</strong> {rationale}
        </div>
    </div>
    """

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown(f"""
    <div style='text-align: center; margin-bottom: 20px;'>
        <h2 style='color: {C["text_primary"]}; margin-bottom: 0; font-size: 1.3rem;'>⚙️ Setup</h2>
        <span style='color: {C["text_muted"]}; font-size: 11px;'>Configure your analysis</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Dark mode toggle
    st.session_state.dark_mode = st.toggle("Dark Mode", value=st.session_state.dark_mode)
    
    env_key = os.getenv("GROQ_API_KEY")
    api_key = env_key or None

    if env_key:
        st.success("✓ Analyzer connected", icon="✓")
    else:
        st.warning("⚠ Setup incomplete", icon="⚠")

    st.markdown("---")

    st.markdown("### Your Target Role")
    target_role = st.text_input("Role", placeholder="e.g., Frontend Developer", label_visibility="collapsed")
    experience_level = st.selectbox(
        "Experience",
        ["Not specified", "Student / Fresher", "Entry level", "Mid level", "Senior level"],
        index=0,
        label_visibility="collapsed"
    )
    focus_area = st.selectbox(
        "Focus",
        ["Overall match", "Missing keywords", "Resume wording", "Interview preparation"],
        index=0,
        label_visibility="collapsed"
    )

# ---------------- HEADER ----------------
st.markdown(f"""
<div class='main-title'>📄 Resume Match</div>
<div class='subtitle'>
Analyze your resume against job descriptions and optimize your application
</div>
""", unsafe_allow_html=True)

# Initialize Session State for analysis results
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

# ---------------- INPUT SECTION ----------------
st.markdown(f"""
<div style="margin-bottom: 32px;">
    <h3 style="color: {C['text_primary']}; font-size: 0.95rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: {C['text_muted']};">
        Step 1: Upload Your Materials
    </h3>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown(f"""
    <div class="glass-card-header">
        📄 Your Resume
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload (.pdf, .docx, .txt)", type=["pdf", "docx", "txt"], label_visibility="collapsed")
    
    if uploaded_file is not None:
        try:
            with st.spinner("Extracting content..."):
                extracted_text = utils.parse_resume_file(uploaded_file)
                st.session_state.resume_text = extracted_text
            st.success(f"✓ Loaded {uploaded_file.name}")
        except Exception as e:
            st.error(f"Error: {str(e)}")
            
    resume_input = st.text_area("Or paste resume text", value=st.session_state.resume_text, height=200, label_visibility="collapsed", placeholder="Paste your resume content here...")
    if resume_input != st.session_state.resume_text:
        st.session_state.resume_text = resume_input

with col2:
    st.markdown(f"""
    <div class="glass-card-header">
        💼 Job Description
    </div>
    """, unsafe_allow_html=True)
    
    job_desc = st.text_area("Paste job description", height="208px", label_visibility="collapsed", placeholder="Paste the job description you're applying for...")

# ---------------- WORKFLOW GUIDE - ANALYZE BUTTON ----------------
st.markdown("<div style='margin: 40px 0 30px 0;'>", unsafe_allow_html=True)

col_left, col_center, col_right = st.columns([1, 2, 1])
with col_center:
    analyze_btn = st.button("🚀 Analyze & Optimize", key="analyze_main", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# Analysis logic
if analyze_btn:
    if not api_key:
        st.error("The analyzer is not connected. Please ask the app owner to set up the API.")
    elif not st.session_state.resume_text.strip():
        st.error("Please upload or paste your resume.")
    elif not job_desc.strip():
        st.error("Please paste the job description.")
    else:
        with st.spinner("Analyzing your resume..."):
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
                st.success("✓ Analysis complete!")
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")

# ---------------- RESULTS DASHBOARD ----------------
if st.session_state.analysis_results:
    res = st.session_state.analysis_results
    
    # Dashboard header
    st.markdown(f"""
    <div style="margin-top: 48px; margin-bottom: 32px;">
        <h3 style="color: {C['text_primary']}; font-size: 0.95rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: {C['text_muted']};">
            Step 2: Review Your Analysis
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Main Dashboard Gauges - Staggered Animation
    st.markdown(f"""
    <div class="glass-card" style="text-align: center; padding: 32px 24px;">
        <div style="display: flex; flex-wrap: wrap; justify-content: center; width: 100%; gap: 20px; margin: 20px 0;">
    """, unsafe_allow_html=True)
    
    gauge_cols = st.columns(4)
    gauge_data = [
        (res.get("ats_score", 0), "ATS Score", 0.0),
        (res.get("match_percentage", 0), "Job Match", 0.15),
        (res.get("formatting_score", 0), "Format", 0.30),
        (res.get("keyword_score", 0), "Keywords", 0.45),
    ]
    
    for col, (score, label, delay) in zip(gauge_cols, gauge_data):
        with col:
            st.markdown(draw_gauge(score, label, delay), unsafe_allow_html=True)
    
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Results Tabs
    tab_overview, tab_keywords, tab_optimization, tab_cover_letter, tab_interview = st.tabs([
        "📈 Overview", 
        "🔍 Keywords", 
        "🛠️ Optimize", 
        "✉️ Cover Letter", 
        "🗣️ Interview Prep"
    ])
    
    # --- TAB 1: OVERVIEW ---
    with tab_overview:
        col_sum, col_items = st.columns([1, 1.1], gap="large")
        
        with col_sum:
            st.markdown("**Fit Assessment**")
            st.markdown(f"""
            <div style="background-color: {C['bg_secondary']}; border: 1px solid {C['border_light']}; border-radius: 8px; padding: 20px; line-height: 1.7; color: {C['text_secondary']}; font-size: 14px;">
                {res.get('analysis_summary', 'No summary provided.')}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**ATS Compatibility Checks**")
            
            for idx, check in enumerate(res.get("ats_compatibility_checks", [])):
                chk_name = check.get("check", "")
                chk_status = check.get("status", "Passed")
                chk_feedback = check.get("feedback", "")
                
                status_color = C['success'] if chk_status == "Passed" else (C['warning'] if chk_status == "Warning" else C['error'])
                status_symbol = "●"
                
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid {C['border_subtle']}; padding: 12px 0;">
                    <div>
                        <div style="font-size: 13px; font-weight: 600; color: {C['text_primary']};">{chk_name}</div>
                        <div style="font-size: 12px; color: {C['text_muted']}; margin-top: 2px;">{chk_feedback}</div>
                    </div>
                    <div style="color: {status_color}; font-weight: 700; font-size: 12px; display: flex; align-items: center; gap: 6px; text-transform: uppercase;">
                        <span>{status_symbol}</span>{chk_status}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col_items:
            st.markdown("**Key Alignments**")
            st.markdown(make_bullet_list(res.get("key_strengths", []), is_positive=True), unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("**Action Items**")
            st.markdown(make_bullet_list(res.get("critical_issues", []), is_positive=False), unsafe_allow_html=True)
    
    # --- TAB 2: KEYWORDS ---
    with tab_keywords:
        st.markdown("**Keywords & Skills from Job Post**")
        
        keywords_list = res.get("keyword_analysis", [])
        present_kws = [k for k in keywords_list if k.get("status") == "Present"]
        missing_kws = [k for k in keywords_list if k.get("status") != "Present"]
        
        col_pres, col_miss = st.columns(2)
        
        with col_pres:
            st.markdown(f"**Present ({len(present_kws)})**")
            if present_kws:
                st.markdown(make_keyword_badges(present_kws), unsafe_allow_html=True)
            else:
                st.info("No matching keywords found.")
                
        with col_miss:
            st.markdown(f"**Missing ({len(missing_kws)})**")
            if missing_kws:
                st.markdown(make_keyword_badges(missing_kws), unsafe_allow_html=True)
            else:
                st.success("All critical keywords present!")
        
        st.divider()
        st.markdown("**Skills Gaps**")
        
        gaps = res.get("skills_gap", [])
        if gaps:
            for gap in gaps:
                skill_name = gap.get("skill", "")
                category = gap.get("category", "Skill")
                desc = gap.get("gap_description", "")
                
                st.markdown(f"""
                <div style="background-color: rgba(231, 76, 60, 0.04); border-left: 3px solid {C['error']}; border-radius: 6px; padding: 14px; margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <span style="font-weight: 700; color: {C['error']}; font-size: 14px;">{skill_name}</span>
                        <span style="font-size: 9px; font-weight: 700; text-transform: uppercase; background-color: rgba(231, 76, 60, 0.1); color: {C['error']}; padding: 2px 6px; border-radius: 4px;">{category}</span>
                    </div>
                    <div style="color: {C['text_secondary']}; font-size: 12.5px; line-height: 1.5;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("No major skills gaps identified.")
    
    # --- TAB 3: OPTIMIZE ---
    with tab_optimization:
        st.markdown("**Rewrite Suggestions**")
        st.markdown("Replace weak phrasing with high-impact accomplishments tailored to the role.")
        
        snippets = res.get("optimized_resume_snippets", [])
        if snippets:
            for snip in snippets:
                orig = snip.get("original", "")
                opt = snip.get("optimized", "")
                rat = snip.get("rationale", "")
                st.markdown(make_optimizer_card(orig, opt, rat), unsafe_allow_html=True)
        else:
            st.info("Your bullet points are strong! No rewrites needed.")
        
        st.divider()
        st.markdown("**General Improvements**")
        for advice in res.get("improvement_suggestions", []):
            st.markdown(f"• {advice}")
    
    # --- TAB 4: COVER LETTER ---
    with tab_cover_letter:
        st.markdown("**Your Tailored Cover Letter**")
        
        cl_text = res.get("cover_letter", "")
        if cl_text:
            st.markdown(f'<div class="copy-area">{cl_text}</div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            col_cl1, col_cl2 = st.columns([1, 1])
            with col_cl1:
                st.download_button(
                    label="📥 Download (.txt)",
                    data=cl_text,
                    file_name="cover_letter.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            with col_cl2:
                st.info("Copy the text directly to your word processor.")
        else:
            st.info("No cover letter generated.")
    
    # --- TAB 5: INTERVIEW ---
    with tab_interview:
        st.markdown("**Mock Interview Questions**")
        st.markdown("Prepare for challenging questions based on your experience gaps.")
        
        questions = res.get("interview_questions", [])
        if questions:
            for idx, q_item in enumerate(questions):
                q = q_item.get("question", "")
                rationale = q_item.get("rationale", "")
                
                with st.expander(f"Question {idx+1}: {q[:80]}..."):
                    st.markdown(f"""
                    <div style="padding: 10px 0;">
                        <p style="font-size: 14px; font-weight: 600; color: {C['text_primary']}; margin-bottom: 12px;">{q}</p>
                        <div style="background-color: {C['bg_tertiary']}; border-left: 3px solid {C['info']}; padding: 12px 14px; border-radius: 6px;">
                            <span style="font-size: 9.5px; font-weight: 700; text-transform: uppercase; color: {C['accent_primary']}; display: block; margin-bottom: 6px;">Why they ask this:</span>
                            <span style="font-size: 13px; color: {C['text_secondary']}; line-height: 1.5;">{rationale}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No interview questions generated.")

# Final note
st.markdown(f"""
<div style="margin-top: 60px; padding: 20px; text-align: center; border-top: 1px solid {C['border_light']}; color: {C['text_muted']}; font-size: 12px;">
    Ready to apply? Download your optimized materials and submit your application with confidence.
</div>
""", unsafe_allow_html=True)
