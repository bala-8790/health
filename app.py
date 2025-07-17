import streamlit as st
import pandas as pd
import json
from disease_model import predict_disease
from utils import send_email_with_report, generate_pdf_report

# Load disease and hospital data
with open("disease_info.json", "r") as f:
    disease_info = json.load(f)

with open("hospital_info.json", "r") as f:
    hospital_info = json.load(f)

# Symptom list
symptoms = [
    "fever", "cough", "fatigue", "headache", "joint pain", "rash", "vomiting", "diarrhea",
    "weight loss", "night sweats", "sore throat", "chills", "skin lesions", "blurred vision",
    "abdominal pain", "shortness of breath", "blood in stool", "nausea", "hair loss", "swollen lymph nodes"
]

# Streamlit UI
st.set_page_config(page_title="AI Disease Predictor", layout="wide")
st.title("🩺 AI Disease Prediction App")

# User input
st.markdown("### 🔍 Enter Your Information")
name = st.text_input("Name")
age = st.number_input("Age", min_value=1, max_value=120, step=1)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
email = st.text_input("Email (for report)")

st.markdown("### 🤒 Select Your Symptoms")
selected_symptoms = st.multiselect("Choose symptoms:", symptoms)

if st.button("🔮 Predict Disease"):
    if len(selected_symptoms) < 3:
        st.warning("Please select at least 3 symptoms.")
    else:
        input_data = [1 if s in selected_symptoms else 0 for s in symptoms]
        input_df = pd.DataFrame([input_data], columns=symptoms)

        # Predict
        prediction = predict_disease(input_df)

        st.success(f"✅ Predicted Disease: **{prediction}**")

        # Disease Info
        disease = disease_info.get(prediction, {})
        st.markdown(f"**🧪 Cause:** {disease.get('cause', 'Not available')}")
        st.markdown(f"**🥗 Diet Plan:** {disease.get('diet', 'Not available')}")
        st.markdown(f"**💊 Recommendations:** {disease.get('recommendation', 'Not available')}")

        # Hospitals
        st.markdown("### 🏥 Recommended Hospitals")
        for hospital in hospital_info:
            st.markdown(f"- **{hospital['name']}**, {hospital['city']} - 📞 {hospital['contact']}")

        # Generate Report
        report_path = generate_pdf_report(name, age, gender, selected_symptoms, prediction, disease)

        # Download report
        with open(report_path, "rb") as file:
            st.download_button("📄 Download Report", file, file_name="health_report.pdf")

        # Email
        if email:
            try:
                send_email_with_report(email, name, report_path)
                st.success(f"📧 Report sent to {email}")
            except Exception as e:
                st.error(f"❌ Failed to send email: {e}")
