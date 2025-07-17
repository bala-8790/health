import streamlit as st
import pandas as pd
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load disease info
with open("disease_info.json", "r") as f:
    disease_info = json.load(f)

# Define the symptoms
symptoms = [
    "fever", "cough", "fatigue", "headache", "joint pain", "rash", "vomiting", "diarrhea",
    "weight loss", "night sweats", "sore throat", "chills", "skin lesions", "blurred vision",
    "abdominal pain", "shortness of breath", "blood in stool", "nausea", "hair loss", "swollen lymph nodes"
]

# Dummy function to simulate prediction (replace this with real model logic)
def predict_disease(input_df):
    # You can implement your ML logic here
    # For example: rule-based, threshold-based, or a manually coded model
    # Example: If fever, cough, and fatigue, then flu
    symptoms_present = input_df.iloc[0].to_dict()
    if symptoms_present["fever"] and symptoms_present["cough"] and symptoms_present["fatigue"]:
        return "Flu"
    elif symptoms_present["rash"] and symptoms_present["joint pain"]:
        return "Dengue"
    else:
        return "Unknown"

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
        # Encode symptoms as binary
        input_data = [1 if sym in selected_symptoms else 0 for sym in symptoms]
        input_df = pd.DataFrame([input_data], columns=symptoms)

        # Predict using dummy function
        prediction = predict_disease(input_df)
        st.success(f"✅ Predicted Disease: **{prediction}**")

        # Show additional info
        if prediction in disease_info:
            st.markdown(f"**🧪 Cause:** {disease_info[prediction]['cause']}")
            st.markdown(f"**🥗 Diet Plan:** {disease_info[prediction]['diet']}")
            st.markdown(f"**💊 Recommendations:** {disease_info[prediction]['recommendation']}")
        else:
            st.warning("ℹ️ Additional info not available for this disease.")

        # Hospitals
        st.markdown("### 🏥 Recommended Hospitals")
        hospitals = [
            {"name": "Apollo Hospitals", "city": "Hyderabad", "contact": "040-23232323"},
            {"name": "AIIMS", "city": "Delhi", "contact": "011-26588500"},
            {"name": "Fortis Health", "city": "Mumbai", "contact": "022-45678900"},
        ]
        for h in hospitals:
            st.markdown(f"- **{h['name']}**, {h['city']} - 📞 {h['contact']}")

        # Email sending
        if email:
            try:
                sender = "your_email@example.com"
                sender_pass = "your_app_password"

                message = MIMEMultipart()
                message["From"] = sender
                message["To"] = email
                message["Subject"] = f"Health Report for {name}"

                body = f"""Hello {name},

Based on your symptoms, the predicted disease is: {prediction}.

Cause: {disease_info.get(prediction, {}).get("cause", "Not available")}
Diet Plan: {disease_info.get(prediction, {}).get("diet", "Not available")}
Recommendations: {disease_info.get(prediction, {}).get("recommendation", "Not available")}

Regards,
Health AI System
"""
                message.attach(MIMEText(body, "plain"))

                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                    server.starttls()
                    server.login(sender, sender_pass)
                    server.send_message(message)

                st.success(f"📩 Report sent to {email}")
            except Exception as e:
                st.error(f"❌ Failed to send email: {e}")
