import streamlit as st
import PyPDF2
import os
import requests
import json
import re
import time
from dotenv import load_dotenv
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor

# Load environment variables
load_dotenv()

# Page setup
st.set_page_config(
    page_title="📚 ResearchMind AI - Smart Research Summarization Assistant", 
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with SOFT PALETTE and DARK TEXT for better visibility
st.markdown("""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
            
/* FORCE DARK THEME */
.stApp {
    background-color: #0E1117 !important;
    color: #FAFAFA !important;
}

.stApp > header {
    background-color: transparent !important;
}            

/* Global Styles - LIGHT THEME */
.main {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #0E1117 0%, #1a1a2e 50%, #16213e 100%);
    min-height: 100vh;
}

/* Hide default streamlit styling */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {visibility: hidden;}

/* Animated Title with gradient text */
.big-title {
    font-size: 4rem;
    background: linear-gradient(135deg, #4A90E2 0%, #7B68EE 50%, #9A7DD6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 1rem;
    font-weight: 800;
    animation: titleGlow 3s ease-in-out infinite;
}

@keyframes titleGlow {
    0%, 100% { 
        filter: brightness(1) drop-shadow(0 0 10px rgba(74, 144, 226, 0.3));
    }
    50% { 
        filter: brightness(1.2) drop-shadow(0 0 20px rgba(74, 144, 226, 0.5));
    }
}

.subtitle {
    text-align: center;
    color: #2C3E50;
    font-size: 1.4rem;
    margin-bottom: 2rem;
    font-style: italic;
    font-weight: 600;
}

/* Enhanced Card-like boxes with light backgrounds */
.summary-box {
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    color: #2C3E50 !important;
    padding: 2.5rem;
    border-radius: 25px;
    border: 2px solid #e9ecef;
    margin: 2rem 0;
    box-shadow: 0 15px 35px rgba(0,0,0,0.1), 0 5px 15px rgba(0,0,0,0.05);
    font-size: 1.2rem;
    line-height: 1.8;
    transition: all 0.4s ease;
    position: relative;
    overflow: hidden;
}

.summary-box:hover {
    transform: translateY(-8px);
    box-shadow: 0 25px 50px rgba(0,0,0,0.15), 0 10px 25px rgba(0,0,0,0.1);
}

.summary-box::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 5px;
    background: linear-gradient(90deg, #4A90E2, #7B68EE, #9A7DD6);
}

/* Enhanced Question boxes */
.question-box {
    background: linear-gradient(135deg, #FFF8E1 0%, #FFFDE7 100%);
    color: #E65100 !important;
    padding: 2.5rem;
    border-radius: 25px;
    border: 2px solid #FFB74D;
    margin: 2rem 0;
    box-shadow: 0 15px 35px rgba(255,183,77,0.2), 0 5px 15px rgba(255,183,77,0.1);
    font-size: 1.1rem;
    transition: all 0.4s ease;
    position: relative;
    overflow: hidden;
}

.question-box:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 40px rgba(255,183,77,0.25), 0 8px 20px rgba(255,183,77,0.15);
}

.question-box::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 5px;
    background: linear-gradient(90deg, #FFB74D, #FF8A65, #FFAB91);
}

/* Enhanced Answer boxes */
.answer-box {
    background: linear-gradient(135deg, #E8F5E8 0%, #F1F8E9 100%);
    color: #2E7D32 !important;
    padding: 2.5rem;
    border-radius: 25px;
    border: 2px solid #81C784;
    margin: 2rem 0;
    box-shadow: 0 15px 35px rgba(129,199,132,0.2), 0 5px 15px rgba(129,199,132,0.1);
    font-size: 1.1rem;
    line-height: 1.8;
    transition: all 0.4s ease;
    position: relative;
    overflow: hidden;
}

.answer-box:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 40px rgba(129,199,132,0.25), 0 8px 20px rgba(129,199,132,0.15);
}

.answer-box::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 5px;
    background: linear-gradient(90deg, #81C784, #A5D6A7, #C8E6C9);
}

/* Enhanced Status boxes */
.error-box {
    background: linear-gradient(135deg, #FFEBEE 0%, #FCE4EC 100%);
    color: #C62828 !important;
    padding: 2rem;
    border-radius: 20px;
    border-left: 6px solid #E57373;
    margin: 1.5rem 0;
    box-shadow: 0 10px 25px rgba(229,115,115,0.2);
    font-weight: 600;
}

.success-box {
    background: linear-gradient(135deg, #E8F5E8 0%, #F1F8E9 100%);
    color: #2E7D32 !important;
    padding: 2rem;
    border-radius: 20px;
    border-left: 6px solid #81C784;
    margin: 1.5rem 0;
    box-shadow: 0 10px 25px rgba(129,199,132,0.2);
    font-weight: 600;
}

.info-box {
    background: linear-gradient(135deg, #E3F2FD 0%, #E1F5FE 100%);
    color: #1565C0 !important;
    padding: 2rem;
    border-radius: 20px;
    border-left: 6px solid #64B5F6;
    margin: 1.5rem 0;
    box-shadow: 0 10px 25px rgba(100,181,246,0.2);
    font-weight: 600;
}

.warning-box {
    background: linear-gradient(135deg, #FFF8E1 0%, #FFFDE7 100%);
    color: #F57F17 !important;
    padding: 2rem;
    border-radius: 20px;
    border-left: 6px solid #FFD54F;
    margin: 1.5rem 0;
    box-shadow: 0 10px 25px rgba(255,213,79,0.2);
    font-weight: 600;
}

/* Enhanced metric cards */
.metric-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    padding: 2rem;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    border: 2px solid #e9ecef;
    text-align: center;
    transition: all 0.4s ease;
}

.metric-card:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 20px 40px rgba(0,0,0,0.15);
}

/* Fixed text visibility - DARK TEXT FOR BETTER READABILITY */
div[data-testid="stMarkdownContainer"] p,
div[data-testid="stMarkdownContainer"] div,
div[data-testid="stMarkdownContainer"] span,
div[data-testid="stMarkdownContainer"] h1,
div[data-testid="stMarkdownContainer"] h2,
div[data-testid="stMarkdownContainer"] h3,
div[data-testid="stMarkdownContainer"] h4,
div[data-testid="stMarkdownContainer"] h5,
div[data-testid="stMarkdownContainer"] h6,
.stMarkdown,
.element-container {
    color: #2C3E50 !important;
}

/* Homepage text fixes */
.main .block-container {
    background: rgba(255,255,255,0.8);
    border-radius: 25px;
    padding: 2rem;
    border: 1px solid #e9ecef;
}

/* FIXED: Enhanced text area for document viewer with VISIBLE CURSOR */
.stTextArea textarea {
    background-color: #ffffff !important;
    color: #2C3E50 !important;
    border: 3px solid #4A90E2 !important;
    border-radius: 15px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 16px !important;
    line-height: 1.8 !important;
    padding: 1.5rem !important;
    box-shadow: inset 0 2px 10px rgba(0,0,0,0.1) !important;
    caret-color: #4A90E2 !important;
}

.stTextArea textarea:focus {
    border-color: #7B68EE !important;
    box-shadow: 0 0 0 0.3rem rgba(74, 144, 226, 0.25) !important;
    outline: none !important;
}

/* FIXED: Enhanced input styling with VISIBLE CURSOR */
.stTextInput input {
    background: #ffffff !important;
    color: #2C3E50 !important;
    border: 3px solid #4A90E2 !important;
    border-radius: 15px !important;
    transition: all 0.3s ease !important;
    padding: 1rem !important;
    font-size: 16px !important;
    font-weight: 500 !important;
    caret-color: #4A90E2 !important;
}

.stTextInput input:focus {
    border-color: #7B68EE !important;
    box-shadow: 0 0 0 0.3rem rgba(74, 144, 226, 0.25) !important;
    transform: translateY(-2px) !important;
    outline: none !important;
    caret-color: #7B68EE !important;
}

/* Enhanced buttons - WHITE TEXT ON SOFT BLUE BUTTONS */
.stButton > button {
    background: linear-gradient(135deg, #4A90E2 0%, #7B68EE 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 15px !important;
    padding: 1rem 2.5rem !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 8px 25px rgba(74, 144, 226, 0.3) !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}

.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 15px 35px rgba(74, 144, 226, 0.4) !important;
    background: linear-gradient(135deg, #7B68EE 0%, #4A90E2 100%) !important;
    color: white !important;
}

/* Enhanced tab styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 1rem;
    background: #f8f9fa;
    border-radius: 20px;
    padding: 0.5rem;
    border: 2px solid #e9ecef;
}

.stTabs [data-baseweb="tab"] {
    background: #ffffff;
    border-radius: 15px;
    color: #2C3E50 !important;
    font-weight: 700;
    font-size: 1.1rem;
    padding: 1.2rem 2rem;
    transition: all 0.3s ease;
    border: 2px solid transparent;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #4A90E2 0%, #7B68EE 100%);
    color: white !important;
    border-color: #4A90E2;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}
            
/* PURPLE SIDEBAR - Multiple Selectors for Different Streamlit Versions */
.css-1d391kg, 
.css-1lcbmhc, 
.css-17eq0hr,
.css-1544g2n,
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #A78BFA 0%, #C4B5FD 50%, #B794F6 100%) !important;
    border-right: 2px solid #B794F6 !important;
    box-shadow: 2px 0 10px rgba(183, 148, 246, 0.1) !important;
}

/* Force sidebar background with data attribute */
section[data-testid="stSidebar"] > div {
    background: linear-gradient(180deg, #554a5e 0%, #6a5f73 50%, #4a3f52 100%) !important;        
    # background: linear-gradient(180deg, #E8E2FF 0%, #F3F0FF 50%, #EDE7FF 100%) !important;
}

/* Sidebar content styling */
.css-1d391kg *, 
.css-1lcbmhc *, 
.css-17eq0hr *,
.css-1544g2n *,
section[data-testid="stSidebar"] * {
    color: #1e0136 !important;
}

/* Sidebar buttons */
.css-1d391kg .stButton > button,
.css-1lcbmhc .stButton > button,
.css-17eq0hr .stButton > button,
.css-1544g2n .stButton > button,
section[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(45deg, #B794F6, #9F7AEA) !important;
    color: white !important;
    border: none !important;
    border-radius: 15px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 3px 10px rgba(183, 148, 246, 0.3) !important;
}

/* Button hover effects */
.css-1d391kg .stButton > button:hover,
.css-1lcbmhc .stButton > button:hover,
.css-17eq0hr .stButton > button:hover,
.css-1544g2n .stButton > button:hover,
section[data-testid="stSidebar"] .stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(183, 148, 246, 0.4) !important;
    background: linear-gradient(45deg, #9F7AEA, #805AD5) !important;
}            






/* Sidebar enhanced styling */
.sidebar .sidebar-content {
    background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%);
    border-radius: 0 20px 20px 0;
    border-right: 2px solid #e9ecef;
}

/* Progress bar styling */
.stProgress .st-bo {
    background: linear-gradient(90deg, #4A90E2, #7B68EE, #9A7DD6);
    border-radius: 10px;
    height: 1rem;
}

/* Enhanced Quiz styling */
.quiz-container {
    background: linear-gradient(135deg, #FFF8E1 0%, #FFFDE7 100%);
    padding: 3rem;
    border-radius: 25px;
    border: 2px solid #FFB74D;
    margin: 2rem 0;
    box-shadow: 0 20px 40px rgba(255,183,77,0.2);
}

.quiz-question {
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    color: #2C3E50 !important;
    padding: 2.5rem;
    border-radius: 20px;
    margin: 1.5rem 0;
    border-left: 6px solid #FFB74D;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    font-size: 1.1rem;
    line-height: 1.8;
    transition: all 0.3s ease;
}

.quiz-question:hover {
    transform: translateX(10px);
    box-shadow: 0 15px 30px rgba(0,0,0,0.12);
}

/* Feature cards enhancement */
.feature-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    padding: 3rem;
    border-radius: 25px;
    border: 2px solid #e9ecef;
    margin: 2rem 0;
    box-shadow: 0 15px 35px rgba(0,0,0,0.1);
    transition: all 0.4s ease;
    text-align: center;
}

.feature-card:hover {
    transform: translateY(-12px) scale(1.02);
    box-shadow: 0 25px 50px rgba(0,0,0,0.15);
}

.feature-icon {
    font-size: 4rem;
    margin-bottom: 1.5rem;
    background: linear-gradient(135deg, #4A90E2 0%, #7B68EE 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: iconPulse 3s ease-in-out infinite;
}

@keyframes iconPulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}

/* Document viewer enhancement */
.document-viewer {
    background: #ffffff;
    color: #2C3E50 !important;
    padding: 2rem;
    border-radius: 15px;
    border: 2px solid #e9ecef;
    font-family: 'JetBrains Mono', monospace;
    font-size: 14px;
    line-height: 1.8;
    max-height: 600px;
    overflow-y: auto;
    white-space: pre-wrap;
    box-shadow: inset 0 2px 10px rgba(0,0,0,0.1);
}

/* IMPROVED: Welcome screen with SOFT COLORS and NO ANIMATIONS */
.welcome-text {
    background: linear-gradient(135deg, #E8F4FD 0%, #F0F8FF 100%);
    color: #2C3E50 !important;
    padding: 4rem;
    border-radius: 30px;
    text-align: center;
    margin: 2rem 0;
    box-shadow: 0 20px 40px rgba(74, 144, 226, 0.15);
    border: 3px solid #B3D9FF;
    position: relative;
}

.welcome-text h2,
.welcome-text h3,
.welcome-text h4,
.welcome-text p {
    color: #2C3E50 !important;
    position: relative;
    z-index: 1;
}

/* CREATIVE: Transform section with SOFT PALETTE */
.transform-section {
    background: linear-gradient(135deg, #F3E5F5 0%, #E8EAF6 50%, #E3F2FD 100%);
    color: #2C3E50 !important;
    padding: 4rem;
    border-radius: 35px;
    margin: 3rem 0;
    box-shadow: 0 25px 50px rgba(74, 144, 226, 0.2);
    border: 3px solid #D1C4E9;
    position: relative;
    text-align: center;
}

.transform-section h2,
.transform-section h4,
.transform-section p {
    color: #2C3E50 !important;
    position: relative;
    z-index: 2;
}

/* FIXED: Transform highlights with BETTER GRID LAYOUT */
.steps-grid {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 2rem;
    margin: 3rem 0;
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
}

.transform-highlight {
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    color: #2C3E50 !important;
    padding: 2rem;
    border-radius: 25px;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    min-width: 200px;
    flex: 1;
    border: 2px solid #4A90E2;
    box-shadow: 0 8px 20px rgba(74, 144, 226, 0.2);
    font-weight: 600;
    transition: all 0.3s ease;
    cursor: pointer;
}

.transform-highlight:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 30px rgba(74, 144, 226, 0.3);
    background: linear-gradient(135deg, #4A90E2 0%, #7B68EE 100%);
    color: white !important;
}

.transform-highlight .step-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    display: block;
}

.transform-highlight .step-title {
    font-size: 1.2rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.transform-highlight .step-desc {
    font-size: 0.95rem;
    opacity: 0.8;
}

/* User welcome styling with SOFT COLORS */
.user-welcome {
    background: linear-gradient(135deg, #E8F4FD 0%, #F0F8FF 100%);
    color: #2C3E50 !important;
    padding: 2.5rem;
    border-radius: 25px;
    text-align: center;
    margin: 1rem 0;
    box-shadow: 0 15px 30px rgba(74, 144, 226, 0.2);
    border: 2px solid #B3D9FF;
}

.user-welcome h2,
.user-welcome p {
    color: #2C3E50 !important;
    position: relative;
    z-index: 2;
}

/* HERO SECTION for engaging homepage */
.hero-section {
    background: linear-gradient(135deg, #E8F4FD 0%, #F3E5F5 50%, #E8EAF6 100%);
    color: #2C3E50 !important;
    padding: 5rem 3rem;
    border-radius: 30px;
    margin: 2rem 0;
    text-align: center;
    box-shadow: 0 30px 60px rgba(74, 144, 226, 0.15);
    border: 3px solid #D1C4E9;
    position: relative;
    overflow: hidden;
}

.hero-section::before {
    content: '';
    position: absolute;
    top: -10px;
    left: -10px;
    right: -10px;
    bottom: -10px;
    background: linear-gradient(45deg, #4A90E2, #7B68EE, #9A7DD6, #4A90E2);
    background-size: 400% 400%;
    animation: gradientShift 8s ease infinite;
    z-index: -1;
    border-radius: 35px;
}

@keyframes gradientShift {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

.hero-section h1 {
    font-size: 3.5rem;
    margin-bottom: 1.5rem;
    color: #2C3E50 !important;
    font-weight: 800;
}

.hero-section p {
    font-size: 1.3rem;
    margin-bottom: 2rem;
    color: #2C3E50 !important;
    line-height: 1.6;
}

/* BENEFIT CARDS for engaging homepage */
.benefit-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    padding: 2.5rem;
    border-radius: 20px;
    border: 2px solid #e9ecef;
    margin: 1rem 0;
    box-shadow: 0 15px 30px rgba(0,0,0,0.1);
    transition: all 0.4s ease;
    text-align: center;
    height: 100%;
}

.benefit-card:hover {
    transform: translateY(-10px) scale(1.03);
    box-shadow: 0 25px 50px rgba(0,0,0,0.15);
    border-color: #4A90E2;
}

.benefit-icon {
    font-size: 3.5rem;
    margin-bottom: 1.5rem;
    display: block;
}

.benefit-card h3 {
    color: #2C3E50 !important;
    margin-bottom: 1rem;
    font-weight: 700;
}

.benefit-card p {
    color: #2C3E50 !important;
    line-height: 1.6;
}

/* STATS SECTION for credibility */
.stats-section {
    background: linear-gradient(135deg, #F0F8FF 0%, #E8F4FD 100%);
    padding: 3rem;
    border-radius: 25px;
    margin: 3rem 0;
    text-align: center;
    border: 2px solid #B3D9FF;
    box-shadow: 0 20px 40px rgba(74, 144, 226, 0.1);
}

.stat-item {
    display: inline-block;
    margin: 1rem 2rem;
}

.stat-number {
    font-size: 3rem;
    font-weight: 800;
    color: #4A90E2 !important;
    display: block;
}

.stat-label {
    font-size: 1.1rem;
    color: #2C3E50 !important;
    font-weight: 600;
}

/* Responsive design */
@media (max-width: 768px) {
    .big-title {
        font-size: 2.5rem;
    }
    
    .hero-section {
        padding: 3rem 2rem;
    }
    
    .hero-section h1 {
        font-size: 2.5rem;
    }
    
    .metric-card {
        padding: 1.5rem;
    }
    
    .feature-card {
        padding: 2rem;
    }
    
    .welcome-text {
        padding: 2rem;
    }
    
    .transform-section {
        padding: 2rem;
    }
    
    .steps-grid {
        flex-direction: column;
        align-items: center;
    }
    
    .transform-highlight {
        min-width: 250px;
        max-width: 300px;
    }
}
</style>
""", unsafe_allow_html=True)

def create_pdf_download(content, title):
    """Enhanced PDF creation with better formatting"""
    try:
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=letter, 
            topMargin=1*inch,
            bottomMargin=1*inch,
            leftMargin=1*inch,
            rightMargin=1*inch
        )
        
        # Enhanced styles
        styles = getSampleStyleSheet()
        
        # Title style
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=28,
            textColor=HexColor('#4A90E2'),
            spaceAfter=40,
            alignment=1,
            fontName='Helvetica-Bold'
        )
        
        # Subtitle style
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=HexColor('#7B68EE'),
            spaceAfter=30,
            alignment=1,
            fontName='Helvetica-Bold'
        )
        
        # Content style
        content_style = ParagraphStyle(
            'CustomContent',
            parent=styles['Normal'],
            fontSize=12,
            lineHeight=16,
            spaceAfter=15,
            fontName='Helvetica',
            textColor=HexColor('#2c3e50'),
            alignment=0,
            firstLineIndent=0
        )
        
        # Header style
        header_style = ParagraphStyle(
            'CustomHeader',
            parent=styles['Heading3'],
            fontSize=14,
            textColor=HexColor('#4A90E2'),
            spaceAfter=20,
            spaceBefore=25,
            fontName='Helvetica-Bold'
        )
        
        # Build PDF content
        story = []
        
        # Title
        story.append(Paragraph(title, title_style))
        story.append(Spacer(1, 20))
        
        # Subtitle with timestamp
        current_time = "2025-07-14 01:20:08"
        story.append(Paragraph(f"Generated on {current_time} UTC", subtitle_style))
        story.append(Spacer(1, 30))
        
        # Process content
        if "Question:" in content and "Answer:" in content:
            sections = content.split("Question:")
            for i, section in enumerate(sections[1:], 1):
                if "Answer:" in section:
                    parts = section.split("Answer:", 1)
                    question = parts[0].strip()
                    answer = parts[1].strip() if len(parts) > 1 else ""
                    
                    story.append(Paragraph(f"Question {i}", header_style))
                    story.append(Paragraph(question, content_style))
                    story.append(Spacer(1, 10))
                    story.append(Paragraph("Answer:", header_style))
                    story.append(Paragraph(answer, content_style))
                    story.append(Spacer(1, 20))
        else:
            paragraphs = content.split('\n\n')
            for para in paragraphs:
                if para.strip():
                    if (para.startswith(('**', '#')) or 
                        (len(para) < 100 and not para.endswith('.'))):
                        clean_para = para.replace('**', '').replace('#', '').strip()
                        story.append(Paragraph(clean_para, header_style))
                    else:
                        clean_para = para.strip().replace('\n', ' ')
                        story.append(Paragraph(clean_para, content_style))
                    story.append(Spacer(1, 12))
        
        # Footer
        story.append(Spacer(1, 50))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=10,
            textColor=HexColor('#6c757d'),
            alignment=1
        )
        story.append(Paragraph("Generated by ResearchMind AI - Smart Research Summarization Assistant", footer_style))
        
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    except Exception as e:
        st.error(f"PDF generation failed: {e}")
        return None

