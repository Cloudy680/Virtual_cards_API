from app.models.transaction import TransactionORM ,Transaction
from app.db.database import async_session_factory
from sqlalchemy import select


class TransactionCRUD:

    @staticmethod
    async def add_new_transaction(transaction: Transaction, c_number: str):
        async with async_session_factory() as session:
            new_transaction = TransactionORM(amount_of_money=transaction.amount_of_money,
                                             name=transaction.name,
                                             transaction_date=transaction.transaction_date,
                                             transaction_time=transaction.transaction_time,
                                             status=transaction.status,
                                             card_number=c_number
                                             )
            session.add(new_transaction)
            await session.commit()


    @staticmethod
    async def get_all_transactions_by_card_id(card_number : str):
        async with async_session_factory() as session:
            stmt = select(TransactionORM).where(TransactionORM.card_number == card_number)
            result = await session.execute(stmt)
            transactions = result.scalars().all()
            return [Transaction.model_validate(transaction) for transaction in transactions]


transaction_crud = TransactionCRUD()