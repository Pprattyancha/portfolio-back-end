import os
import httpx
from dotenv import load_dotenv

load_dotenv()

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
ADMIN_EMAIL = "prattyancha009@gmail.com"

async def send_email(user_email: str, message: str, name: str = "User"):
    if not BREVO_API_KEY:
        print("❌ BREVO_API_KEY missing")
        return

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }

    # ✅ MUST be verified in Brevo
    VERIFIED_SENDER = ADMIN_EMAIL  

    admin_data = {
        "sender": {
            "email": VERIFIED_SENDER,
            "name": "Portfolio Contact"
        },
        "to": [{"email": ADMIN_EMAIL}],
        "replyTo": {  # ✅ IMPORTANT
            "email": user_email,
            "name": name
        },
        "subject": f"🚀 New message from {name}",
        "htmlContent": f"""
        <h3>New Contact Message</h3>
        <p><b>Name:</b> {name}</p>
        <p><b>Email:</b> {user_email}</p>
        <p><b>Message:</b> {message}</p>
        """
    }

    user_data = {
        "sender": {
            "email": VERIFIED_SENDER,
            "name": "Prattyancha"
        },
        "to": [{"email": user_email}],
        "subject": "🙌 Thanks for contacting us",
        "htmlContent": f"""
        <h3>Hi {name},</h3>
        <p>Thanks for reaching out! I'll get back to you soon.</p>
        """
    }

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            res1 = await client.post(url, json=admin_data, headers=headers)
            res2 = await client.post(url, json=user_data, headers=headers)

            print("ADMIN STATUS:", res1.status_code, res1.text)
            print("USER STATUS:", res2.status_code, res2.text)

            if res1.status_code >= 400 or res2.status_code >= 400:
                print("❌ Email sending failed")

            else:
                print("✅ Emails sent successfully")

    except Exception as e:
        print("❌ Email error:", e)