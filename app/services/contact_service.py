from fastapi import APIRouter, BackgroundTasks
from app.services.email_service import send_email
from app.db.database import get_db
from app.models.contact_model import Contact

router = APIRouter()

@router.post("/add-contact")
async def add_contact(contact: Contact, background_tasks: BackgroundTasks):
    try:
        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)",
            (contact.name, contact.email, contact.message)
        )
        db.commit()

        print("DB insert success")

        # 🚀 FASTEST → async background task
        background_tasks.add_task(
            send_email,
            contact.email,
            contact.message,
            contact.name
        )

        return {"message": "Saved ✅ Email sending in background"}

    except Exception as e:
        print("ERROR:", e)
        return {"error": str(e)}