from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from app.api.dependencies import get_current_active_user
from app.core.db_core import add_new_transaction
from app.models.user import User
from datetime import date, datetime
from app.models.transaction import Status, Transaction
from app.crud.card import Card_CRUD


router = APIRouter()


@router.post("/Payments")
async def make_payment(current_user : Annotated[User, Depends(get_current_active_user)],
                            card_id : int,
                            money_amount : float,
                            company_name: str = "Free payment"):
    card = await Card_CRUD.get_card_by_id(card_id,current_user.username)
    if card is not None:
        if not card.frozen:
            transaction_data = {"amount_of_money" : money_amount,
                                "name" : company_name,
                                "transaction_date" : date.today(),
                                "transaction_time" : datetime.now().time(),
                                "status" : Status.approved}
            await add_new_transaction(Transaction(**transaction_data), card.number)
            return {"message" : "Payment was successfully done"}
        else:
            raise HTTPException(status_code=400, detail="This card is frozen")
    else:
        raise HTTPException(status_code=404, detail="There is no card with this id")
