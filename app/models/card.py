import enum

from pydantic import BaseModel
from datetime import date

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import async_session_factory, Base
from sqlalchemy import select, exists

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
    id : int |  None = None
    number : str = None
    carrier_name : str = None
    expires_date : date = None
    payment_system : Payment_system = None
    frozen : bool = False


    @staticmethod
    async def check_if_card_exists(number : str, carrier_username : str) -> bool:
        async with async_session_factory() as session:
            stmt = select(exists().where(CardORM.number == number, CardORM.carrier_username == carrier_username))
            result = await session.execute(stmt)
            return result.scalar()

    @staticmethod
    async def check_if_card_is_frozen(id : int, carrier_username : str) -> bool:
        async with async_session_factory() as session:
            stmt = select(exists().where(CardORM.id == id, CardORM.carrier_username == carrier_username,
                                         CardORM.frozen == True))
            result = await session.execute(stmt)
            return result.scalar()

    class Config:
        from_attributes = True

class Card_In_DB(Card):
    cvv : str


Card_check_functions = Card()