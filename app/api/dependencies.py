from datetime import datetime, timedelta, timezone
from typing import Annotated

import re
import jwt
from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError

from app.core.config import settings
from app.core.security import pwd_context, oauth2_scheme, TokenData

from app.models.user import User, User_In_DB, UserORM

from app.core.db_core import get_user_by_username, check_if_username_exists



def validate_password(password : str):
    has_lower = re.search(r'[a-z]', password) is not None
    has_upper = re.search(r'[A-Z]', password) is not None
    has_digit = re.search(r'\d', password) is not None
    has_special = re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>/?\\|`~]', password) is not None
    password_check = {"small letter" : has_lower, "capital letter" : has_upper, "digit" : has_digit, "special symbol" : has_special}
    for key in password_check:
        if not password_check[key]:
            raise HTTPException(status_code=400, detail=password_check)



def check_if_active(user : User):
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user(username: str):
    if await check_if_username_exists(username):
        user_from_db = await get_user_by_username(username)
        return user_from_db
    else:
        return None


async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token,
                             settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM],
                             options={"verify_exp": True}
                             )
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    check_if_active(current_user)
    return current_user

