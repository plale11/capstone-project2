import cv2
import pandas as pd
from datetime import datetime
import os
import time

# 학생 명단 불러오기
students = pd.read_csv("students.csv")
students["student_id"] = students["student_id"].astype(str)

attendance_file = "attendance.csv"

# 출석 기록 파일 없으면 생성
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

today = datetime.now().strftime("%Y-%m-%d")

attendance = pd.read_csv(attendance_file)
scanned_today = set(
    attendance[attendance["date"] == today]["student_id"].astype(str)
)

cap = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

last_message = ""
last_message_time = 0

print("SMART ATTENDANCE SYSTEM STARTED")
print("Press q to quit")

while True:
    success, frame = cap.read()

    if not success:
        print("카메라를 찾을 수 없습니다.")
        break

    student_id, points, _ = detector.detectAndDecode(frame)

    if student_id:
        now = datetime.now()
        check_in_time = now.strftime("%H:%M:%S")

        if student_id in scanned_today:
            last_message = "Already checked today"
            last_message_time = time.time()
            print("이미 오늘 출석 처리된 학생입니다.")

        else:
            student = students[students["student_id"] == student_id]

            if student.empty:
                last_message = "Unknown QR code"
                last_message_time = time.time()
                print("등록되지 않은 QR 코드입니다.")

            else:
                name = student.iloc[0]["name"]
                status = get_status(now)

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

                scanned_today.add(student_id)

                print("=" * 40)
                print(f"{name} 학생 인증 성공!")
                print(f"출석 시간: {check_in_time}")
                print(f"출석 상태: {status}")
                print("=" * 40)

                # 웹캠 화면에 띄울 메시지
                last_message = f"{name} authentication success | {status} | {check_in_time}"
                last_message_time = time.time()

    # 최근 3초 동안 화면에 메시지 표시
    if time.time() - last_message_time < 3:
        cv2.rectangle(frame, (30, 30), (610, 120), (0, 0, 0), -1)
        cv2.putText(frame, last_message, (50, 85),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow("QR Attendance Scanner", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()