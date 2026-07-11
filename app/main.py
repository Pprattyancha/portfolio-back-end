from fastapi import FastAPI
from app.routes import review, contact

app = FastAPI()

app.include_router(review.router, prefix="/api")
app.include_router(contact.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "API running 🚀"}