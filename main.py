from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from . import models, schemas, crud, database, gemini_integration

app = FastAPI()

# --- BOOK ENDPOINTS ---

@app.post("/books", response_model=schemas.Book)
async def create_book(book: schemas.BookCreate, db: AsyncSession = Depends(database.get_db)):
    return await crud.create_book(db=db, book=book)

@app.get("/books", response_model=List[schemas.Book])
async def read_books(db: AsyncSession = Depends(database.get_db)):
    return await crud.get_books(db=db)

@app.get("/books/{book_id}", response_model=schemas.Book)
async def read_book(book_id: int, db: AsyncSession = Depends(database.get_db)):
    db_book = await crud.get_book(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.put("/books/{book_id}", response_model=schemas.Book)
async def update_book(book_id: int, book: schemas.BookCreate, db: AsyncSession = Depends(database.get_db)):
    db_book = await crud.update_book(db=db, book_id=book_id, book=book)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.delete("/books/{book_id}")
async def delete_book(book_id: int, db: AsyncSession = Depends(database.get_db)):
    db_book = await crud.delete_book(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}

# --- REVIEW ENDPOINTS ---

@app.post("/books/{book_id}/reviews", response_model=schemas.Review)
async def create_review(book_id: int, review: schemas.ReviewCreate, db: AsyncSession = Depends(database.get_db)):
    db_book = await crud.get_book(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return await crud.create_review(db=db, book_id=book_id, review=review)

@app.get("/books/{book_id}/reviews", response_model=List[schemas.Review])
async def read_reviews(book_id: int, db: AsyncSession = Depends(database.get_db)):
    return await crud.get_reviews(db=db, book_id=book_id)

# --- SUMMARY & RATING ENDPOINT ---

@app.get("/books/{book_id}/summary")
async def get_summary_and_rating(book_id: int, db: AsyncSession = Depends(database.get_db)):
    db_book = await crud.get_book(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    summary = await gemini_integration.generate_summary(db_book.summary)
    avg_rating = await crud.get_aggregated_rating(db=db, book_id=book_id)
    return {"summary": summary, "average_rating": avg_rating or 0}

# --- RECOMMENDATIONS ENDPOINT ---

@app.get("/recommendations")
async def get_recommendations(genre: str, db: AsyncSession = Depends(database.get_db)):
    recommendations = await crud.get_recommendations(db=db, genre=genre)
    return recommendations

# --- GENERATING SUMMARY FOR BOOK CONTENT ---

@app.post("/generate-summary")
async def generate_book_summary(input_text: str):
    summary = await gemini_integration.generate_summary(input_text)
    return {"summary": summary}