import smtplib
from email.mime.text import MIMEText
from .config import EMAIL_ADDRESS, EMAIL_PASSWORD, RECIPIENT_ADDRESS, MAIL_SUBJECT

def send_mail(body_text: str) -> None:
    msg = MIMEText(body_text, 'plain', 'utf-8')
    msg["Subject"] = MAIL_SUBJECT
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = RECIPIENT_ADDRESS

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
