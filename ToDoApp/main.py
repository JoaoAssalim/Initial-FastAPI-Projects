import models
from models import Todo
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from database import engine, SessionLocal
from fastapi import FastAPI, Depends, HTTPException, Path

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(max_length=100)
    priority: int = Field(ge=0, le=5)
    complete: bool = Field(default=False)
    
@app.get("/")
def read_all(db: db_dependency):
    return db.query(Todo).all()

@app.get("/{todo_id}")
def read_one(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo_model:
        return todo_model
    return HTTPException(status_code=404, detail="Todo not found")

@app.post("/")
def create_todo(db: db_dependency, todo_request: TodoRequest):
    todo_model = Todo(**todo_request.dict())
    db.add(todo_model)
    db.commit()
    
    return todo_request

@app.patch("/{todo_id}")
def create_todo(db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
    
    if todo_model:
        todo_model.title = todo_request.title
        todo_model.description = todo_request.description
        todo_model.priority = todo_request.priority
        todo_model.complete = todo_request.complete
        
        db.add(todo_model)
        db.commit()
        
        return todo_request

    return HTTPException(status_code=404, detail="Todo not found")


@app.delete("/{todo_id}")
def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
    
    if todo_model:
        db.delete(todo_model)
        db.commit()
        
        return {"message": "Todo deleted"}

    return HTTPException(status_code=404, detail="Todo not found")