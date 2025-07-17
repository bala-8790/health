import smtplib
from email.message import EmailMessage

def send_email(receiver_email, subject, content):
    sender_email = "jonnabalamahendravarma@gmail.com"
    password = "Ammanana@8790"

    msg = EmailMessage()
    msg.set_content(content)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.send_message(msg)
