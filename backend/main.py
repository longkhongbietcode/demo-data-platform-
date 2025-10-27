from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import os

app = FastAPI(title="Bookshop API")

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@postgres:5432/bookshop")

class Book(BaseModel):
    title: str
    author: str
    price: float

@app.on_event("startup")
def connect_db():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                price NUMERIC(10,2)
            );
        """)
        conn.commit()
        conn.close()
    except Exception as e:
        print("Database connection failed:", e)

@app.post("/books/")
def create_book(book: Book):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (title, author, price) VALUES (%s, %s, %s);",
                       (book.title, book.author, book.price))
        conn.commit()
        conn.close()
        return {"message": "Book added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/books/")
def get_books():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, author, price FROM books;")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "title": r[1], "author": r[2], "price": float(r[3])} for r in rows]
