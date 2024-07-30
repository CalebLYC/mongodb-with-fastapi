from typing import Annotated, List, Optional
from bson import ObjectId
from pydantic import BaseModel, BeforeValidator, ConfigDict, EmailStr, Field


PyObjectId = Annotated[str, BeforeValidator(str)]


class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(...)
    email: EmailStr = Field(...)
    username: Optional[str] = Field(...)
    fullname: Optional[str] = Field(...)


class UserCreateModel(UserModel):
    password: str = Field(...)
    model_config = ConfigDict(
        populate_by_name = True,
        arbitrary_types_allowed = True,
        json_schema_extra = {
            'example': {
                "name": "jdoe",
                "email": "jdoe@example.com",
                "username": "jdoe",
                "fullname": "John Doe",
                "password": "12345678"
            }
        }
    )


class UpdateUserModel(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    username: Optional[str] = Field(...)
    fullname: Optional[str] = Field(...)
    model_config = ConfigDict(
        arbitrary_types_allowed = True,
        json_encoders = {ObjectId: str},
        json_schema_extra = {
            "example": {
                "name": "jdoe",
                "email": "jdoe@example.com",
                "username": "jdoe",
                "fullname": "John Doe",
                "password": "12345678",
            }
        }
    )


class UserCollection(BaseModel):
    users: List[UserModel]