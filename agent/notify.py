import smtplib
from email.mime.text import MIMEText

EMAIL_TO = "din@epost.no"
EMAIL_FROM = "agent@github"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_notification(title, summary, link):
    body = f"{title}\n\n{summary}\n\n{link}"
    msg = MIMEText(body)
    msg["Subject"] = f"Ny episode: {title}"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    print("Varsel sendt:")
    print(body)
