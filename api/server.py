import hashlib
import json
import os
from typing import Optional

from fastapi import FastAPI, HTTPException
from passlib.handlers import bcrypt
from pydantic import BaseModel, EmailStr

import psycopg2  # You need to configure your Redshift connection separately
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

import jwt
from passlib.context import CryptContext
import bcrypt
from starlette.middleware.cors import CORSMiddleware

from models.users import User
from rds.rds import Client

from api.token_verification import verify_token
import configparser
import datetime

from rds.table_create_scripts.users import verify_or_create_tables
config = configparser.ConfigParser()
config.read("settings.cfg")

verify_or_create_tables()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use "*" to allow all origins
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
    allow_credentials=False,  # Do not allow credentials (cookies, HTTP authentication)
)

# JWT settings
SECRET_KEY = os.getenv("USER_API_SECRET")

ALGORITHM = "HS256"

# Password hashing settings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for token generation
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Replace with your Redshift database connection information

async def create_jwt_token(data: dict):
    to_encode = data.copy()
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

async def authenticate_user(username: str, password: str):
    with Client(config) as client:
        user = client.get_user(username)
        if user and bcrypt.checkpw(password.encode("utf-8"), user['password_hash'].encode("utf-8")):
            return user


@app.post("/user/create")
async def create_user(username: str, password: str, email: EmailStr, profile_image_s3_path: Optional[str] = None,
                      bio: Optional[str] = None, date_of_birth: Optional[datetime.datetime] = None,
                      phone_number: Optional[str] = None):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update((username + password).encode('utf-8'))
    hashed_value = hash_algorithm.hexdigest()

    user = User(
        username=username,
        password_hash=hashed_password.decode('utf-8'),
        created=datetime.datetime.utcnow(),
        email=email,
        profile_image_s3_path=profile_image_s3_path,
        bio=bio,
        last_login=None,
        is_active=True,
        is_admin=False,
        date_of_birth=date_of_birth,
        phone_number=phone_number
    )

    with Client(config) as client:
        try:
            client.insert_user(user)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return {"message": "success"}


@app.post("/login/")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    with Client(config) as client:
        user = client.get_user(form_data.username)

        provided_password_bytes = form_data.password.encode("utf-8")
        if user is None or not bcrypt.checkpw(provided_password_bytes, user['password_hash'].encode("utf-8")):
            raise HTTPException(
                status_code=400,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create a dictionary with user claims
        user_claims = {"uhash": user["uhash"]}

        # Generate the JWT token
        access_token = create_jwt_token(user_claims)

        return {"access_token": access_token, "token_type": "bearer"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
