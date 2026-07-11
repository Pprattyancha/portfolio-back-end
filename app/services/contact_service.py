from app.db.database import get_db
from app.services.email_service import send_email

def add_contact(contact, background_tasks):
    try:
        db = get_db()
        cursor = db.cursor()

        query = "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)"
        values = (contact.name, contact.email, contact.message)

        cursor.execute(query, values)
        db.commit()

        print("DB insert success")

        # ✅ background email
        background_tasks.add_task(
            send_email,
            contact.email,
            contact.message,
            contact.name
        )

        cursor.close()
        db.close()

        return {"message": "Contact saved & email will be sent"}

    except Exception as e:
        print("ERROR:", e)
        return {"error": str(e)}