from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str
    full_name: str
    phone_number: str
    adress: str | None = None
    disabled: bool | None = None


class User_In_DB(User):
    hashed_password: str