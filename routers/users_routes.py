from fastapi import APIRouter, Body, status

from config.database import db
from models.user import UserCollection, UserModel


router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[],
    responses={
        404: {"description": "Not found"},
        401: {"description": "Not authenticated"},
        403: {"description": "Forbidden"}
    },
)
users_collection = db.get_collection("users")


@router.get(
    "/",
    response_model = UserCollection,
    status_code = status.HTTP_201_CREATED,
    response_model_by_alias = False,
    response_description = "List of all users"
)
async def get_users():
    return await UserCollection(students = users_collection.find())