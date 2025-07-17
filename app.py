import streamlit as st
import pandas as pd
import json
import smtplib
import base64
from io import BytesIO
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Load disease info
with open("disease_info.json", "r") as f:
    disease_info = json.load(f)

# Dummy model prediction function (replace with real logic if needed)
def predict_disease(input_df):
    # Just a placeholder: predict based on first positive symptom
    symptom_to_disease = {
        "fever": "Typhoid",
        "cough": "Flu",
        "fatigue": "Anemia",
        "headache": "Migraine",
        "joint pain": "Arthritis"
    }
    for symptom in input_df.columns:
        if input_df[symptom].iloc[0] == 1 and symptom in symptom_to_disease:
            return symptom_to_disease[symptom]
    return "Unknown Disease"

# Symptom list
symptoms = [
    "fever", "cough", "fatigue", "headache", "joint pain", "rash", "vomiting", "diarrhea",
    "weight loss", "night sweats", "sore throat", "chills", "skin lesions", "blurred vision",
    "abdominal pain", "shortness of breath", "blood in stool", "nausea", "hair loss", "swollen lymph nodes"
]

# Streamlit UI
st.set_page_config(page_title="AI Disease Prediction", layout="wide")
st.title("🩺 AI-Powered Disease Prediction App")

st.markdown("### 🧾 Enter your details")
name = st.text_input("Name")
age = st.number_input("Age", min_value=1, max_value=120, step=1)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
email = st.text_input("Enter your email to get the report")

st.markdown("### 🤒 Select your symptoms")
selected_symptoms = st.multiselect("Choose the symptoms you're experiencing:", symptoms)

if st.button("Predict Disease"):
    if len(selected_symptoms) < 3:
        st.warning("Please select at least 3 symptoms.")
    else:
        # Prepare input
        input_data = [1 if sym in selected_symptoms else 0 for sym in symptoms]
        input_df = pd.DataFrame([input_data], columns=symptoms)

        # Prediction
        prediction = predict_disease(input_df)
        st.success(f"✅ Predicted Disease: **{prediction}**")

        # Extra Info
        cause = disease_info.get(prediction, {}).get("cause", "Not available")
        diet = disease_info.get(prediction, {}).get("diet", "Not available")
        recommendation = disease_info.get(prediction, {}).get("recommendation", "Not available")

        st.markdown(f"**🧪 Cause:** {cause}")
        st.markdown(f"**🥗 Diet Plan:** {diet}")
        st.markdown(f"**💊 Recommendations:** {recommendation}")

        # Hospitals
        st.markdown("### 🏥 Recommended Hospitals")
        hospitals = [
            {"name": "Apollo Hospitals", "city": "Hyderabad", "contact": "040-23232323"},
            {"name": "AIIMS", "city": "Delhi", "contact": "011-26588500"},
            {"name": "Fortis Health", "city": "Mumbai", "contact": "022-45678900"},
        ]
        for h in hospitals:
            st.markdown(f"- **{h['name']}**, {h['city']} - 📞 {h['contact']}")

        # Report Content
        report_text = f"""Health Report for {name}

Predicted Disease: {prediction}

Cause: {cause}
Diet Plan: {diet}
Recommendations: {recommendation}

Selected Symptoms: {', '.join(selected_symptoms)}
Age: {age}, Gender: {gender}

Regards,
Health AI System
"""

        # Download Report
        buffer = BytesIO()
        buffer.write(report_text.encode())
        buffer.seek(0)
        b64 = base64.b64encode(buffer.read()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="health_report.txt">📄 Download Health Report</a>'
        st.markdown(href, unsafe_allow_html=True)

        # Send email
        if email:
            try:
                sender = "your_email@example.com"
                sender_pass = "your_app_password"  # Use App Password

                message = MIMEMultipart()
                message["From"] = sender
                message["To"] = email
                message["Subject"] = f"Health Report for {name}"

                message.attach(MIMEText(report_text, "plain"))
                attachment = MIMEApplication(report_text.encode(), Name="health_report.txt")
                attachment['Content-Disposition'] = 'attachment; filename="health_report.txt"'
                message.attach(attachment)

                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                    server.starttls()
                    server.login(sender, sender_pass)
                    server.send_message(message)

                st.success(f"📩 Report sent to {email}")
            except Exception as e:
                st.error("❌ Failed to send email. Please check credentials or enable Gmail App Password.")
