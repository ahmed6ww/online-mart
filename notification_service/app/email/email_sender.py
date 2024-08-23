# app/email/email_sender.py
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from app.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_USERNAME, EMAIL_PASSWORD, EMAIL_FROM

def send_order_confirmation_email(to_email: str, subject: str, body: str):
    # Set up the email message
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        # Set up the SMTP server connection
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.sendmail(EMAIL_FROM, to_email, msg.as_string())
            print(f"Email sent successfully to {to_email}!")
    except Exception as e:
        print(f"Failed to send email: {e}")
