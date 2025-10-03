from sqlalchemy import select, exists
from app.db.database import async_engine, async_session_factory, Base
from app.models.user import UserORM, User_In_DB, User


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
