# import os
# import smtplib
# from email.mime.text import MIMEText
# from dotenv import load_dotenv

# load_dotenv()

# EMAIL_USER = os.getenv("EMAIL_USER")
# EMAIL_PASS = os.getenv("EMAIL_PASS")

# ADMIN_EMAIL = "prattyancha009@gmail.com"


# def send_email(user_email: str, message: str, name: str = "User"):
#     try:
#         # ✅ Check env variables
#         if not EMAIL_USER or not EMAIL_PASS:
#             raise Exception("Email credentials missing in environment variables")

#         print("📧 Starting email service...")
#         print("Using EMAIL_USER:", EMAIL_USER)

#         # ✅ Connect to Gmail SMTP
#         server = smtplib.SMTP("smtp.gmail.com", 587, timeout=15)
#         server.set_debuglevel(1)  # 🔥 shows logs in Render
#         server.starttls()

#         # ✅ Login (App Password required)
#         server.login(EMAIL_USER, EMAIL_PASS)
#         print("✅ SMTP login successful")

#         # =========================
#         # 1️⃣ Email to ADMIN (YOU)
#         # =========================
#         admin_html = f"""
#         <h2>📩 New Contact Form Submission</h2>
#         <p><b>Name:</b> {name}</p>
#         <p><b>Email:</b> {user_email}</p>
#         <p><b>Message:</b></p>
#         <p>{message}</p>
#         """

#         admin_msg = MIMEText(admin_html, "html")
#         admin_msg["Subject"] = "🚀 New Contact Message"
#         admin_msg["From"] = EMAIL_USER
#         admin_msg["To"] = ADMIN_EMAIL

#         server.send_message(admin_msg)
#         print("✅ Admin email sent")

#         # =========================
#         # 2️⃣ Auto-reply to USER
#         # =========================
#         user_html = f"""
#         <h3>Hi {name}, 👋</h3>

#         <p>Thanks for reaching out!</p>
#         <p>We received your message and will get back to you soon.</p>

#         <br/>
#         <p><b>Your Message:</b></p>
#         <p>{message}</p>

#         <br/>
#         <p>Best regards,<br/>Prattyancha</p>
#         """

#         user_msg = MIMEText(user_html, "html")
#         user_msg["Subject"] = "🙌 Thanks for contacting us"
#         user_msg["From"] = EMAIL_USER
#         user_msg["To"] = user_email

#         server.send_message(user_msg)
#         print("✅ User auto-reply sent")

#         # ✅ Close connection
#         server.quit()
#         print("🎉 All emails sent successfully")

#         return True

#     except smtplib.SMTPAuthenticationError:
#         print("❌ SMTP Authentication Failed")
#         raise Exception("Invalid EMAIL_USER or EMAIL_PASS (use App Password)")

#     except smtplib.SMTPException as e:
#         print("❌ SMTP Error:", str(e))
#         raise Exception(f"SMTP error: {str(e)}")

#     except Exception as e:
#         print("❌ General Email Error:", str(e))
#         raise Exception(f"Email failed: {str(e)}")

import os
import requests
import threading
from dotenv import load_dotenv

load_dotenv()

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
ADMIN_EMAIL = "prattyancha009@gmail.com"


def send_email_async(data, headers, url):
    try:
        response = requests.post(url, json=data, headers=headers)
        print("Email status:", response.status_code, response.text)
    except Exception as e:
        print("Async email error:", e)


def send_email(user_email, message, name="User"):
    try:
        if not BREVO_API_KEY:
            raise Exception("BREVO_API_KEY missing")

        url = "https://api.brevo.com/v3/smtp/email"

        headers = {
            "accept": "application/json",
            "api-key": BREVO_API_KEY,
            "content-type": "application/json"
        }

        # =========================
        # 1️⃣ ADMIN EMAIL DATA
        # =========================
        admin_data = {
            "sender": {
                "email": ADMIN_EMAIL,
                "name": "Portfolio Contact"
            },
            "to": [
                {"email": ADMIN_EMAIL}
            ],
            "subject": "🚀 New Contact Message",
            "htmlContent": f"""
                <h2>📩 New Contact Form Submission</h2>
                <p><b>Name:</b> {name}</p>
                <p><b>Email:</b> {user_email}</p>
                <p><b>Message:</b></p>
                <p>{message}</p>
            """
        }

        # =========================
        # 2️⃣ USER AUTO-REPLY DATA
        # =========================
        user_data = {
            "sender": {
                "email": ADMIN_EMAIL,
                "name": "Prattyancha"
            },
            "to": [
                {"email": user_email}
            ],
            "subject": "🙌 Thanks for contacting us",
            "htmlContent": f"""
                <h3>Hi {name}, 👋</h3>
                <p>Thank you for reaching out!</p>
                <p>We have received your message and will get back to you shortly.</p>

                <br/>
                <p><b>Your Message:</b></p>
                <p>{message}</p>

                <br/>
                <p>Best regards,<br/>Prattyancha</p>
            """
        }

        # 🚀 Run both emails in parallel
        t1 = threading.Thread(target=send_email_async, args=(admin_data, headers, url))
        t2 = threading.Thread(target=send_email_async, args=(user_data, headers, url))

        t1.start()
        t2.start()

        # t1.join()
        # t2.join()

        print("✅ Both emails triggered")

        return True

    except Exception as e:
        print("❌ Email Error:", e)
        raise Exception(str(e))