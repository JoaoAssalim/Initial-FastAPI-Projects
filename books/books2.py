from typing import Optional
from starlette import status
from pydantic import BaseModel, Field
from fastapi import FastAPI, Path, Query, HTTPException

app = FastAPI()


class Book(BaseModel):
    id: Optional[int] = Field(description="Id is not needed on create", default=None)
    title: str = Field(min_length=3, max_length=100)
    author: str = Field(min_length=1, max_length=100)
    description: str = Field(max_length=100)
    rating: int = Field(ge=0, le=5)
    published_date: int = Field(ge=0)
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "String",
                "author": "String",
                "description": "String",
                "rating": 5,
                "published_date": 2000
            }
        }
    }


BOOKS = [
]

@app.get("/books", status_code=status.HTTP_200_OK)
async def find_all_books():
    return BOOKS
 
@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def find_book_by_id(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.get("/books/rating/", status_code=status.HTTP_200_OK)
async def find_book_by_rating(rating: int = Query(ge=0, le=5)):
    book_rating_list = []
    for book in BOOKS:
        if book.rating == rating:
            book_rating_list.append(book)
    return book_rating_list

@app.get("/books/published/", status_code=status.HTTP_200_OK)
async def find_book_by_published_date(published_date: int = Query(ge=0)):
    book_published_date_list = []
    for book in BOOKS:
        if book.published_date == published_date:
            book_published_date_list.append(book)
    return book_published_date_list

@app.put("/books/update-book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book_request: Book, book_id: int = Path(gt=0)):
    book_request.id = book_id
    
    for e, book in enumerate(BOOKS):
        if book.id == book_id:
            BOOKS[e] = book_request
            return book_request
        
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/delete-book/{book_id}", status_code=status.HTTP_200_OK)
async def delete_book(book_id: int = Path(gt=0)):
    for e, book in enumerate(BOOKS):
        if book.id == book_id:
            deleted_book = BOOKS.pop(e)
            return deleted_book
    raise HTTPException(status_code=404, detail="Book not found")

@app.post("/books/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: Book):
    BOOKS.append(get_book_id(book_request))
    return book_request

def get_book_id(book: Book):
    book.id = BOOKS[-1].id + 1 if len(BOOKS) > 0 else 1
    return book