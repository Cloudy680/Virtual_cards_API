from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str = None
    full_name: str = None
    phone_number: str | None = None
    adress: str = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str