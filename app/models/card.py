import enum

from pydantic import BaseModel
from datetime import date

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base

class Payment_system(enum.Enum):
    mastercard = "MASTERCARD"
    visa = "VISA"
    belcard = "BELCARD"

class CardORM(Base):
    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str] = mapped_column(String(16), nullable=False, unique = True)
    carrier_name : Mapped[str] = mapped_column(nullable=False)
    expires_date : Mapped[date] = mapped_column(nullable=False)
    payment_system : Mapped[Payment_system] = mapped_column(nullable=False)
    cvv : Mapped[str] = mapped_column(String(3), nullable=False)

    carrier_username : Mapped[str] = mapped_column(ForeignKey("users.username", ondelete="CASCADE"))

    frozen : Mapped[bool] = mapped_column(nullable=False, default=False)



class Card(BaseModel):
    number : str
    carrier_name : str
    expires_date : date
    payment_system : Payment_system
    frozen : bool = False

    class Config:
        from_attributes = True

class Card_In_DB(Card):
    cvv : str