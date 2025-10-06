from sqlalchemy import select

from app.db.database import async_session_factory

from app.models.user import User, User_In_DB, UserORM


class UserCRUD:

    @staticmethod
    async def add_new_user(user: User_In_DB):
        async with async_session_factory() as session:
            new_user = UserORM(username=user.username,
                               hashed_password=user.hashed_password,
                               email=user.email,
                               name=user.name,
                               surname=user.surname,
                               patronymic=user.patronymic,
                               phone_number=user.phone_number,
                               address=user.address,
                               disabled=user.disabled)
            session.add(new_user)
            await session.commit()\

    @staticmethod
    async def get_user_by_username(username: str):
        async with async_session_factory() as session:
            stmt = select(UserORM).where(UserORM.username == username)
            user = await session.scalars(stmt)
            return user.first()

    @staticmethod
    async def select_all_users():
        async with async_session_factory() as session:
            stmt = select(UserORM)
            result = await session.execute(stmt)
            users = result.scalars().all()
            return [User.model_validate(user) for user in users]

    @staticmethod
    async def delete_account_by_username(username : str):
        async with async_session_factory() as session:
            stmt = select(UserORM).where(UserORM.username == username)
            result = await session.execute(stmt)
            user = result.scalar()

            if user:
                await session.delete(user)
                await session.commit()
                return True
            else:
                return False




user_CRUD_operations = UserCRUD()