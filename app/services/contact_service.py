from app.db.database import get_db
from app.services.email_service import send_email

def add_contact(contact):
    try:
        db = get_db()
        cursor = db.cursor()

        query = "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)"
        values = (contact.name, contact.email, contact.message)

        cursor.execute(query, values)
        db.commit()

        print("DB insert success")

        # ✅ Send email safely
        try:
            send_email(contact.email, contact.message, contact.name)
            email_status = "Email sent"
        except Exception as e:
            print("Email error:", e)
            email_status = "Email failed"

        cursor.close()
        db.close()

        return {
            "message": "Contact saved",
            "email_status": email_status
        }

    except Exception as e:
        print("ERROR:", e)
        return {"error": str(e)}