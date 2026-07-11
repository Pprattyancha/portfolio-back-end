import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

ADMIN_EMAIL = "prattyancha009@gmail.com"


def send_email(user_email, message, name="User"):
    try:
        if not EMAIL_USER or not EMAIL_PASS:
            raise Exception("Email credentials missing")

        # Connect once
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)

        # =========================
        # 1️⃣ Email to YOU (Admin)
        # =========================
        admin_msg = MIMEText(f"""
        <h2>📩 New Contact Form Submission</h2>
        <p><b>Name:</b> {name}</p>
        <p><b>Email:</b> {user_email}</p>
        <p><b>Message:</b></p>
        <p>{message}</p>
        """, "html")

        admin_msg["Subject"] = "New Contact Form Message 🚀"
        admin_msg["From"] = EMAIL_USER
        admin_msg["To"] = ADMIN_EMAIL

        server.send_message(admin_msg)

        # =========================
        # 2️⃣ Auto-reply to USER
        # =========================
        user_msg = MIMEText(f"""
        <h3>Hi {name}, 👋</h3>

        <p>Thank you for reaching out!</p>

        <p>We have received your message and will get back to you shortly.</p>

        <br/>
        <p><b>Your Message:</b></p>
        <p>{message}</p>

        <br/>
        <p>Best regards,<br/>Prattyancha</p>
        """, "html")

        user_msg["Subject"] = "Thanks for contacting us 🙌"
        user_msg["From"] = EMAIL_USER
        user_msg["To"] = user_email

        server.send_message(user_msg)

        # Close connection
        server.quit()

        print("Both emails sent successfully ✅")
        return True

    except Exception as e:
        print("Email error:", e)
        raise Exception(f"Email failed: {str(e)}")