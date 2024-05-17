import datetime
from enum import Enum
import pydantic

from bson import ObjectId
from pydantic import Field
import datetime


from typing import Optional
from pydantic import BaseModel, EmailStr, constr


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type='string')

class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    username: constr(min_length=3, max_length=50)
    password_hash: str
    created: datetime.datetime
    email: EmailStr
    profile_image_s3_path: Optional[str] = None
    bio: Optional[str] = None
    last_login: Optional[datetime.datetime] = None
    is_active: bool = True
    is_admin: bool = False
    date_of_birth: Optional[datetime.datetime] = None
    phone_number: Optional[str] = None

    class Config:
        orm_mode = True


class UserComment(pydantic.BaseModel):
    id: int
    user_id: int
    comment: str
    created: datetime.datetime
    replied_to: Optional[int]


class UserCommentLike(pydantic.BaseModel):
    id: int
    user_id: int
    comment_id: str
    created: datetime.datetime


class UserRecipeLike(pydantic.BaseModel):
    id: int
    user_id: int
    recipe_id: int
    created: datetime.datetime


class UserCommentDislike(pydantic.BaseModel):
    id: int
    user_id: int
    comment_id: str
    created: datetime.datetime


class UserRecipeDislike(pydantic.BaseModel):
    id: int
    user_id: int
    recipe_id: int
    created: datetime.datetime





