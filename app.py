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
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(102, 126, 234, 0.1);
        }
        
        /* Input fields glassmorphism */
        .stFileUploader {
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
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
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }
        
        /* Data frame styling */
        [data-testid="stDataFrame"] {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            backdrop-filter: blur(10px);
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