from fastapi import APIRouter, BackgroundTasks
from app.models.contact_model import Contact
from app.services.contact_service import add_contact

router = APIRouter()

@router.post("/add-contact")
async def create_contact(contact: Contact, background_tasks: BackgroundTasks):
    return await add_contact(contact, background_tasks)