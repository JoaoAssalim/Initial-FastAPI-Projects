from jose import jwt
from models import User
from typing import Annotated
from pydantic import BaseModel
from database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()

SECRET_KEY = '44b0e33035652a9fd75528a7bf274a39'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username: str, password: str, db: db_dependency):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


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
            hashed_password = bcrypt_context.hash(create_user_request.password),
            role = create_user_request.role,
            is_active = True
        )

        db.add(create_user_model)
        db.commit()
    except Exception as e:
        return {"error": "Unable to create. Try again later..."}

    return create_user_request

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):

    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return "Failed authentication"
    
    token = create_access_token(user.username, user.id, timedelta(minutes=15))
    return {"access_token": token, 'token_type': 'bearer'}