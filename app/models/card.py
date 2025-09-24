import enum

from pydantic import BaseModel
from datetime import date

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base

class payment_system(enum.Enum):
    mastercard = "mastercard"
    visa = "visa"
    belcard = "belcard"

class CardORM(Base):
    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int] = mapped_column(String(16), nullable=False)
    carrier_name : Mapped[str] = mapped_column(nullable=False)
    establishment_date : Mapped[date] = mapped_column(nullable=False)
    expires_date : Mapped[date] = mapped_column(nullable=False)
    payment_system : Mapped[payment_system]
    cvv : Mapped[str] = mapped_column(String(3), nullable=False)

    user_id : Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))




class Card(BaseModel):
    number : str
    carrier_name : str
    establishment_date : date
    expires_date : date
    payment_system : str

class Card_In_DB(Card):
    cvv : int