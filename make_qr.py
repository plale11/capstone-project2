import qrcode
import pandas as pd
import os

students = pd.read_csv("students.csv")
students["student_id"] = students["student_id"].astype(str)

os.makedirs("qr_codes", exist_ok=True)

for _, row in students.iterrows():
    student_id = row["student_id"]

    qr = qrcode.make(student_id)
    qr.save(f"qr_codes/{student_id}.png")

print("QR codes created!")