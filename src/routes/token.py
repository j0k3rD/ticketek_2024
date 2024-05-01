from datetime import timedelta
from typing import Annotated
import os
from dotenv import load_dotenv
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from src.utils.authenticate_user import authenticate_user
from src.utils.create_token import create_token
from src.utils.validate_refresh_token import validate_refresh_token
from models import Token, User


refresh_tokens = []

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES"))

token = APIRouter()


@token.post("/token", tags=["token"])
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = authenticate_user(
        form_data.username,
        form_data.password,
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect Username or Password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    access_token = create_token(
        data={"sub": user.name, "role": user.role},
        expires_delta=access_token_expires,
    )
    refresh_token = create_token(
        data={"sub": user.name, "role": user.role},
        expires_delta=refresh_token_expires,
    )
    refresh_tokens.append(refresh_token)
    return Token(access_token=access_token, refresh_token=refresh_token)


@token.post("/refresh", tags=["token"])
async def refresh_access_token(
    token_data: Annotated[tuple[User, str], Depends(validate_refresh_token)]
):
    user, token = token_data
    access_token = create_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = create_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES),
    )

    refresh_tokens.remove(token)
    refresh_tokens.append(refresh_token)
    return Token(access_token=access_token, refresh_token=refresh_token)
