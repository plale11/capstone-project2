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

# Custom CSS for glassmorphism effect
st.markdown("""
    <style>
        /* Dark background */
        :root {
            --primary-dark: #0f0f23;
            --secondary-dark: #1a1a3e;
            --accent-purple: #667eea;
            --accent-blue: #4c63d2;
        }
        
        /* Main page background */
        .stApp {
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 100%);
        }
        
        /* Glassmorphism containers */
        .glass-container {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
            transition: all 0.3s ease;
            margin-bottom: 20px;
        }
        
        .glass-container:hover {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.15);
            box-shadow: 0 12px 40px rgba(102, 126, 234, 0.2);
        }
        
        /* Title styling */
        .title-glass {
            background: rgba(102, 126, 234, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(102, 126, 234, 0.2);
            border-radius: 20px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(102, 126, 234, 0.1);
            text-align: center;
        }
        
        /* Checkbox styling */
        .stCheckbox {
            background: rgba(255, 255, 255, 0.03) !important;
        }
        
        /* Input fields glassmorphism */
        .stTextInput {
            background: rgba(255, 255, 255, 0.03) !important;
        }
        
        /* Buttons glassmorphism */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #4c63d2 100%);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            padding: 12px 24px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            width: 100%;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }
        
        /* Success, warning, error messages */
        .stSuccess {
            background: rgba(34, 197, 94, 0.1);
            border: 1px solid rgba(34, 197, 94, 0.3);
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }
        
        .stWarning {
            background: rgba(234, 179, 8, 0.1);
            border: 1px solid rgba(234, 179, 8, 0.3);
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }
        
        .stError {
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.3);
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }
        
        .stInfo {
            background: rgba(59, 130, 246, 0.1);
            border: 1px solid rgba(59, 130, 246, 0.3);
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }
        
        /* Heading styling */
        h1, h2, h3 {
            color: #e8e8ff;
            text-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
        }
        
        /* Result boxes */
        .result-glass {
            background: rgba(102, 126, 234, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(102, 126, 234, 0.3);
            border-radius: 12px;
            padding: 20px;
            margin: 10px 0;
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