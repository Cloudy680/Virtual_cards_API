from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str
    full_name: str | None = None
    phone_number: str
    adress: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str