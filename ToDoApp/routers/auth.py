from models import User
from typing import Annotated
from pydantic import BaseModel
from database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends


router = APIRouter()

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/users")
async def list_all_users(db: db_dependency):
    return db.query(User).all()


@router.post("/auth")
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    try:
        create_user_model = User(
            username = create_user_request.username,
            email = create_user_request.email,
            first_name = create_user_request.first_name,
            last_name = create_user_request.last_name,
            hashed_password = create_user_request.password,
            role = create_user_request.role,
            is_active = True
        )

        db.add(create_user_model)
        db.commit()
    except Exception as e:
        return {"error": "Unable to create. Try again later..."}

    return create_user_request