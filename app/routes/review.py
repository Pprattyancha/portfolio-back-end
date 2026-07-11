from fastapi import APIRouter
from app.models.review_model import Review
from app.services.review_service import add_review,get_reviews

router = APIRouter()

@router.post("/add-review")
def create_review(review: Review):
    return add_review(review)

# GET - Fetch reviews
@router.get("/reviews")
def fetch_reviews():
    return get_reviews()