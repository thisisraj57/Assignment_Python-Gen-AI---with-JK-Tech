from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from . import models, schemas

async def create_book(db: AsyncSession, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book

async def get_books(db: AsyncSession):
    result = await db.execute(select(models.Book))
    return result.scalars().all()

async def get_book(db: AsyncSession, book_id: int):
    result = await db.execute(select(models.Book).filter(models.Book.id == book_id))
    return result.scalar()

async def update_book(db: AsyncSession, book_id: int, book: schemas.BookCreate):
    db_book = await get_book(db, book_id)
    if db_book:
        for key, value in book.dict().items():
            setattr(db_book, key, value)
        await db.commit()
        await db.refresh(db_book)
    return db_book

async def delete_book(db: AsyncSession, book_id: int):
    db_book = await get_book(db, book_id)
    if db_book:
        await db.delete(db_book)
        await db.commit()
    return db_book

async def create_review(db: AsyncSession, book_id: int, review: schemas.ReviewCreate):
    db_review = models.Review(book_id=book_id, **review.dict())
    db.add(db_review)
    await db.commit()
    await db.refresh(db_review)
    return db_review

async def get_reviews(db: AsyncSession, book_id: int):
    result = await db.execute(select(models.Review).filter(models.Review.book_id == book_id))
    return result.scalars().all()

async def get_aggregated_rating(db: AsyncSession, book_id: int):
    result = await db.execute(
        select(func.avg(models.Review.rating)).filter(models.Review.book_id == book_id)
    )
    return result.scalar()

async def get_recommendations(db: AsyncSession, genre: str):
    result = await db.execute(select(models.Book).filter(models.Book.genre == genre))
    return result.scalars().all()
