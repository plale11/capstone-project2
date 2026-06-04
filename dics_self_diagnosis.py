import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(
    page_title="DICS Self-Diagnosis System",
    layout="centered"
)

records_file = "screening_records.csv"

record_columns = [
    "time", "student_name", "grade", "gender",
    "health_score", "lifestyle_score", "top_condition", "top_score",
    "sleep_hours", "screen_time_hours", "study_hours",
    "exercise_minutes", "stress_level"
]


def initialize_records_file():
    if not os.path.exists(records_file):
        pd.DataFrame(columns=record_columns).to_csv(
            records_file,
            index=False,
            encoding="utf-8-sig"
        )
    else:
        records = pd.read_csv(records_file)
        records = records.reindex(columns=record_columns)
        records.to_csv(records_file, index=False, encoding="utf-8-sig")


def get_level(score):
    if score >= 80:
        return "Good"
    if score >= 60:
        return "Moderate"
    return "Needs Improvement"


def calculate_lifestyle_scores(
    sleep_hours,
    screen_time_hours,
    study_hours,
    exercise_minutes,
    stress_level
):
    if sleep_hours >= 8:
        sleep_score = 25
    elif sleep_hours >= 7:
        sleep_score = 22
    elif sleep_hours >= 6:
        sleep_score = 16
    elif sleep_hours >= 5:
        sleep_score = 10
    else:
        sleep_score = 5

    if screen_time_hours <= 2:
        screen_score = 20
    elif screen_time_hours <= 4:
        screen_score = 16
    elif screen_time_hours <= 6:
        screen_score = 10
    else:
        screen_score = 5

    if exercise_minutes >= 60:
        exercise_score = 20
    elif exercise_minutes >= 30:
        exercise_score = 16
    elif exercise_minutes >= 10:
        exercise_score = 10
    else:
        exercise_score = 5

    if stress_level <= 3:
        stress_score = 20
    elif stress_level <= 6:
        stress_score = 14
    elif stress_level <= 8:
        stress_score = 8
    else:
        stress_score = 4

    if 2 <= study_hours <= 5:
        study_score = 15
    elif 5 < study_hours <= 8:
        study_score = 11
    elif study_hours > 8:
        study_score = 7
    elif 1 <= study_hours < 2:
        study_score = 10
    else:
        study_score = 6

    lifestyle_score = (
        sleep_score + screen_score + exercise_score + stress_score + study_score
    )

    category_scores = {
        "Sleep": sleep_score,
        "Screen Time": screen_score,
        "Exercise": exercise_score,
        "Stress": stress_score,
        "Study Balance": study_score
    }

    return lifestyle_score, category_scores


