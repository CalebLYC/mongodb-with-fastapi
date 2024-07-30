import datetime
import bcrypt
from fastapi import APIRouter, Body, HTTPException, status
import jwt

from config.database import db
from models.student import StudentModel
from models.user import UserCreateModel, UserModel
from repositories import user_repository


router = APIRouter(
    tags=["Auth"],
    dependencies=[],
    responses={
        404: {"description": "Not found"},
        401: {"description": "Not authenticated"},
        403: {"description": "Forbidden"}
    },
)
users_collection = db.get_collection("users")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


@router.post(
    "/register",
    response_model = UserModel,
    status_code = status.HTTP_201_CREATED,
    response_model_by_alias = False,
    response_description = "Register User"
)
async def register(user: UserCreateModel = Body(...)):
    return await user_repository.create_user(users_collection=users_collection, user=user)