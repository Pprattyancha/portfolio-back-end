from fastapi import APIRouter, BackgroundTasks
from app.models.contact_model import Contact
from app.services.contact_service import add_contact

router = APIRouter()

@router.post("/add-contact")
def create_contact(contact: Contact, background_tasks: BackgroundTasks):
    return add_contact(contact, background_tasks)