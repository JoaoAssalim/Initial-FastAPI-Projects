from fastapi import FastAPI, Body

app = FastAPI()

BOOKS = [
    {"title": "title of the book 2", "author": "author of the book 2"},
    {"title": "title of the book 3", "author": "author of the book 3"},
    {"title": "title of the book 4", "author": "author of the book 4"}
]

@app.get("/books")
async def find_all_books():
    return BOOKS

# Path parameters
@app.get("/books/{book_id}")
async def find_unique_book(book_id: int):
    if len(BOOKS) > book_id:
        return BOOKS[book_id]
    return {"message": "Book not found"}

# Query parameters
@app.get("/books/")
async def find_book_by_title(title: str):
    for book in BOOKS:
        if book.get("title").casefold() == title.casefold():
            return book
    return {"message": "Book not found"}

@app.post("/books/create-book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)
    return {"message": new_book}

@app.patch("/books/update-book/{book_id}")
async def update_book(book_id: int, book_update=Body()):
    if len(BOOKS) > book_id:
        BOOKS[book_id] = book_update
        return {"message": book_update}
    return {"message": "Book not found"}

@app.delete("/books/delete-book/{book_id}")
async def delete_book(book_id: int):
    if len(BOOKS) > book_id:
        deleted_book = BOOKS.pop(book_id)
        return {"message": deleted_book}
    return {"message": "Book not found"}

@app.get("/books/find-all-books-from-author/{author}")
async def find_all_books_from_author(author: str):
    books_by_author = []
    for book in BOOKS:
        if book.get("author").upper() == author.upper():
            books_by_author.append(book)
    
    return books_by_author