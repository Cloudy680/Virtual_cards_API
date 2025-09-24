from pydantic import BaseModel
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base



# users_table = Table(
#     "users",
#     metadata_user,
#     Column("id", Integer, primary_key = True ),
#     Column("username", String),
#     Column("hashed_password", String),
#     Column("name", String),
#     Column("surname", String),
#     Column("patronymic", String),
#     Column("phone_number", String),
#     Column("adress", String)
# )


class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    hashed_password : Mapped[str] = mapped_column(nullable=False)
    email : Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    surname: Mapped[str] = mapped_column(nullable=False)
    patronymic: Mapped[str] = mapped_column(nullable=False)
    phone_number : Mapped[str] = mapped_column()
    address : Mapped[str] = mapped_column()
    disabled : Mapped[bool] = mapped_column(default=False)

class User(BaseModel):
    username: str
    email: str
    name: str
    surname : str
    patronymic : str
    phone_number: str
    address: str | None = None
    disabled: bool | None = None

    class Config:
        from_attributes = True


class User_In_DB(User):
    hashed_password: str