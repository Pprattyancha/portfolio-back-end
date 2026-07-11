from fastapi import APIRouter
from app.models.contact_model import Contact
from app.services.contact_service import add_contact

router = APIRouter()

@router.post("/add-contact")
def create_contact(contact: Contact):
    return add_contact(contact)