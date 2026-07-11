from app.db.database import get_db

def add_review(review):
    query = "INSERT INTO reviews (name, rating, comment) VALUES (%s, %s, %s)"
    values = (review.name, review.rating, review.comment)

    db = get_db()
    cursor = db.cursor()
    cursor.execute(query, values)
    db.commit()

    return {"message": "Review added successfully"}

def get_reviews():
    db = get_db()
    cursor = db.cursor(dictionary=True)  # 👈 returns JSON-like data

    query = "SELECT * FROM reviews ORDER BY id DESC"
    cursor.execute(query)

    reviews = cursor.fetchall()

    cursor.close()
    db.close()

    return reviews