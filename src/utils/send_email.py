import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()


def send_email(to_address: str, subject: str, body: str):
    from_address = os.getenv("ADMIN_EMAIL")
    password = os.getenv("ADMIN_EMAIL_PASSWORD")

    msg = MIMEMultipart()
    msg["From"] = from_address
    msg["To"] = to_address
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(from_address, password)
    server.send_message(msg)
    server.quit()