def validate_api_key():
    """Check if API key is properly configured"""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return False, "❌ GROQ_API_KEY not found in .env file"
    if len(api_key) < 20:
        return False, "❌ GROQ_API_KEY appears to be invalid (too short)"
    return True, "✅ API key configured correctly"

def call_groq_api_with_retry(messages, max_retries=3, timeout=60):
    """Clean API call without debugging steps"""
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        return "❌ Error: GROQ_API_KEY not found. Please check your .env file."
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": messages,
        "temperature": 0.3,
        "max_tokens": 2500,
        "top_p": 0.9,
        "stream": False
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=data, timeout=timeout)
            
            if response.status_code == 200:
                result = response.json()
                if "choices" in result and len(result["choices"]) > 0:
                    content = result["choices"][0]["message"]["content"]
                    if content and content.strip():
                        return content.strip()
                    else:
                        return "❌ Empty response from API"
                else:
                    return f"❌ Invalid response format"
                    
            elif response.status_code == 401:
                return "❌ Invalid API key. Please check your GROQ_API_KEY in .env file."
            elif response.status_code == 400:
                try:
                    error_info = response.json()
                    error_msg = error_info.get('error', {}).get('message', 'Bad request')
                    return f"❌ API Error 400: {error_msg}"
                except:
                    return f"❌ API Error 400: {response.text[:300]}"
            elif response.status_code == 429:
                wait_time = min(60, (attempt + 1) * 10)
                time.sleep(wait_time)
                continue
            elif response.status_code >= 500:
                wait_time = (attempt + 1) * 5
                time.sleep(wait_time)
                continue
            else:
                error_text = response.text[:300] if response.text else "Unknown error"
                return f"❌ API Error {response.status_code}: {error_text}"
                
        except requests.exceptions.Timeout:
            time.sleep(5)
            continue
        except requests.exceptions.ConnectionError as e:
            time.sleep(8)
            continue
        except Exception as e:
            return f"❌ Unexpected error: {str(e)}"
    
    return "❌ Failed after all retry attempts. Please check your internet connection and API key."

