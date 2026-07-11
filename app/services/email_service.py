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
        'htmlContent' : f"""
        <div style="font-family: Arial, sans-serif; background-color: #f4f6f8; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background: #ffffff; border-radius: 10px; padding: 30px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">

            <h2 style="color: #2d3748; margin-bottom: 10px;">Hi {name}, 👋</h2>

            <p style="color: #4a5568; font-size: 15px;">
            Thank you for reaching out! I’ve received your message and really appreciate you taking the time to connect.
            </p>

            <p style="color: #4a5568; font-size: 15px;">
            I’ll review your message and get back to you as soon as possible.
            </p>

            <div style="margin: 25px 0; padding: 15px; background: #f7fafc; border-left: 4px solid #3182ce;">
            <p style="margin: 0; color: #2d3748; font-size: 14px;">
                💡 <strong>Quick Note:</strong> If your query is urgent, feel free to reply directly to this email.
            </p>
            </div>

            <p style="color: #4a5568; font-size: 15px;">
            Best regards,<br>
            <strong>Prattyancha Patharkar</strong><br>
            Frontend Lead
            </p>

            <hr style="margin: 25px 0; border: none; border-top: 1px solid #e2e8f0;">

            <p style="font-size: 12px; color: #a0aec0; text-align: center;">
            This is an automated response confirming receipt of your message.
            </p>

        </div>
        </div>
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