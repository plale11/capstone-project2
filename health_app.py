import streamlit as st

# Page config with dark theme
st.set_page_config(
    page_title="Symptom-Based Health Screening App",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
    theme={
        "primaryColor": "#667eea",
        "backgroundColor": "#0f0f23",
        "secondaryBackgroundColor": "#1a1a3e",
        "textColor": "#e8e8ff",
        "font": "sans serif"
    }
)

# Custom CSS for premium glassmorphism effect
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Dark background with premium gradient */
        :root {
            --primary-dark: #0a0e27;
            --secondary-dark: #141b3a;
            --accent-purple: #7c3aed;
            --accent-blue: #3b82f6;
            --accent-cyan: #06b6d4;
            --accent-pink: #ec4899;
        }
        
        /* Main page background with animated gradient */
        .stApp {
            background: linear-gradient(135deg, #0a0e27 0%, #141b3a 25%, #1a0f3a 50%, #0a1f3a 75%, #0a0e27 100%);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* Premium glassmorphism containers */
        .glass-container {
            background: rgba(20, 27, 58, 0.4);
            backdrop-filter: blur(16px) saturate(150%);
            border: 1px solid rgba(124, 58, 237, 0.25);
            border-radius: 20px;
            padding: 28px;
            box-shadow: 0 8px 48px rgba(124, 58, 237, 0.12), 
                        inset 0 1px 1px rgba(255, 255, 255, 0.08);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            margin-bottom: 20px;
            position: relative;
            overflow: hidden;
        }
        
        .glass-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            transition: left 0.5s;
        }
        
        .glass-container:hover::before {
            left: 100%;
        }
        
        .glass-container:hover {
            background: rgba(20, 27, 58, 0.5);
            border: 1px solid rgba(124, 58, 237, 0.4);
            box-shadow: 0 12px 60px rgba(124, 58, 237, 0.25),
                        inset 0 1px 1px rgba(255, 255, 255, 0.12);
            transform: translateY(-4px);
        }
        
        /* Premium title styling */
        .title-glass {
            background: rgba(20, 27, 58, 0.5);
            backdrop-filter: blur(20px) saturate(180%);
            border: 1.5px solid rgba(124, 58, 237, 0.4);
            border-radius: 25px;
            padding: 50px;
            margin-bottom: 30px;
            box-shadow: 0 12px 60px rgba(124, 58, 237, 0.15),
                        inset 0 1px 2px rgba(255, 255, 255, 0.1);
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .title-glass::after {
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(124, 58, 237, 0.1) 0%, transparent 70%);
            animation: glow 6s ease-in-out infinite;
            z-index: -1;
        }
        
        @keyframes glow {
            0%, 100% { transform: translate(0, 0); }
            50% { transform: translate(20px, 20px); }
        }
        
        /* Checkbox styling */
        .stCheckbox {
            background: rgba(255, 255, 255, 0.05) !important;
            border-radius: 8px !important;
            padding: 8px !important;
            transition: all 0.3s ease !important;
        }
        
        .stCheckbox:hover {
            background: rgba(124, 58, 237, 0.1) !important;
        }
        
        /* Input fields glassmorphism */
        .stTextInput input {
            background: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(124, 58, 237, 0.2) !important;
            border-radius: 12px !important;
            transition: all 0.3s ease !important;
        }
        
        .stTextInput input:focus {
            background: rgba(255, 255, 255, 0.08) !important;
            border: 1px solid rgba(124, 58, 237, 0.5) !important;
            box-shadow: 0 0 20px rgba(124, 58, 237, 0.3) !important;
        }
        
        /* Premium buttons */
        .stButton > button {
            background: linear-gradient(135deg, #7c3aed 0%, #3b82f6 50%, #06b6d4 100%);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.25);
            border-radius: 14px;
            padding: 14px 32px;
            font-weight: 600;
            letter-spacing: 0.5px;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 8px 24px rgba(124, 58, 237, 0.35),
                        inset 0 1px 2px rgba(255, 255, 255, 0.2);
            width: 100%;
            position: relative;
            overflow: hidden;
        }
        
        .stButton > button::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }
        
        .stButton > button:hover::before {
            width: 300px;
            height: 300px;
        }
        
        .stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 32px rgba(124, 58, 237, 0.5),
                        inset 0 1px 2px rgba(255, 255, 255, 0.3);
            background: linear-gradient(135deg, #8b5cf6 0%, #4c9aff 50%, #06d6d4 100%);
        }
        
        .stButton > button:active {
            transform: translateY(-1px);
        }
        
        /* Success, warning, error messages */
        .stSuccess {
            background: rgba(34, 197, 94, 0.12);
            border: 1.5px solid rgba(34, 197, 94, 0.4);
            border-radius: 14px;
            backdrop-filter: blur(12px);
            padding: 16px;
        }
        
        .stWarning {
            background: rgba(234, 179, 8, 0.12);
            border: 1.5px solid rgba(234, 179, 8, 0.4);
            border-radius: 14px;
            backdrop-filter: blur(12px);
            padding: 16px;
        }
        
        .stError {
            background: rgba(239, 68, 68, 0.12);
            border: 1.5px solid rgba(239, 68, 68, 0.4);
            border-radius: 14px;
            backdrop-filter: blur(12px);
            padding: 16px;
        }
        
        .stInfo {
            background: rgba(59, 130, 246, 0.12);
            border: 1.5px solid rgba(59, 130, 246, 0.4);
            border-radius: 14px;
            backdrop-filter: blur(12px);
            padding: 16px;
        }
        
        /* Premium heading styling */
        h1, h2, h3 {
            color: #f0f9ff;
            text-shadow: 0 2px 20px rgba(124, 58, 237, 0.25);
            font-weight: 700;
            letter-spacing: -0.5px;
        }
        
        h1 {
            background: linear-gradient(135deg, #ffffff 0%, #e0e7ff 50%, #a78bfa 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: none;
            font-size: 2.5em;
        }
        
        h2 {
            background: linear-gradient(135deg, #e0e7ff 0%, #a78bfa 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 1.8em;
        }
        
        /* Premium result boxes */
        .result-glass {
            background: rgba(20, 27, 58, 0.45);
            backdrop-filter: blur(16px) saturate(150%);
            border: 1.5px solid rgba(124, 58, 237, 0.35);
            border-radius: 18px;
            padding: 28px;
            margin: 15px 0;
            box-shadow: 0 8px 40px rgba(124, 58, 237, 0.12),
                        inset 0 1px 1px rgba(255, 255, 255, 0.08);
            transition: all 0.3s ease;
        }
        
        .result-glass:hover {
            border: 1.5px solid rgba(124, 58, 237, 0.5);
            box-shadow: 0 12px 50px rgba(124, 58, 237, 0.2),
                        inset 0 1px 1px rgba(255, 255, 255, 0.12);
            transform: translateY(-2px);
        }
        
        /* Smooth transitions for all elements */
        * {
            transition: background-color 0.3s ease, border-color 0.3s ease;
        }
    </style>
""", unsafe_allow_html=True)

# Main title
st.markdown("""
    <div class="title-glass">
        <h1 style="margin: 0;">🏥 Symptom-Based Health Screening App</h1>
        <p style="color: rgba(232, 232, 255, 0.7); margin: 10px 0 0 0;">
            AI-Powered Health Assessment Tool
        </p>
    </div>
""", unsafe_allow_html=True)

# Warning message
st.markdown("""
    <div class="glass-container" style="background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3);">
        <p style="margin: 0; color: rgba(232, 232, 255, 0.8);">
            ⚠️ <strong>Disclaimer:</strong> This app is for educational screening only. 
            It does not provide medical diagnosis or prescription. 
            Please consult a healthcare professional for proper medical advice.
        </p>
    </div>
""", unsafe_allow_html=True)

# Patient information section
st.markdown("""
    <div style="margin-top: 30px;">
        <h2 style="color: #e8e8ff; text-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);">👤 Patient Information</h2>
    </div>
""", unsafe_allow_html=True)

st.markdown('<div class="glass-container">', unsafe_allow_html=True)
name = st.text_input("Enter Patient Name", placeholder="John Doe")
st.markdown('</div>', unsafe_allow_html=True)

# Symptoms selection section
st.markdown("""
    <div style="margin-top: 30px;">
        <h2 style="color: #e8e8ff; text-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);">🔍 Select Symptoms</h2>
    </div>
""", unsafe_allow_html=True)

st.markdown('<div class="glass-container">', unsafe_allow_html=True)

# Organize checkboxes in columns
col1, col2, col3 = st.columns(3)

with col1:
    fever = st.checkbox("🌡️ Fever")
    cough = st.checkbox("🤧 Cough")
    sore_throat = st.checkbox("😰 Sore throat")
    runny_nose = st.checkbox("👃 Runny nose")

with col2:
    headache = st.checkbox("🤕 Headache")
    muscle_pain = st.checkbox("💪 Muscle pain")
    fatigue = st.checkbox("😴 Fatigue")
    shortness_breath = st.checkbox("😵 Shortness of breath")

with col3:
    vomiting = st.checkbox("🤮 Vomiting")
    diarrhea = st.checkbox("🚽 Diarrhea")

st.markdown('</div>', unsafe_allow_html=True)

# Analysis button
if st.button("🔬 Analyze Symptoms", key="analyze_btn"):
    
    cold_score = 0
    flu_score = 0
    covid_score = 0
    allergy_score = 0
    stomach_flu_score = 0

    if fever:
        flu_score += 25
        covid_score += 20
        stomach_flu_score += 10

    if cough:
        cold_score += 25
        flu_score += 15
        covid_score += 20

    if sore_throat:
        cold_score += 20
        flu_score += 10
        covid_score += 10

    if runny_nose:
        cold_score += 25
        allergy_score += 30

    if headache:
        flu_score += 15
        covid_score += 10

    if muscle_pain:
        flu_score += 25
        covid_score += 10

    if fatigue:
        flu_score += 20
        covid_score += 15
        stomach_flu_score += 10

    if shortness_breath:
        covid_score += 30

    if vomiting:
        stomach_flu_score += 35

    if diarrhea:
        stomach_flu_score += 35

    results = {
        "Common Cold": cold_score,
        "Flu": flu_score,
        "COVID-19-like symptoms": covid_score,
        "Allergic Rhinitis": allergy_score,
        "Stomach Flu / Gastroenteritis": stomach_flu_score
    }

    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)

    # Results section
    st.markdown("""
        <div style="margin-top: 40px;">
            <h2 style="color: #e8e8ff; text-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);">📋 Screening Result</h2>
        </div>
    """, unsafe_allow_html=True)

    if name:
        st.markdown(f'<p style="font-size: 18px; color: #e8e8ff; text-align: center;"><strong>{name}</strong>\'s Health Assessment</p>', 
                   unsafe_allow_html=True)

    top_disease, top_score = sorted_results[0]

    # Top result
    st.markdown(f"""
        <div class="result-glass" style="background: rgba(102, 126, 234, 0.15); border: 2px solid rgba(102, 126, 234, 0.4);">
            <h3 style="color: #667eea; margin: 0 0 10px 0;">🎯 Most Likely Condition</h3>
            <p style="font-size: 24px; color: #22c55e; margin: 0; font-weight: bold;">{top_disease}: {top_score}%</p>
        </div>
    """, unsafe_allow_html=True)

    # Other possibilities
    st.markdown(f"""
        <div class="result-glass">
            <h3 style="color: #a78bfa; margin: 0 0 15px 0;">📊 Other Possibilities</h3>
    """, unsafe_allow_html=True)
    
    for disease, score in sorted_results[1:]:
        st.markdown(f"""
            <p style="color: rgba(232, 232, 255, 0.8); margin: 8px 0;">
                <strong>{disease}:</strong> <span style="color: #60a5fa;">{score}%</span>
            </p>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Recommendations section
    st.markdown("""
        <div style="margin-top: 30px;">
            <h2 style="color: #e8e8ff; text-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);">💊 Recommended Action</h2>
        </div>
    """, unsafe_allow_html=True)

    if shortness_breath or top_score >= 70:
        st.error("🚨 Medical attention is recommended, especially if symptoms are severe or worsening. Please seek professional medical care immediately.")
    elif fever or muscle_pain or fatigue:
        st.warning("⚠️ Rest, hydration, and symptom monitoring are recommended. If symptoms worsen, consult a healthcare professional.")
    else:
        st.info("ℹ️ Symptoms appear mild. Continue monitoring your condition. If symptoms persist or worsen, please consult a doctor.")

    st.caption("This result is not a medical diagnosis. Please consult a healthcare professional for accurate diagnosis and treatment.")

st.markdown("---")

if st.button("New Patient"):
    st.rerun()