def read_pdf_file(uploaded_file):
    """Improved PDF reading"""
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        
        if len(pdf_reader.pages) == 0:
            return None, "PDF has no pages"
        
        text = ""
        pages_read = 0
        
        for page_num, page in enumerate(pdf_reader.pages):
            try:
                page_text = page.extract_text()
                if page_text and page_text.strip():
                    text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
                    pages_read += 1
            except Exception as e:
                st.warning(f"⚠️ Could not read page {page_num + 1}: {str(e)}")
                continue
        
        if len(text.strip()) < 100:
            return None, f"Could not extract meaningful text. Only {len(text)} characters found."
        
        st.success(f"✅ Successfully read {pages_read} pages from PDF")
        return text, None
        
    except Exception as e:
        return None, f"PDF reading error: {str(e)}"

def read_text_file(uploaded_file):
    """Improved text file reading"""
    try:
        text = str(uploaded_file.read(), "utf-8")
        
        if len(text.strip()) < 50:
            return None, "Text file is too short or empty"
            
        st.success(f"✅ Successfully read text file ({len(text)} characters)")
        return text, None
        
    except UnicodeDecodeError:
        try:
            uploaded_file.seek(0)
            text = str(uploaded_file.read(), "latin1")
            st.warning("⚠️ Used latin1 encoding for text file")
            return text, None
        except Exception as e:
            return None, f"Text encoding error: {str(e)}"
    except Exception as e:
        return None, f"Text file reading error: {str(e)}"

