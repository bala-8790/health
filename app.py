import streamlit as st
import json
from disease_model import predict_disease
from utils import send_email

# Load data
with open("disease_info.json") as f:
    disease_info = json.load(f)

with open("hospital_info.json") as f:
    hospital_info = json.load(f)

st.set_page_config(page_title="Disease Predictor App", layout="centered")

st.title("🩺 Disease Prediction App")

name = st.text_input("Your Name")
age = st.number_input("Your Age", 1, 100)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
email = st.text_input("Your Email")

st.subheader("🩹 Select Your Symptoms")
symptoms = st.multiselect("Choose your symptoms:", [
    "Fever", "Cough", "Fatigue", "Weight Loss", "Headache", "Rash", 
    "Sweating", "Joint Pain", "Chest Pain", "Blood in Cough", "Vomiting"
])

if st.button("🔍 Predict Disease"):
    if symptoms:
        diseases = predict_disease(symptoms)
        st.success(f"Top 3 possible diseases for you:")
        for dis in diseases:
            if dis in disease_info:
    st.markdown(f"**Cause:** {disease_info[dis]['cause']}")
    st.markdown(f"**Diet Plan:** {disease_info[dis]['diet']}")
    st.markdown(f"**Recommendations:** {disease_info[dis]['recommendation']}")
else:
    st.warning("Details for this disease are not available yet.")

            st.markdown(f"**Cause:** {disease_info[dis]['cause']}")
            st.markdown(f"**Diet Plan:** {disease_info[dis]['diet']}")
            st.markdown(f"**Precautions:** {disease_info[dis]['precaution']}")
            st.markdown(f"**Recommended Hospitals:**")
            for h in hospital_info[dis]:
                st.markdown(f"- {h}")

        full_report = f"""
        Name: {name}
        Age: {age}
        Gender: {gender}
        Symptoms: {', '.join(symptoms)}
        Predicted Diseases: {', '.join(diseases)}
        """

        if email:
            send_email(email, "Your Health Report", full_report)
            st.success("✅ Report sent to your email!")
    else:
        st.warning("Please select at least one symptom.")
