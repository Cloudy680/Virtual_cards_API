from sqlalchemy import text
from app.db.database import async_engine, async_session_factory, Base
from app.models.user import metadata_user, UserORM, User_In_DB

async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
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