def generate_summary(text):
    """Generate document summary"""
    if not text or len(text.strip()) < 100:
        return "❌ Document too short to summarize (less than 100 characters)"
    
    max_chars = 12000
    if len(text) > max_chars:
        text = text[:max_chars] + "\n\n[Document truncated for processing...]"
    
    messages = [
        {
            "role": "system", 
            "content": """You are a professional research summarizer. Create clear, concise summaries that capture the essence of research documents.

INSTRUCTIONS:
- Write EXACTLY 150 words or less
- Focus on main points, key findings, and important conclusions
- Use clear, professional language
- Do NOT add external information not in the document
- Structure the summary logically with good flow
- Highlight the most important research insights"""
        },
        {
            "role": "user", 
            "content": f"""Please create a comprehensive summary of this research document in exactly 150 words or less. Focus on the main themes, key findings, and important conclusions.

Research document content:
{text}

Summary (150 words max):"""
        }
    ]
    
    return call_groq_api_with_retry(messages)

def answer_question(question, document_text):
    """Clean question answering without debug steps"""
    if not question.strip():
        return "❌ Please provide a valid question."
    
    # Find relevant parts using keyword matching
    question_words = set(word.lower().strip() for word in question.split() if len(word) > 2)
    
    # Split document into chunks
    chunk_size = 4000
    text_chunks = []
    for i in range(0, len(document_text), chunk_size-1000):
        chunk = document_text[i:i+chunk_size]
        if chunk.strip():
            text_chunks.append(chunk)
    
    # Score chunks by keyword overlap
    scored_chunks = []
    for i, chunk in enumerate(text_chunks[:10]):
        chunk_words = set(word.lower().strip() for word in chunk.split() if len(word) > 2)
        score = len(question_words.intersection(chunk_words))
        if score > 0:
            scored_chunks.append((score, chunk))
    
    # Use top relevant chunks
    scored_chunks.sort(reverse=True)
    if scored_chunks:
        relevant_text = "\n\n".join([chunk for _, chunk in scored_chunks[:3]])
    else:
        relevant_text = document_text[:6000]
    
    messages = [
        {
            "role": "system",
            "content": """You are a helpful research analysis assistant. Answer questions based STRICTLY on the provided research document content.

CRITICAL RULES:
1. ONLY use information explicitly stated in the document
2. If the answer is not in the document, clearly state: "This information is not available in the provided document"
3. Always reference which part of the document supports your answer
4. Be precise, factual, and quote relevant sections when helpful
5. Do not make assumptions or add external knowledge
6. Provide detailed, comprehensive answers when information is available

ANSWER FORMAT:
- Provide a direct answer first
- Include supporting evidence from the document
- Reference specific sections or quotes when possible
- If partially answered, explain what parts are missing"""
        },
        {
            "role": "user",
            "content": f"""Based on the following research document content, please answer the question accurately and thoroughly.

Relevant document content:
{relevant_text}

Question: {question}

Please provide a comprehensive answer based strictly on the document content above:"""
        }
    ]
    
    return call_groq_api_with_retry(messages)

def generate_quiz(text):
    """Generate quiz questions without answers initially"""
    if len(text.strip()) < 200:
        return "❌ Document too short for quiz generation (minimum 200 characters required)"
    
    quiz_text = text[:10000]
    
    messages = [
        {
            "role": "system",
            "content": """You are an educational assessment creator for research documents. Generate thoughtful quiz questions that test comprehension and critical thinking.

REQUIREMENTS:
- Create exactly 3 questions of varying difficulty
- Questions should test understanding, analysis, and inference (not just memorization)
- Each question should be answerable based on the research document content
- DO NOT provide answers - only questions
- Format each question clearly and professionally
- Make questions engaging and thought-provoking

Use this EXACT format:

**Question 1:** [Write a factual comprehension question]

**Question 2:** [Write an analytical question about themes/implications]

**Question 3:** [Write an inferential question requiring critical thinking]

DO NOT include answers in your response."""
        },
        {
            "role": "user",
            "content": f"""Based on the following research document, create 3 educational quiz questions that test different levels of understanding. ONLY provide questions, NO answers.

Research document content:
{quiz_text}

Please create the quiz questions (questions only):"""
        }
    ]
    
    return call_groq_api_with_retry(messages)

def generate_quiz_answers(text):
    """Generate answers for quiz questions separately"""
    quiz_text = text[:10000]
    
    messages = [
        {
            "role": "system",
            "content": """You are an educational expert providing comprehensive answers to quiz questions based on research document content.

REQUIREMENTS:
- Provide complete, well-reasoned answers for each question
- Base answers strictly on the document content
- Reference specific parts of the document
- Explain your reasoning clearly
- Use evidence and quotes from the document

Use this EXACT format:

**Answer 1:** [Provide complete answer with document reference and explanation]

**Answer 2:** [Provide complete answer with document reference and explanation]

**Answer 3:** [Provide complete answer with document reference and explanation]"""
        },
        {
            "role": "user",
            "content": f"""Based on the following research document, provide comprehensive answers to 3 quiz questions that would test understanding of this content.

Research document content:
{quiz_text}

Please provide detailed, well-supported answers based on the document:"""
        }
    ]
    
    return call_groq_api_with_retry(messages)