def build_lifestyle_feedback(
    sleep_hours,
    screen_time_hours,
    study_hours,
    exercise_minutes,
    stress_level
):
    feedback = []
    goals = []

    if sleep_hours < 6:
        feedback.append(
            "Sleep: Your sleep time is low. Try sleeping 30 minutes earlier this week."
        )
        goals.append("Sleep 30 minutes earlier than usual tonight.")
    elif sleep_hours < 7:
        feedback.append(
            "Sleep: Your sleep time is slightly low. A more regular sleep schedule may help your concentration."
        )
        goals.append("Keep a fixed bedtime and wake-up time today.")
    else:
        feedback.append("Sleep: Your sleep time looks relatively stable.")

    if screen_time_hours > 6:
        feedback.append(
            "Screen Time: Your screen time is high. Reducing phone use before sleep may help rest and focus."
        )
        goals.append("Avoid phone use for 30 minutes before sleeping.")
    elif screen_time_hours > 4:
        feedback.append(
            "Screen Time: Your screen time is moderate to high. Try adding short screen-free breaks."
        )
        goals.append("Take one 20-minute screen-free break today.")
    else:
        feedback.append("Screen Time: Your screen time is within a balanced range.")

    if exercise_minutes < 10:
        feedback.append(
            "Exercise: Your activity level is low. Even a short walk can support energy and mood."
        )
        goals.append("Take a 10-minute walk or stretch today.")
    elif exercise_minutes < 30:
        feedback.append(
            "Exercise: You had some movement today. Try to gradually increase it."
        )
        goals.append("Add 10 more minutes of light activity tomorrow.")
    else:
        feedback.append("Exercise: Your physical activity looks good today.")

    if stress_level >= 8:
        feedback.append(
            "Stress: Your stress level is high. Take breaks and consider talking to a trusted adult or school staff."
        )
        goals.append("Do one 5-minute breathing break between study sessions.")
    elif stress_level >= 6:
        feedback.append(
            "Stress: Your stress level is moderate. Short breaks and planning may help."
        )
        goals.append("Plan one short rest period after studying.")
    else:
        feedback.append("Stress: Your stress level looks manageable today.")

    if study_hours > 8:
        feedback.append(
            "Study Balance: Your study time is very high. Long study time without rest can reduce efficiency."
        )
        goals.append("Use a 5-minute break after each focused study session.")
    elif study_hours < 1:
        feedback.append(
            "Study Balance: Your study time is low today. Try setting a small, realistic study goal."
        )
        goals.append("Complete one focused 25-minute study session.")
    else:
        feedback.append("Study Balance: Your study time looks reasonably balanced.")

    if not goals:
        goals.append("Maintain your current healthy routine tomorrow.")

    return feedback, goals[:3]


initialize_records_file()

st.title("DICS Self-Diagnosis System")
st.write("Health screening application for DICS students.")

st.warning(
    "This app is for educational health screening only. "
    "It does not provide medical diagnosis or prescription."
)

st.markdown("---")

if "form_key" not in st.session_state:
    st.session_state.form_key = 0

if "form_locked" not in st.session_state:
    st.session_state.form_locked = False

 form_disabled = st.session_state.form_locked

with st.form(f"diagnosis_form_{st.session_state.form_key}"):
   student_name = st.text_input(
    "Student Name",
    disabled=form_disabled
)

    grade = st.selectbox(
        "Grade",
        [
            "Select grade", "Grade 1", "Grade 2", "Grade 3", "Grade 4",
            "Grade 5", "Grade 6", "Grade 7", "Grade 8", "Grade 9",
            "Grade 10", "Grade 11", "Grade 12"
        ]
    )

    gender = st.radio("Gender", ["Male", "Female", "Other"])

    st.subheader("Basic Health Information")

    height_cm = st.number_input(
        "Height (cm)",
        min_value=100.0,
        max_value=220.0,
        value=170.0,
        step=1.0
    )

    weight_kg = st.number_input(
        "Weight (kg)",
        min_value=30.0,
        max_value=150.0,
        value=60.0,
        step=1.0
    )

    st.subheader("Lifestyle & Daily Habit Information")

    sleep_hours = st.slider(
        "Sleep Time Last Night (hours)",
        0,
        12,
        7
    )

    screen_time_hours = st.slider(
        "Screen Time Today (hours)",
        0,
        16,
        4
    )

    study_hours = st.slider(
        "Study Time Today (hours)",
        0,
        12,
        3
    )

    exercise_minutes = st.slider(
        "Exercise Time Today (minutes)",
        0,
        180,
        30,
        step=5
    )

    stress_level = st.slider(
        "Stress Level",
        1,
        10,
        5
    )

    st.subheader("Select Your Symptoms")

    fever = st.checkbox("Fever")
    cough = st.checkbox("Cough")
    sore_throat = st.checkbox("Sore throat")
    runny_nose = st.checkbox("Runny nose")
    headache = st.checkbox("Headache")
    muscle_pain = st.checkbox("Muscle pain")
    fatigue = st.checkbox("Fatigue")
    shortness_breath = st.checkbox("Shortness of breath")
    vomiting = st.checkbox("Vomiting")
    diarrhea = st.checkbox("Diarrhea")

    submitted = st.form_submit_button("Analyze Health & Lifestyle")

