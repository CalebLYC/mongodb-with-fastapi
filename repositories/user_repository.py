import datetime
from fastapi import Body, HTTPException
import jwt

from config.env import env
from models.user import UserCollection, UserCreateModel, UserModel


def create_access_token(data: dict, expires_delta: datetime.timedelta = None):
    return jwt.encode(data, env('SECRET_KEY'), algorithm=env('ALGORITHM'))

async def create_user(users_collection: UserCollection, user: UserCreateModel = Body(...)):
    db_user = await users_collection.find_one({'email': user.email})
    if db_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    db_user = await users_collection.find_one({'username': user.username})
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = await users_collection.insert_one(
        UserCreateModel(
            **user.model_dump(
            by_alias=True,
            exclude=['id', 'password'],
        ),
        password = create_access_token({'sub': user.password})
        ).model_dump(
            by_alias=True,
            exclude=['id'],
        ),
    )
    return await users_collection.find_one({'_id': new_user.inserted_id})


async def get_users(users_collection: UserCollection):
    return await UserCollection(students = users_collection.find())