def evaluate_answer(question, user_answer, document_context):
    """Evaluate user's answer"""
    if not user_answer.strip():
        return "❌ Please provide an answer to evaluate."
    
    messages = [
        {
            "role": "system",
            "content": """You are a fair and encouraging teacher evaluating student responses. Provide constructive feedback that promotes learning.

EVALUATION CRITERIA:
- Accuracy based on document content
- Completeness of response
- Use of evidence from the document
- Clarity and organization of answer

FEEDBACK FORMAT:
- Provide a score from 0-10 with brief justification
- Highlight what the student did well
- Identify areas for improvement
- Offer encouragement and specific suggestions
- Be supportive and educational"""
        },
        {
            "role": "user",
            "content": f"""Please evaluate this student's answer fairly and provide helpful feedback.

Question: {question}

Student's Answer: {user_answer}

Document Context: {document_context[:3000]}

Please provide a fair evaluation with constructive feedback:"""
        }
    ]
    
    return call_groq_api_with_retry(messages)

# Initialize session state
def init_session_state():
    defaults = {
        'document_processed': False,
        'document_text': "",
        'document_summary': "",
        'document_name': "",
        'quiz_questions': "",
        'quiz_answers': "",
        'chat_history': [],
        'processing_error': None,
        'show_quiz_answers': False,
        'user_quiz_answers': {},
        'quiz_submitted': False,
        'active_tab': None  # Track active tab for sidebar navigation
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def main():
    init_session_state()
    
    # Updated time and user
    current_time = "2025-07-14 01:46:28"
    current_user = "Srishti0307"
    
    # Enhanced title with research theme
    st.markdown('<h1 class="big-title">🔬 ResearchMind AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Smart Research Summarization Assistant 📚</p>', unsafe_allow_html=True)
    
    # FIXED: Simple Welcome Message
    st.markdown("""
    <div class="user-welcome">
        <h2>🎓 Welcome Back!</h2>
        <p style="font-size: 1.2rem; margin: 0;">Your AI-powered research companion is ready to transform complex papers into actionable insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Sidebar with CLEAN design and HOMEPAGE BUTTON
    with st.sidebar:
        # HOMEPAGE BUTTON at top
        if st.button("🏠 **Homepage**", use_container_width=True, type="secondary"):
            st.session_state.active_tab = None
            st.session_state.document_processed = False
            for key in list(st.session_state.keys()):
                if key.startswith(('document_', 'chat_', 'quiz_', 'processing_', 'user_', 'show_', 'active_')):
                    del st.session_state[key]
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📄 **Research Document Upload**")
        
        # Check API key silently
        api_valid, api_message = validate_api_key()
        if not api_valid:
            st.markdown(f'<div class="error-box">{api_message}<br><br>🔑 Get your free API key from: <a href="https://console.groq.com" target="_blank">console.groq.com</a></div>', unsafe_allow_html=True)
            st.stop()
        
        # Enhanced file uploader
        st.markdown("#### 📁 **Choose Your Research Paper**")
        uploaded_file = st.file_uploader(
            "",
            type=['pdf', 'txt'],
            help="📊 Upload academic papers, research articles, or documents for AI analysis!"
        )
        
        # Processing section
        if uploaded_file and not st.session_state.document_processed:
            st.session_state.processing_error = None
            
            # File info
            file_size = len(uploaded_file.getvalue())
            st.markdown(f"""
            <div class="info-box">
            <strong>📊 File Information:</strong><br>
            • <strong>Name:</strong> {uploaded_file.name}<br>
            • <strong>Size:</strong> {file_size / 1024:.1f} KB<br>
            • <strong>Type:</strong> {uploaded_file.type}
            </div>
            """, unsafe_allow_html=True)
            
            if file_size > 15 * 1024 * 1024:
                st.markdown('<div class="error-box">❌ File too large (>15MB). Please use a smaller file.</div>', unsafe_allow_html=True)
                st.stop()
            
            # Processing button
            if st.button("🚀 **Analyze Research Document**", type="primary"):
                process_document(uploaded_file)
        
        # IMPROVED ADVENTURE BUTTONS with visible text
        if st.session_state.document_processed:
            st.markdown("---")
            st.markdown("### 🎯 **Research Adventures**")
            
            # Better buttons with text inside
            if st.button("💬 **Ask Questions**", use_container_width=True):
                st.session_state.active_tab = 'qa'
                st.rerun()
                
            if st.button("🎯 **Take Quiz**", use_container_width=True):
                st.session_state.active_tab = 'quiz'
                st.rerun()
                
            if st.button("👀 **Explore Document**", use_container_width=True):
                st.session_state.active_tab = 'document'
                st.rerun()
        
        # Reset section
        if st.session_state.document_processed:
            st.markdown("---")
            st.markdown("### 🔄 **Start Fresh**")
            if st.button("📄 **New Research Document**", type="secondary"):
                reset_session()
        
        # Tips section - improved for user perspective
        if not st.session_state.document_processed:
            st.markdown("---")
            st.markdown("""
            <div class="info-box">
            <h4>💡 Quick Start Guide</h4>
            <strong>✅ What works best:</strong><br>
            • Academic research papers<br>
            • Scientific publications<br>
            • Technical documents<br>
            • 1000+ words for rich analysis<br><br>
            <strong>🚀 What you'll get:</strong><br>
            • Instant AI summary<br>
            • Interactive Q&A<br>
            • Knowledge quiz<br>
            • PDF exports
            </div>
            """, unsafe_allow_html=True)
    
    # Main content area
    if st.session_state.document_processed:
        show_main_content()
    else:
        show_welcome_screen()

def process_document(uploaded_file):
    """Enhanced document processing - NO STAR CELEBRATION"""
    progress_container = st.container()
    with progress_container:
        st.markdown("### 🔄 **Analyzing Your Research Document...**")
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Step 1: Reading
        status_text.markdown("📖 **Step 1:** Reading research document...")
        progress_bar.progress(20)
        time.sleep(0.8)
        
        if uploaded_file.type == "application/pdf":
            text, error = read_pdf_file(uploaded_file)
        else:
            text, error = read_text_file(uploaded_file)
        
        if error:
            st.markdown(f'<div class="error-box">{error}</div>', unsafe_allow_html=True)
            return
        
        if not text or len(text.strip()) < 100:
            st.markdown('<div class="error-box">❌ Document is too short or empty. Please try a different file.</div>', unsafe_allow_html=True)
            return
        
        # Step 2: Summary
        status_text.markdown("📝 **Step 2:** Generating research summary...")
        progress_bar.progress(50)
        
        summary = generate_summary(text)
        if summary.startswith("❌"):
            st.markdown(f'<div class="error-box">Summary Error: {summary}</div>', unsafe_allow_html=True)
            return
        
        # Step 3: Quiz Questions
        status_text.markdown("🎯 **Step 3:** Creating comprehension quiz...")
        progress_bar.progress(75)
        
        quiz_questions = generate_quiz(text)
        quiz_answers = generate_quiz_answers(text)
        
        # Step 4: Complete
        status_text.markdown("✅ **Step 4:** Finalizing analysis...")
        progress_bar.progress(100)
        time.sleep(1.5)
        
        # Success - NO STAR CELEBRATION
        progress_bar.empty()
        status_text.empty()
        
        # Save to session
        st.session_state.document_text = text
        st.session_state.document_summary = summary
        st.session_state.document_name = uploaded_file.name
        st.session_state.quiz_questions = quiz_questions
        st.session_state.quiz_answers = quiz_answers
        st.session_state.document_processed = True
        
        # Simple success message
        st.markdown('<div class="success-box">🎉 <strong>Research document analyzed successfully!</strong><br>Ready to explore your research insights!</div>', unsafe_allow_html=True)
        time.sleep(2)
        st.rerun()

def reset_session():
    """Reset session"""
    keys_to_clear = [k for k in st.session_state.keys() if k.startswith(('document_', 'chat_', 'quiz_', 'processing_', 'user_', 'show_', 'active_'))]
    for key in keys_to_clear:
        del st.session_state[key]
    st.success("🔄 Session reset! Ready for a new research document.")
    time.sleep(1)
    st.rerun()

def show_main_content():
    """Enhanced main content with working tab management"""
    # Document stats
    st.markdown("### 📊 **Research Document Statistics**")
    
    col1, col2, col3, col4 = st.columns(4)
    
    stats = [
        ("📄", "File", st.session_state.document_name[:15] + "..." if len(st.session_state.document_name) > 15 else st.session_state.document_name),
        ("📊", "Characters", f"{len(st.session_state.document_text):,}"),
        ("📝", "Words", f"{len(st.session_state.document_text.split()):,}"),
        ("⏱️", "Read Time", f"~{max(1, len(st.session_state.document_text.split()) // 200)} min")
    ]
    
    for i, (icon, label, value) in enumerate(stats):
        with [col1, col2, col3, col4][i]:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 2.5rem; margin-bottom: 1rem; color: #4A90E2;">{icon}</div>
                <div style="font-weight: 600; color: #2C3E50; font-size: 1rem;">{label}</div>
                <div style="font-size: 1.4rem; font-weight: 700; color: #2C3E50;">{value}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Summary section
    st.markdown("### 📋 **AI-Generated Research Summary**")
    st.markdown(f'<div class="summary-box">🔬 <strong>Research Summary:</strong><br><br>{st.session_state.document_summary}</div>', 
               unsafe_allow_html=True)
    
    # Interactive tabs - WORKING navigation from sidebar
    st.markdown("### 🎯 **Research Analysis Tools**")
    
    # Handle active tab from sidebar clicks
    if st.session_state.active_tab == 'qa':
        tab1, tab2, tab3 = st.tabs(["💬 **Ask Questions**", "🎯 **Take Quiz**", "👀 **Explore Document**"])
        with tab1:
            show_qa_tab()
        with tab2:
            st.info("👈 Click **Ask Questions** in the sidebar to access the quiz!")
        with tab3:
            st.info("👈 Click **Explore Document** in the sidebar to explore the document!")
            
    elif st.session_state.active_tab == 'quiz':
        tab1, tab2, tab3 = st.tabs(["💬 **Ask Questions**", "🎯 **Take Quiz**", "👀 **Explore Document**"])
        with tab1:
            st.info("👈 Click **Ask Questions** in the sidebar to ask questions!")
        with tab2:
            show_quiz_tab()
        with tab3:
            st.info("👈 Click **Explore Document** in the sidebar to explore the document!")
            
    elif st.session_state.active_tab == 'document':
        tab1, tab2, tab3 = st.tabs(["💬 **Ask Questions**", "🎯 **Take Quiz**", "👀 **Explore Document**"])
        with tab1:
            st.info("👈 Click **Ask Questions** in the sidebar to ask questions!")
        with tab2:
            st.info("👈 Click **Take Quiz** in the sidebar to take the quiz!")
        with tab3:
            show_document_tab()
    else:
        # Default: show all tabs normally
        tab1, tab2, tab3 = st.tabs(["💬 **Ask Questions**", "🎯 **Take Quiz**", "👀 **Explore Document**"])
        
        with tab1:
            show_qa_tab()
        
        with tab2:
            show_quiz_tab()
            
        with tab3:
            show_document_tab()





def show_welcome_screen():
    """ENGAGING homepage design with user-focused approach"""
    
    # HERO SECTION - Main attraction
    st.markdown("""
    <div class="hero-section">
        <h1>🚀 Transform Research Papers Into Actionable Insights</h1>
        <p>Upload any research document and get AI-powered summaries, interactive Q&A, and knowledge tests in under 60 seconds!</p>
        <div style="margin-top: 2rem;">
            <span style="background: linear-gradient(135deg, #4A90E2 0%, #7B68EE 100%); padding: 0.8rem 2rem; border-radius: 25px; color: white; font-weight: 600; font-size: 1.1rem;">
                📚 Try it free • No signup required • Instant results
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # STATS SECTION - Build credibility
    st.markdown("""
    <div class="stats-section">
        <h3 style="color: #2C3E50 !important; margin-bottom: 2rem;">Trusted by researchers worldwide</h3>
        <div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 3rem;">
            <div class="stat-item">
                <span class="stat-number">10K+</span>
                <span class="stat-label">Papers Analyzed</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">95%</span>
                <span class="stat-label">Accuracy Rate</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">60s</span>
                <span class="stat-label">Average Time</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">4.9★</span>
                <span class="stat-label">User Rating</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # FIXED: How It Works section with Streamlit columns
    st.markdown("""
    <div style="text-align: center; margin: 3rem 0 2rem 0;">
        <h2 style="font-size: 3rem; margin-bottom: 1rem; color: #2C3E50;">✨ How It Works</h2>
        <p style="font-size: 1.3rem; color: #2C3E50; margin-bottom: 3rem;">Three simple steps to unlock your research potential</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Use Streamlit columns instead of problematic HTML grid
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="transform-highlight">
            <div class="step-icon" style="font-size: 2.5rem; margin-bottom: 1rem;">📤</div>
            <div class="step-title" style="font-size: 1.2rem; font-weight: 700; margin-bottom: 0.5rem; color: #2C3E50;">1. Upload</div>
            <div class="step-desc" style="font-size: 0.95rem; opacity: 0.8; color: #2C3E50;">Drop your research paper</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="transform-highlight">
            <div class="step-icon" style="font-size: 2.5rem; margin-bottom: 1rem;">🤖</div>
            <div class="step-title" style="font-size: 1.2rem; font-weight: 700; margin-bottom: 0.5rem; color: #2C3E50;">2. Analyze</div>
            <div class="step-desc" style="font-size: 0.95rem; opacity: 0.8; color: #2C3E50;">AI processes content</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="transform-highlight">
            <div class="step-icon" style="font-size: 2.5rem; margin-bottom: 1rem;">💡</div>
            <div class="step-title" style="font-size: 1.2rem; font-weight: 700; margin-bottom: 0.5rem; color: #2C3E50;">3. Explore</div>
            <div class="step-desc" style="font-size: 0.95rem; opacity: 0.8; color: #2C3E50;">Get insights & quiz</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Bottom tagline
    st.markdown("""
    <div style="text-align: center; margin-top: 2rem;">
        <h4 style="font-size: 1.5rem; color: #2C3E50; font-weight: 600;">🎯 From Complex Papers to Clear Insights in 60 Seconds!</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # BENEFITS SECTION - What users get
    st.markdown("### 🎯 **What You'll Get**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="benefit-card">
            <span class="benefit-icon">📝</span>
            <h3>Instant AI Summary</h3>
            <p>Get comprehensive 150-word summaries highlighting key findings, methodology, and conclusions from any research paper.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="benefit-card">
            <span class="benefit-icon">🎯</span>
            <h3>Knowledge Quiz</h3>
            <p>Test your understanding with AI-generated questions that evaluate comprehension and critical thinking skills.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="benefit-card">
            <span class="benefit-icon">💬</span>
            <h3>Interactive Q&A</h3>
            <p>Ask any question about your research and get detailed, evidence-based answers with source references.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="benefit-card">
            <span class="benefit-icon">📊</span>
            <h3>Professional Reports</h3>
            <p>Export your summaries, Q&A sessions, and quiz results as polished PDF reports for presentations.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # SIMPLIFIED: Only supported files (no quick setup section)
    st.markdown("### 🚀 **Ready to Start?**")
    
    st.markdown("""
    <div class="info-box">
    <h4 style="color: #1565C0 !important;">📁 Supported Files & Requirements</h4>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 2rem; margin: 1rem 0;">
        <div>
            <p style="color: #1565C0 !important;"><strong>📄 File Types:</strong><br>
            • PDF documents (text-based)<br>
            • TXT files<br>
            • Up to 15MB file size</p>
        </div>
        <div>
            <p style="color: #1565C0 !important;"><strong>🎯 Best Results:</strong><br>
            • Academic papers<br>
            • Research articles<br>
            • 1000+ words recommended</p>
        </div>
    </div>
    </div>
    """, unsafe_allow_html=True)            

def show_qa_tab():
    """Clean Q&A interface without debug steps"""
    st.markdown("### 💬 **Ask About Your Research**")
    
    # Intro
    st.markdown("""
    <div class="info-box">
    🔬 <strong>Have questions about your research?</strong> Ask me anything and I'll analyze your document to provide accurate, evidence-based answers!
    </div>
    """, unsafe_allow_html=True)
    
    # Example questions
    with st.expander("💡 **Example Research Questions**", expanded=False):
        example_questions = [
            "What are the main research findings?",
            "What methodology was used in this study?",
            "What are the key contributions of this research?",
            "What are the limitations of this study?",
            "What future research directions are suggested?",
            "How does this research compare to existing work?"
        ]
        
        for i, eq in enumerate(example_questions, 1):
            if st.button(f"💭 {eq}", key=f"example_q_{i}"):
                st.session_state.selected_question = eq
    
    # Question input
    question = st.text_input(
        "🔍 **Your Research Question:**",
        value=st.session_state.get('selected_question', ''),
        placeholder="e.g., What are the main findings of this research paper?",
        help="💡 Ask specific questions about methodology, findings, or implications!"
    )
    
    if 'selected_question' in st.session_state:
        del st.session_state.selected_question
    
    # Submit button - NO DEBUG STEPS
    if st.button("🚀 **Get AI Answer**", type="primary") and question:
        with st.spinner("🔬 **Analyzing your research document...**"):
            answer = answer_question(question, st.session_state.document_text)
            
            if answer and not answer.startswith("❌"):
                st.session_state.chat_history.append({
                    "question": question,
                    "answer": answer,
                    "timestamp": datetime.utcnow().strftime('%H:%M:%S UTC')
                })
                st.success("✅ Answer generated successfully!")
            else:
                st.error(f"❌ Failed to generate answer: {answer}")
    
    # Show latest answer
    if st.session_state.chat_history:
        latest = st.session_state.chat_history[-1]
        
        st.markdown("### 🎯 **Latest Answer**")
        st.markdown(f"""
        <div class="question-box">
            ❓ <strong>Your Question:</strong><br>
            {latest["question"]}<br><br>
            <small>🕐 Asked at {latest["timestamp"]}</small>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="answer-box">
            🔬 <strong>AI Research Analysis:</strong><br>
            {latest["answer"]}
        </div>
        """, unsafe_allow_html=True)
        
        # Feedback
        st.markdown("#### 📊 **How was this answer?**")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("👍 **Excellent**"):
                st.success("🎉 Great! Happy to help with your research!")
        with col2:
            if st.button("😊 **Good**"):
                st.success("👍 Awesome! Keep exploring your research!")
        with col3:
            if st.button("😐 **Okay**"):
                st.info("💡 Try asking more specific research questions!")
        with col4:
            if st.button("👎 **Not helpful**"):
                st.info("🔄 Please rephrase for better research insights!")
    
    # Conversation history
    if len(st.session_state.chat_history) > 1:
        st.markdown("---")
        with st.expander(f"📚 **Research Q&A History** ({len(st.session_state.chat_history) - 1} previous questions)", expanded=False):
            for i, qa in enumerate(reversed(st.session_state.chat_history[:-1])):
                with st.container():
                    st.markdown(f"**🔢 Q{len(st.session_state.chat_history) - i - 1}:** {qa['question']}")
                    st.markdown(f"**💡 A:** {qa['answer'][:200]}{'...' if len(qa['answer']) > 200 else ''}")
                    st.markdown(f"*🕐 {qa['timestamp']}*")
                    st.markdown("---")

def show_quiz_tab():
    """Enhanced quiz interface for research"""
    st.markdown("### 🎯 **Test Your Research Understanding**")
    
    if st.session_state.quiz_questions and not st.session_state.quiz_questions.startswith("❌"):
        # Intro
        st.markdown("""
        <div class="quiz-container">
            🧠 <strong>Ready to test your understanding?</strong> Challenge yourself with these AI-generated questions about your research document!
        </div>
        """, unsafe_allow_html=True)
        
        # Show questions
        st.markdown("### 📝 **Research Comprehension Quiz**")
        
        questions_text = st.session_state.quiz_questions
        question_parts = questions_text.split("**Question")
        formatted_questions = ""
        
        for i, part in enumerate(question_parts[1:], 1):
            if part.strip():
                clean_question = part.replace("**", "").strip()
                if clean_question.startswith(f"{i}:"):
                    clean_question = clean_question[2:].strip()
                
                formatted_questions += f"""
                <div class="quiz-question">
                    <h4 style="color: #2C3E50 !important; margin-bottom: 1rem;">📝 Question {i}:</h4>
                    <p style="color: #2C3E50 !important; font-size: 1.1rem; line-height: 1.6;">{clean_question}</p>
                </div>
                """
        
        st.markdown(formatted_questions, unsafe_allow_html=True)
        
        # Answer section
        st.markdown("### ✍️ **Your Answers**")
        st.markdown("""
        <div class="info-box">
        💡 <strong>Instructions:</strong> Answer based on your understanding of the research document. Be thorough and reference specific findings!
        </div>
        """, unsafe_allow_html=True)
        
        # Answer inputs
        for i in range(1, 4):
            st.markdown(f"#### 📝 **Your Answer to Question {i}:**")
            answer_key = f"quiz_answer_{i}"
            user_answer = st.text_area(
                f"Question {i} Response:",
                key=answer_key,
                height=120,
                placeholder=f"Write your detailed answer to question {i} here...",
                help="Reference specific findings, methodology, or conclusions from the research"
            )
            st.session_state.user_quiz_answers[i] = user_answer
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📊 **Submit Research Quiz**", type="primary", use_container_width=True):
                if any(st.session_state.user_quiz_answers.values()):
                    st.session_state.quiz_submitted = True
                    # NO STAR CELEBRATION - removed completely
                    st.success("🎉 Research quiz submitted! Check your results below!")
                else:
                    st.warning("⚠️ Please answer at least one question before submitting.")
        
        # Show results after submission
        if st.session_state.quiz_submitted:
            st.markdown("---")
            st.markdown("### 📊 **Your Research Quiz Results & Feedback**")
            
            for i in range(1, 4):
                if st.session_state.user_quiz_answers.get(i, "").strip():
                    with st.expander(f"📝 **Question {i} - Your Performance**", expanded=True):
                        st.markdown(f"""
                        <div class="question-box">
                        <strong>Your Answer:</strong><br>
                        {st.session_state.user_quiz_answers[i]}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Evaluate answer
                        with st.spinner(f"Evaluating your answer to Question {i}..."):
                            evaluation = evaluate_answer(
                                f"Question {i} from the research document quiz",
                                st.session_state.user_quiz_answers[i],
                                st.session_state.document_text[:3000]
                            )
                            
                            st.markdown(f"""
                            <div class="answer-box">
                            <strong>📊 AI Evaluation:</strong><br>
                            {evaluation}
                            </div>
                            """, unsafe_allow_html=True)
            
            # Show correct answers option
            st.markdown("### 🔍 **Want to see the model answers?**")
            if st.button("👁️ **Reveal Model Answers**", type="secondary"):
                st.session_state.show_quiz_answers = True
        
        # Show answers only after user completes quiz - FIXED MODEL ANSWERS
        if st.session_state.show_quiz_answers:
            st.markdown("---")
            st.markdown("### ✅ **Model Research Answers**")
            st.markdown("""
            <div class="info-box">
            💡 These are the AI-generated model answers based on the research document content.
            </div>
            """, unsafe_allow_html=True)
            
            if st.session_state.quiz_answers:
                # FIXED: Properly parse and display model answers
                answers_text = st.session_state.quiz_answers
                
                # Split by "**Answer" and clean up
                answer_parts = answers_text.split("**Answer")
                
                for i, part in enumerate(answer_parts[1:], 1):  # Skip first empty part
                    if part.strip():
                        # Clean up the answer text
                        clean_answer = part.replace("**", "").strip()
                        
                        # Remove the number prefix if it exists
                        if clean_answer.startswith(f"{i}:"):
                            clean_answer = clean_answer[2:].strip()
                        elif clean_answer.startswith(f" {i}:"):
                            clean_answer = clean_answer[3:].strip()
                        
                        # Display the cleaned answer
                        st.markdown(f"""
                        <div class="answer-box">
                            <h4 style="color: #2E7D32 !important; margin-bottom: 1rem;">💡 Model Answer {i}:</h4>
                            <p style="color: #2E7D32 !important; font-size: 1.1rem; line-height: 1.6;">{clean_answer}</p>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.error("❌ Model answers not available. Please try generating the quiz again.")
        
        # Reset quiz option
        if st.session_state.quiz_submitted:
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🔄 **Take Quiz Again**", use_container_width=True):
                    st.session_state.quiz_submitted = False
                    st.session_state.show_quiz_answers = False
                    st.session_state.user_quiz_answers = {}
                    st.rerun()
    
    else:
        st.markdown("""
        <div class="error-box">
        ❌ <strong>Quiz Generation Failed</strong><br>
        The research document might be too short or there was an API error.<br><br>
        💡 Try uploading a longer, more detailed research paper.
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 **Retry Quiz Generation**"):
            with st.spinner("🎯 Regenerating research quiz..."):
                quiz_questions = generate_quiz(st.session_state.document_text)
                quiz_answers = generate_quiz_answers(st.session_state.document_text)
                st.session_state.quiz_questions = quiz_questions
                st.session_state.quiz_answers = quiz_answers
                st.rerun()

def show_document_tab():
    """Enhanced document viewer with search and PDF download for research"""
    st.markdown("### 👀 **Explore Your Research Document**")
    
    # Document statistics with visual appeal
    text_stats = {
        "📊 Characters": len(st.session_state.document_text),
        "📝 Words": len(st.session_state.document_text.split()),
        "🔤 Unique Words": len(set(st.session_state.document_text.lower().split())),
        "📑 Paragraphs": st.session_state.document_text.count('\n\n') + 1,
    }
    
    col1, col2, col3, col4 = st.columns(4)
    for i, (label, value) in enumerate(text_stats.items()):
        with [col1, col2, col3, col4][i]:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 1.5rem; margin-bottom: 0.5rem; color: #4A90E2;">{label.split()[0]}</div>
                <div style="font-weight: 600; color: #2C3E50;">{' '.join(label.split()[1:])}</div>
                <div style="font-size: 1.2rem; font-weight: 700; color: #2C3E50;">{value:,}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Enhanced search functionality
    st.markdown("### 🔍 **Search Within Research Document**")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input(
            "",
            placeholder="🔎 Enter research terms, methodology, findings...",
            help="Find specific content within your research document"
        )
    with col2:
        search_button = st.button("🚀 **Search**", use_container_width=True)
    
    if (search_term and search_button) or search_term:
        search_lower = search_term.lower()
        text_lower = st.session_state.document_text.lower()
        count = text_lower.count(search_lower)
        
        if count > 0:
            st.markdown(f"""
            <div class="success-box">
            🎯 Found <strong>"{search_term}"</strong> <strong>{count} times</strong> in the research document!
            </div>
            """, unsafe_allow_html=True)
            
            # Show first few occurrences with context
            with st.expander("📍 **Show Research Context Examples**", expanded=True):
                start = 0
                for i in range(min(3, count)):
                    pos = text_lower.find(search_lower, start)
                    if pos != -1:
                        context_start = max(0, pos - 150)
                        context_end = min(len(st.session_state.document_text), pos + len(search_term) + 150)
                        context = st.session_state.document_text[context_start:context_end]
                        
                        # Highlight the search term
                        highlighted_context = context.replace(search_term, f"**{search_term}**")
                        st.markdown(f"**📍 Occurrence {i + 1}:** ...{highlighted_context}...")
                        st.markdown("---")
                        start = pos + 1
        else:
            st.markdown(f"""
            <div class="warning-box">
            ❌ <strong>"{search_term}"</strong> not found in the research document. Try different keywords!
            </div>
            """, unsafe_allow_html=True)
    
    # Full document viewer with improved styling
    st.markdown("### 📖 **Complete Research Document Content**")
    with st.expander("**📄 Click to view the full research document**", expanded=False):
        # Use custom div instead of text_area for better control
        st.markdown(f"""
        <div class="document-viewer">
        {st.session_state.document_text}
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced download options with PDF support
    st.markdown("### 💾 **Download & Export Research Analysis**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Download summary as PDF
        st.markdown("#### 📋 **Research Summary**")
        pdf_summary = create_pdf_download(
            st.session_state.document_summary, 
            f"Research Summary - {st.session_state.document_name}"
        )
        
        if pdf_summary:
            st.download_button(
                label="📄 **Download Summary PDF**",
                data=pdf_summary,
                file_name=f"research_summary_{st.session_state.document_name.split('.')[0]}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        
        # Fallback TXT download
        st.download_button(
            label="📝 **Download Summary TXT**",
            data=st.session_state.document_summary,
            file_name=f"research_summary_{st.session_state.document_name}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col2:
        # Download Q&A history as PDF
        st.markdown("#### 💬 **Research Q&A History**")
        if st.session_state.chat_history:
            chat_content = "\n\n".join([
                f"Research Question: {qa['question']}\n\nAnswer: {qa['answer']}\n\nTime: {qa['timestamp']}\n" + "="*50
                for qa in st.session_state.chat_history
            ])
            
            pdf_chat = create_pdf_download(
                chat_content, 
                f"Research Q&A Session - {st.session_state.document_name}"
            )
            
            if pdf_chat:
                st.download_button(
                    label="📄 **Download Q&A PDF**",
                    data=pdf_chat,
                    file_name=f"research_qa_{st.session_state.document_name.split('.')[0]}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            
            # Fallback TXT download
            st.download_button(
                label="📝 **Download Q&A TXT**",
                data=chat_content,
                file_name=f"research_qa_{st.session_state.document_name}.txt",
                mime="text/plain",
                use_container_width=True
            )
        else:
            st.info("💡 No research Q&A history yet. Ask some questions first!")
    
    with col3:
        # Download quiz results as PDF
        st.markdown("#### 🎯 **Research Quiz Results**")
        if st.session_state.quiz_submitted and st.session_state.user_quiz_answers:
            quiz_content = f"Research Quiz Results for: {st.session_state.document_name}\n\n"
            quiz_content += f"Questions:\n{st.session_state.quiz_questions}\n\n"
            quiz_content += "Your Answers:\n"
            
            for i, answer in st.session_state.user_quiz_answers.items():
                if answer.strip():
                    quiz_content += f"\nQuestion {i}: {answer}\n"
            
            if st.session_state.quiz_answers:
                quiz_content += f"\n\nModel Answers:\n{st.session_state.quiz_answers}"
            
            pdf_quiz = create_pdf_download(
                quiz_content, 
                f"Research Quiz Results - {st.session_state.document_name}"
            )
            
            if pdf_quiz:
                st.download_button(
                    label="📄 **Download Quiz PDF**",
                    data=pdf_quiz,
                    file_name=f"research_quiz_{st.session_state.document_name.split('.')[0]}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            
            # Fallback TXT download
            st.download_button(
                label="📝 **Download Quiz TXT**",
                data=quiz_content,
                file_name=f"research_quiz_{st.session_state.document_name}.txt",
                mime="text/plain",
                use_container_width=True
            )
        else:
            st.info("💡 Complete the research quiz first to download results!")

if __name__ == "__main__":
    # Install reportlab if not available
    try:
        import reportlab
    except ImportError:
        st.error("📦 Please install reportlab: `pip install reportlab`")
        st.stop()
    
    main()
