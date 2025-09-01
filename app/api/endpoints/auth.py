from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter, Query, Path, Body
from fastapi.security import OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError

from app.core.config import settings
from app.api.dependencies import get_current_active_user, fake_users_db, get_password_hash, authenticate_user, create_access_token, validate_password
from app.core.security import Token


router = APIRouter()

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer", expires_in = settings.ACCESS_TOKEN_EXPIRE_MINUTES)


@router.post("/users/sign_in")
async def sign_in(username: Annotated[str, Query(max_length = 25)],
                  password: Annotated[str, Query(description = "Password must contain: small letter, capital letter, digit, special symbol", min_length = 6), Depends(validate_password)],
                  email: str,
                  phone_number: Annotated[str, Query(example="+000000000000", max_length = 13, min_length = 13)],
                  full_name: str | None = None,
                  adress: str | None = None
                  ):
    if username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    

    hashed_password = get_password_hash(password)
    fake_users_db[username] = {
        "username": username,
        "full_name": full_name,
        "email": email,
        "phone_number": phone_number,
        "adress": adress,
        "hashed_password": hashed_password,
        "disabled": False
    }
    if full_name:
        return {"message": f"Welcome {full_name}!"}
    else:
        return {"message": f"Welcome {username}!"}


