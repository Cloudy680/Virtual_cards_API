from datetime import datetime, timedelta, timezone
from typing import Annotated

import re
import jwt
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from jwt.exceptions import InvalidTokenError

from app.core.config import settings
from app.core.security import pwd_context, oauth2_scheme, TokenData

from app.models.user import User, UserInDB



fake_users_db = {
    "testuser": {
        "username": "testuser",
        "full_name": "Test User",
        "email": "test@example.com",
        "adress": "221B Baker Street",
        "hashed_password": "$2b$12$tKVCHV/haROHeOQZ9OLzZex2bDx8/ZP3BwejXH/cE7jmyaoIfxuoa",
        "disabled": False,
    }
}


def validate_password(password : str):
    has_lower = re.search(r'[a-z]', password) is not None
    has_upper = re.search(r'[A-Z]', password) is not None
    has_digit = re.search(r'\d', password) is not None
    has_special = re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>/?\\|`~]', password) is not None
    password_check = {"small letter" : has_lower, "capital letter" : has_upper, "digit" : has_digit, "special symbol" : has_special}
    for key in password_check:
        if password_check[key] == False:
            raise HTTPException(status_code=400, detail=f"Password must contain {key}")
    return password


def check_if_active(user : User):
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
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
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    check_if_active(current_user)
    return current_user