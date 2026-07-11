from fastapi import APIRouter, BackgroundTasks
from app.services.contact_service import add_contact

router = APIRouter()

@router.post("/add-contact")
def create_contact(contact, background_tasks: BackgroundTasks):
    return add_contact(contact, background_tasks)