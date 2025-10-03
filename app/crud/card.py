from app.db.database import async_session_factory
from app.models.card import CardORM, Card, Card_In_DB
from sqlalchemy import select, exists
from datetime import date



class CardCRUD:
    @staticmethod
    async def add_new_card(card: Card_In_DB, username):
        async with async_session_factory() as session:
            new_card = CardORM(number=card.number,
                               carrier_name=card.carrier_name,
                               expires_date=card.expires_date,
                               payment_system=card.payment_system,
                               cvv=card.cvv,
                               carrier_username=username)
            session.add(new_card)
            await session.commit()

    @staticmethod
    async def get_all_cards(username):
        async with async_session_factory() as session:
            stmt = select(CardORM).where(CardORM.carrier_username == username)
            result = await session.execute(stmt)
            cards = result.scalars().all()
            return [Card.model_validate(card) for card in cards]

    @staticmethod
    async def delete_card(number, carrier_username):
        async with async_session_factory() as session:
            stmt = select(CardORM).where(CardORM.number == number, CardORM.carrier_username == carrier_username)
            result = await session.execute(stmt)
            card = result.scalar()

            if card:
                await session.delete(card)
                await session.commit()
                return True
            else:
                return False

    @staticmethod
    async def change_card_expires_date(number, carrier_username, new_expires_date):
        async with async_session_factory() as session:
            stmt = select(CardORM).where(CardORM.number == number, CardORM.carrier_username == carrier_username)
            result = await session.execute(stmt)
            card = result.scalar_one_or_none()
            if card:
                if card.frozen:
                    if new_expires_date > date.today():
                        card.expires_date = new_expires_date
                        card.frozen = False
                        await session.commit()
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False

Card_CRUD = CardCRUD()