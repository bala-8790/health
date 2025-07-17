import smtplib
from email.message import EmailMessage
from fpdf import FPDF
import os

def generate_pdf_report(name, age, gender, email, symptoms, prediction, cause, diet, recommendation):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Health Report", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
    pdf.cell(200, 10, txt=f"Age: {age}", ln=True)
    pdf.cell(200, 10, txt=f"Gender: {gender}", ln=True)
    pdf.cell(200, 10, txt=f"Email: {email}", ln=True)
    pdf.ln(5)
    pdf.multi_cell(0, 10, txt=f"Symptoms: {', '.join(symptoms)}")
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Predicted Disease: {prediction}", ln=True)
    pdf.multi_cell(0, 10, txt=f"Cause: {cause}")
    pdf.multi_cell(0, 10, txt=f"Diet: {diet}")
    pdf.multi_cell(0, 10, txt=f"Recommendation: {recommendation}")

    file_path = f"health_report_{name.replace(' ', '_')}.pdf"
    pdf.output(file_path)

    return file_path


def send_email_with_report(receiver_email, subject, body, attachment_path):
    sender_email = "jonnabalamahendravarma@gmail.com"
    password = "Ammanana@8790"

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content(body)

    # Attach the PDF
    with open(attachment_path, "rb") as f:
        file_data = f.read()
        file_name = os.path.basename(attachment_path)

    msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)

    # Send email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.send_message(msg)