if submitted:
    if student_name == "" or grade == "Select grade":
        st.error("Please enter your name and grade first.")

    else:
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
            "COVID-19-like Symptoms": covid_score,
            "Allergic Rhinitis": allergy_score,
            "Stomach Flu / Gastroenteritis": stomach_flu_score
        }

        sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
        top_disease, top_score = sorted_results[0]

        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)

        if bmi < 18.5:
            bmi_category = "Underweight"
        elif bmi < 25:
            bmi_category = "Healthy Weight"
        elif bmi < 30:
            bmi_category = "Overweight"
        else:
            bmi_category = "Obesity Range"

        lifestyle_score, category_scores = calculate_lifestyle_scores(
            sleep_hours,
            screen_time_hours,
            study_hours,
            exercise_minutes,
            stress_level
        )

        lifestyle_feedback, today_goals = build_lifestyle_feedback(
            sleep_hours,
            screen_time_hours,
            study_hours,
            exercise_minutes,
            stress_level
        )

        symptom_health_score = 100
        symptom_health_score -= top_score * 0.4

        if bmi_category != "Healthy Weight":
            symptom_health_score -= 10

        if shortness_breath:
            symptom_health_score -= 20

        symptom_health_score = max(0, min(100, int(symptom_health_score)))
        health_score = int((symptom_health_score * 0.6) + (lifestyle_score * 0.4))
        health_score = max(0, min(100, health_score))

        new_record = pd.DataFrame([{
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "student_name": student_name,
            "grade": grade,
            "gender": gender,
            "health_score": health_score,
            "lifestyle_score": lifestyle_score,
            "top_condition": top_disease,
            "top_score": top_score,
            "sleep_hours": sleep_hours,
            "screen_time_hours": screen_time_hours,
            "study_hours": study_hours,
            "exercise_minutes": exercise_minutes,
            "stress_level": stress_level
        }])

        records = pd.read_csv(records_file)
        records = pd.concat([records, new_record], ignore_index=True)
        records = records.reindex(columns=record_columns)
        records.to_csv(records_file, index=False, encoding="utf-8-sig")

        st.markdown("---")
        st.subheader(f"{student_name}'s Screening Result")

        st.write("Grade:", grade)
        st.write("Gender:", gender)

        st.subheader("Overall Result")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Overall Health Score", f"{health_score}/100")
        with col2:
            st.metric("Lifestyle Score", f"{lifestyle_score}/100")
        with col3:
            st.metric("Symptom Risk", f"{top_score}%")

        st.progress(health_score / 100)

        if health_score >= 80:
            st.success(f"{health_score}/100 - Good Condition")
        elif health_score >= 60:
            st.warning(f"{health_score}/100 - Moderate Risk")
        else:
            st.error(f"{health_score}/100 - High Risk")

        st.write(f"BMI: {bmi:.1f}")
        st.write(f"BMI Category: {bmi_category}")

        st.subheader("Lifestyle Category Scores")

        chart_df = pd.DataFrame({
            "Category": list(category_scores.keys()),
            "Score": list(category_scores.values())
        }).set_index("Category")

        st.bar_chart(chart_df)

        c1, c2 = st.columns(2)
        with c1:
            st.write(f"Sleep: {sleep_hours} hours")
            st.write(f"Screen Time: {screen_time_hours} hours")
            st.write(f"Study Time: {study_hours} hours")
        with c2:
            st.write(f"Exercise Time: {exercise_minutes} minutes")
            st.write(f"Stress Level: {stress_level}/10")
            st.write(f"Lifestyle Level: {get_level(lifestyle_score)}")

        st.subheader("Lifestyle Feedback")
        for item in lifestyle_feedback:
            st.write("- " + item)

        st.subheader("Today's Improvement Goals")
        for goal in today_goals:
            st.write("✅ " + goal)

        st.subheader("Disease Possibility")

        if top_score >= 70:
            st.error(f"Most likely condition: {top_disease}: {top_score}%")
        elif top_score >= 40:
            st.warning(f"Most likely condition: {top_disease}: {top_score}%")
        else:
            st.info(f"Most likely condition: {top_disease}: {top_score}%")

        st.write("Other possibilities:")
        for disease, score in sorted_results[1:]:
            st.write(f"{disease}: {score}%")

        st.subheader("Health Feedback")

        if health_score >= 80:
            st.success("Your overall condition appears stable based on the information you entered.")
        elif health_score >= 60:
            st.warning("Some risk factors were detected. Monitor your symptoms, rest well, and stay hydrated.")
        else:
            st.error("Several risk factors were detected. Please consider visiting the school nurse or a healthcare professional.")

        if bmi_category == "Underweight":
            st.info("Your BMI is below the general healthy range. Regular meals and balanced nutrition may be helpful.")
        elif bmi_category == "Overweight":
            st.info("Your BMI is above the general healthy range. Regular physical activity and balanced eating habits may help.")
        elif bmi_category == "Obesity Range":
            st.warning("Your BMI is in a higher range. This is not a diagnosis, but professional health guidance may be helpful.")

        if shortness_breath:
            st.error("Shortness of breath can be a serious warning sign. Please visit the school nurse or seek medical help immediately.")

        st.subheader("Symptom-Based Suggestions")

        if fever:
            st.write("- Fever: Drink plenty of water, rest, and monitor your temperature. If fever is high or lasts more than 2 days, visit the school nurse or a doctor.")

        if cough:
            st.write("- Cough: Drink warm fluids, avoid cold drinks, and wear a mask to reduce spreading infection.")

        if sore_throat:
            st.write("- Sore throat: Warm water gargling and voice rest may help. If pain is severe, seek medical advice.")

        if runny_nose:
            st.write("- Runny nose: It may be related to a cold or allergy. Avoid dust and stay hydrated.")

        if headache:
            st.write("- Headache: Rest in a quiet place, drink water, and reduce screen time.")

        if muscle_pain:
            st.write("- Muscle pain: Avoid intense physical activity and rest until symptoms improve.")

        if fatigue:
            st.write("- Fatigue: Sleep, hydration, and balanced meals are important for recovery.")

        if vomiting:
            st.write("- Vomiting: Drink small amounts of water frequently. Avoid heavy meals until symptoms improve.")

        if diarrhea:
            st.write("- Diarrhea: Hydration is very important. Avoid greasy food and dairy products temporarily.")

        if not any([
            fever, cough, sore_throat, runny_nose, headache,
            muscle_pain, fatigue, shortness_breath, vomiting, diarrhea
        ]):
            st.info("No major symptoms were selected. Continue maintaining healthy habits and monitor your condition.")

        st.caption(
            "This result is not a medical diagnosis. "
            "Please consult a healthcare professional for accurate diagnosis and treatment."
        )

st.markdown("---")

if st.button("New Student"):
    st.session_state.form_key += 1
    st.rerun()

st.markdown("---")
st.subheader("Screening Records")

records = pd.read_csv(records_file)
records = records.reindex(columns=record_columns)

if records.empty:
    st.info("No students have been screened yet.")
else:
    for index, row in records.iterrows():
        col1, col2 = st.columns([4, 1])

        with col1:
            lifestyle_display = row.get("lifestyle_score", "N/A")
            st.write(
                f"{row['time']} | {row['student_name']} | "
                f"{row['grade']} | Health: {row['health_score']} | "
                f"Lifestyle: {lifestyle_display} | "
                f"{row['top_condition']} ({row['top_score']}%)"
            )

        with col2:
            if st.button("Delete", key=f"delete_{index}"):
                records = records.drop(index)
                records.to_csv(records_file, index=False, encoding="utf-8-sig")
                st.rerun()

if st.button("Clear All Screening Records"):
    pd.DataFrame(columns=record_columns).to_csv(
        records_file,
        index=False,
        encoding="utf-8-sig"
    )

    st.success("All screening records cleared.")
    st.rerun()
