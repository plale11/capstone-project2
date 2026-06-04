import streamlit as st
import pandas as pd
import cv2
from datetime import datetime
import os
from PIL import Image
import numpy as np

# Page config with dark theme
st.set_page_config(
    page_title="Smart Study Attendance System",
    page_icon="🎓",
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
        
        /* Input fields glassmorphism */
        .stFileUploader {
            background: rgba(20, 27, 58, 0.4) !important;
            border: 1px solid rgba(124, 58, 237, 0.25) !important;
            border-radius: 16px !important;
            backdrop-filter: blur(12px) !important;
            transition: all 0.3s ease !important;
        }
        
        .stFileUploader:hover {
            background: rgba(20, 27, 58, 0.5) !important;
            border: 1px solid rgba(124, 58, 237, 0.4) !important;
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
        
        /* Data frame styling */
        [data-testid="stDataFrame"] {
            background: rgba(20, 27, 58, 0.4) !important;
            border-radius: 16px !important;
            backdrop-filter: blur(12px) !important;
            box-shadow: 0 8px 32px rgba(124, 58, 237, 0.1) !important;
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
        
        /* Metric styling */
        [data-testid="metric-container"] {
            background: rgba(20, 27, 58, 0.4) !important;
            border: 1px solid rgba(124, 58, 237, 0.25) !important;
            border-radius: 16px !important;
            backdrop-filter: blur(12px) !important;
            box-shadow: 0 8px 32px rgba(124, 58, 237, 0.1) !important;
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
        <h1 style="text-align: center; margin: 0;">🎓 Smart Study Attendance System</h1>
        <p style="text-align: center; color: rgba(232, 232, 255, 0.7); margin: 10px 0 0 0;">
            QR Code-Based Attendance Management
        </p>
    </div>
""", unsafe_allow_html=True)

students = pd.read_csv("students.csv")
students["student_id"] = students["student_id"].astype(str)

attendance_file = "attendance.csv"

if not os.path.exists(attendance_file):
    pd.DataFrame(columns=[
        "date", "student_id", "name", "check_in_time", "status"
    ]).to_csv(attendance_file, index=False, encoding="utf-8-sig")

def get_status(now):
    deadline = now.replace(hour=18, minute=25, second=0, microsecond=0)

    if now <= deadline:
        return "출석 인정"
    else:
        return "지각"

# QR Code Upload Section
st.markdown("""
    <div style="margin-top: 40px; margin-bottom: 20px;">
        <h2 style="color: #e8e8ff; text-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);">📱 QR Code Recognition</h2>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload QR image", type=["png", "jpg", "jpeg"])
    st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file is not None:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    
    image = Image.open(uploaded_file)
    img = np.array(image)

    detector = cv2.QRCodeDetector()
    student_id, points, _ = detector.detectAndDecode(img)

    if student_id:
        student = students[students["student_id"] == student_id]

        if not student.empty:
            name = student.iloc[0]["name"]
            now = datetime.now()
            today = now.strftime("%Y-%m-%d")
            check_in_time = now.strftime("%H:%M:%S")
            status = get_status(now)

            attendance = pd.read_csv(attendance_file)

            already_checked = (
                (attendance["date"] == today) &
                (attendance["student_id"].astype(str) == student_id)
            ).any()

            if already_checked:
                st.warning(f"⚠️ {name} 학생은 이미 오늘 출석 처리되었습니다.")
            else:
                new_record = pd.DataFrame([{
                    "date": today,
                    "student_id": student_id,
                    "name": name,
                    "check_in_time": check_in_time,
                    "status": status
                }])

                new_record.to_csv(
                    attendance_file,
                    mode="a",
                    header=False,
                    index=False,
                    encoding="utf-8-sig"
                )

                st.success(f"✅ {name} 학생 인증 성공!")
                
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("학생번호", student_id)
                with col_b:
                    st.metric("출석 시간", check_in_time)
                with col_c:
                    st.metric("상태", status)

        else:
            st.error("❌ 등록되지 않은 학생입니다.")
    else:
        st.error("❌ QR 코드를 인식할 수 없습니다.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Attendance Records Section
st.markdown("""
    <div style="margin-top: 50px;">
        <h2 style="color: #e8e8ff; text-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);">📊 Attendance Records</h2>
    </div>
""", unsafe_allow_html=True)

st.markdown('<div class="glass-container">', unsafe_allow_html=True)

if os.path.exists(attendance_file):
    data = pd.read_csv(attendance_file)
    
    if not data.empty:
        # Display statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Records", len(data))
        with col2:
            on_time = len(data[data["status"] == "출석 인정"])
            st.metric("On Time", on_time)
        with col3:
            late = len(data[data["status"] == "지각"])
            st.metric("Late", late)
        with col4:
            unique_students = data["student_id"].nunique()
            st.metric("Unique Students", unique_students)
        
        st.divider()
        st.dataframe(data, use_container_width=True, hide_index=True)
    else:
        st.info("📭 No attendance records yet.")
else:
    st.info("📭 Attendance file not found. It will be created upon first use.")

st.markdown('</div>', unsafe_allow_html=True)