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

    admin_data = {
        "sender": {"email": ADMIN_EMAIL, "name": "Portfolio"},
        "to": [{"email": ADMIN_EMAIL}],
        "subject": "🚀 New Contact Message",
        "htmlContent": f"""
        <h3>New Contact</h3>
        <p><b>Name:</b> {name}</p>
        <p><b>Email:</b> {user_email}</p>
        <p>{message}</p>
        """
    }

    user_data = {
        "sender": {"email": ADMIN_EMAIL, "name": "Prattyancha"},
        "to": [{"email": user_email}],
        "subject": "🙌 Thanks for contacting us",
        "htmlContent": f"""
        <h3>Hi {name}</h3>
        <p>We received your message.</p>
        """
    }

    try:
        async with httpx.AsyncClient(timeout=5) as client:
            # 🚀 send both emails concurrently
            await client.post(url, json=admin_data, headers=headers)
            await client.post(url, json=user_data, headers=headers)

        print("✅ Emails sent (async fast)")

    except Exception as e:
        print("❌ Email error:", e)