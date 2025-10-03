from sqlalchemy import select, exists, text
from app.db.database import async_engine, async_session_factory, Base
from app.models.user import UserORM, User_In_DB, User
from app.models.transaction import TransactionORM ,Transaction
from app.models.card import CardORM


async def create_tables():
    async with async_engine.begin() as conn:
        # await conn.execute(text("DROP TABLE IF EXISTS transactions CASCADE"))
        # await conn.execute(text("DROP TABLE IF EXISTS transaction CASCADE"))
        # await conn.execute(text("DROP TABLE IF EXISTS cards CASCADE"))
        # await conn.execute(text("DROP TABLE IF EXISTS users CASCADE"))
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

async def check_if_username_exists(username : str):
    async with async_session_factory() as session:
        stmt = select(exists().where(UserORM.username == username))
        result = await session.execute(stmt)
        return result.scalar()

async def get_user_by_username(username : str):
    async with async_session_factory() as session:
        stmt = select(UserORM).where(UserORM.username == username)
        user = await session.scalars(stmt)
        return user.first()

async def add_new_transaction(transaction: Transaction, c_number : str):
    async with async_session_factory() as session:
        new_transaction = TransactionORM(amount_of_money = transaction.amount_of_money,
                                         name = transaction.name,
                                         transaction_date = transaction.transaction_date,
                                         transaction_time = transaction.transaction_time,
                                         status = transaction.status,
                                         card_number = c_number
                                         )
        session.add(new_transaction)
        await session.commit()
