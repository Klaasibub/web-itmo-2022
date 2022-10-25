import json
from typing import Optional
from datetime import datetime, timedelta

from tortoise.exceptions import DoesNotExist
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from jose import jwt

from models import User
from api import verify_password, get_current_user, get_password_hash
from api.types import UserType, UserInType

from broker import send_msg
from settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, DEFAULT_QUEUE


router = APIRouter(
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


class Token(BaseModel):
    access_token: str
    token_type: str


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

unauthorized_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/token")
async def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = await UserType.from_queryset_single(User.get(email=form_data.username))
    except DoesNotExist:
        raise unauthorized_exception

    if not verify_password(form_data.password, user.password):
        raise unauthorized_exception

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    token = jsonable_encoder(access_token)
    response = JSONResponse(content={
        "access_token": access_token,
        "token_type": "bearer",
        "message": "You've successfully logged in. Welcome back!"
    })
    response.set_cookie(
        "Authorization",
        value=f"Bearer {token}",
        httponly=True,
        max_age=1800,
        expires=1800,
        samesite="Lax",
        secure=True,
    )

    return response


@router.post("/registration")
async def registration(user: UserInType):
    user = user.dict(exclude_unset=True)
    user['password'] = get_password_hash(user['password'])
    user_obj = await User.create(**user)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_obj.email}, expires_delta=access_token_expires
    )
    send_msg(DEFAULT_QUEUE, body=json.dumps({
        "from": "web-itmo@course.smile",
        "to": user_obj.email,
        "subject": "Registration",
        "msg": "You have successfully registered!",
    }))
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login")
async def login(user_data: UserInType):
    try:
        user = await UserType.from_queryset_single(User.get(email=user_data.email))
    except DoesNotExist:
        raise unauthorized_exception

    if not verify_password(user_data.password, user.password):
        raise unauthorized_exception

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserType)
async def get_user(user: UserType = Depends(get_current_user)):
    return user
