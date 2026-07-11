import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

ADMIN_EMAIL = "prattyancha009@gmail.com"


def send_email(user_email: str, message: str, name: str = "User"):
    try:
        # ✅ Check env variables
        if not EMAIL_USER or not EMAIL_PASS:
            raise Exception("Email credentials missing in environment variables")

        print("📧 Starting email service...")
        print("Using EMAIL_USER:", EMAIL_USER)

        # ✅ Connect to Gmail SMTP
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=15)
        server.set_debuglevel(1)  # 🔥 shows logs in Render
        server.starttls()

        # ✅ Login (App Password required)
        server.login(EMAIL_USER, EMAIL_PASS)
        print("✅ SMTP login successful")

        # =========================
        # 1️⃣ Email to ADMIN (YOU)
        # =========================
        admin_html = f"""
        <h2>📩 New Contact Form Submission</h2>
        <p><b>Name:</b> {name}</p>
        <p><b>Email:</b> {user_email}</p>
        <p><b>Message:</b></p>
        <p>{message}</p>
        """

        admin_msg = MIMEText(admin_html, "html")
        admin_msg["Subject"] = "🚀 New Contact Message"
        admin_msg["From"] = EMAIL_USER
        admin_msg["To"] = ADMIN_EMAIL

        server.send_message(admin_msg)
        print("✅ Admin email sent")

        # =========================
        # 2️⃣ Auto-reply to USER
        # =========================
        user_html = f"""
        <h3>Hi {name}, 👋</h3>

        <p>Thanks for reaching out!</p>
        <p>We received your message and will get back to you soon.</p>

        <br/>
        <p><b>Your Message:</b></p>
        <p>{message}</p>

        <br/>
        <p>Best regards,<br/>Prattyancha</p>
        """

        user_msg = MIMEText(user_html, "html")
        user_msg["Subject"] = "🙌 Thanks for contacting us"
        user_msg["From"] = EMAIL_USER
        user_msg["To"] = user_email

        server.send_message(user_msg)
        print("✅ User auto-reply sent")

        # ✅ Close connection
        server.quit()
        print("🎉 All emails sent successfully")

        return True

    except smtplib.SMTPAuthenticationError:
        print("❌ SMTP Authentication Failed")
        raise Exception("Invalid EMAIL_USER or EMAIL_PASS (use App Password)")

    except smtplib.SMTPException as e:
        print("❌ SMTP Error:", str(e))
        raise Exception(f"SMTP error: {str(e)}")

    except Exception as e:
        print("❌ General Email Error:", str(e))
        raise Exception(f"Email failed: {str(e)}")