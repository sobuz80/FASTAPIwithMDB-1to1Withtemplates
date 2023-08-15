from fastapi import APIRouter, HTTPException, status
from app.models.user import User
from app.database.mongodb import db

router = APIRouter()


@router.post("/register/", status_code=status.HTTP_201_CREATED)
def register(user: User):
    if db.users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    user_data = {"username": user.username, "password": user.password}
    db.users_collection.insert_one(user_data)
    return {"message": "User registered successfully"}


@router.post("/login/")
def login(user: User):
    user_data = db.users_collection.find_one({"username": user.username, "password": user.password})
    if not user_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return {"message": "Login successful"}