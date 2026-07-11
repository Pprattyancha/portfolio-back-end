from pydantic import BaseModel

class Review(BaseModel):
    name: str
    rating: int
    comment: str