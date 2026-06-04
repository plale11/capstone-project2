import streamlit as st
import pandas as pd
import cv2
from datetime import datetime
import os
from PIL import Image
import numpy as np

st.title("Smart Study Attendance System")

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

uploaded_file = st.file_uploader("Upload QR image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
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
                st.warning(f"{name} 학생은 이미 오늘 출석 처리되었습니다.")
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

                st.success(f"{name} 학생 인증 성공!")
                st.write("학생번호:", student_id)
                st.write("출석 시간:", check_in_time)
                st.write("출석 상태:", status)

        else:
            st.error("등록되지 않은 학생입니다.")
    else:
        st.error("QR 코드를 인식할 수 없습니다.")

st.subheader("Attendance Records")

if os.path.exists(attendance_file):
    data = pd.read_csv(attendance_file)
    st.dataframe(data)