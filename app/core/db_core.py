from sqlalchemy import text, select, exists
from app.db.database import async_engine, async_session_factory, Base
from app.models.user import UserORM, User_In_DB, User
from app.models.card import CardORM, Card_In_DB, Card

async def create_tables():
    async with async_engine.begin() as conn:
        # await conn.run_sync(lambda sync_conn: Base.metadata.drop_all(
        #     sync_conn,
        #     tables=[CardORM.__table__, UserORM.__table__]
        # ))
        await conn.run_sync(Base.metadata.create_all)
    print("Tables are created!")


async def add_new_user(user : User_In_DB):
    async with async_session_factory() as session:
        new_user = UserORM(username = user.username,
                           hashed_password =user.hashed_password,
                           email = user.email,
                           name = user.name,
                           surname = user.surname,
                           patronymic = user.patronymic,
                           phone_number = user.phone_number,
                           address = user.address,
                           disabled = user.disabled)
        session.add(new_user)
        await session.commit()


async def select_all_users():
    async with async_session_factory() as session:
        query = select(UserORM)
        result = await session.execute(query)
        users = result.scalars().all()
        return [User.model_validate(user) for user in users]

async def check_if_username_exists(username):
    async with async_session_factory() as session:
        stmt = select(exists().where(UserORM.username == username))
        result = await session.execute(stmt)
        return result.scalar()

async def get_user_by_username(username):
    async with async_session_factory() as session:
        stmt = select(UserORM).where(UserORM.username == username)
        user = await session.scalars(stmt)
        return user.first()

async def get_all_cards(username):
    async with async_session_factory() as session:
        stmt = select(CardORM).where(CardORM.carrier_username == username)
        result = await session.execute(stmt)
        cards =result.scalars().all()
        return [Card.model_validate(card) for card in cards]


async def add_new_card(card : Card_In_DB, username ):
    async with async_session_factory() as session:
        new_card = CardORM(number = card.number,
                           carrier_name = card.carrier_name,
                           expires_date = card.expires_date,
                           payment_system = card.payment_system,
                           cvv = card.cvv,
                           carrier_username = username)
        session.add(new_card)
        await session.commit()

async def check_if_card_exists(number, carrier_username):
    async with async_session_factory() as session:
        stmt = select(exists().where(CardORM.number == number, CardORM.carrier_username == carrier_username))
        result = await session.execute(stmt)
        return result.scalar()

async def freeze_card(number, carrier_username):
    async with async_session_factory() as session:
        stmt = select(CardORM).where(CardORM.number == number, CardORM.carrier_username == carrier_username)
        result = await session.execute(stmt)
        card = result.scalar_one_or_none()

        if card:
            card.frozen = True
            await session.commit()
            return True
        else:
            return False
