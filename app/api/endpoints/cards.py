from typing import Annotated
from fastapi import Depends, HTTPException, status, APIRouter, Query
from app.api.dependencies import get_current_active_user
from app.models.user import User, User_In_DB
from app.services.card_service import validate_card
from app.models.card import Payment_system, Card_In_DB


from app.core.db_core import add_new_card, get_all_cards, check_if_card_exists, freeze_card

from datetime import date

router = APIRouter()

@router.post("/Cards")
async def add_a_new_card(current_user : Annotated[User, Depends(get_current_active_user)],
                        number : Annotated[str, Query(min_length=16, max_length=16)],
                        carrier_name: str,
                        expires_date : date,
                        payment_system: Payment_system,
                        cvv : Annotated[str, Query(min_length=3, max_length=3)],
                        ):
    if await check_if_card_exists(number, current_user.username):
        raise HTTPException(status_code=400, detail="Card already exists")
    card_data = {"number":number,
                 "carrier_name":carrier_name,
                 "expires_date":expires_date,
                 "payment_system":payment_system,
                 "cvv":cvv}
    await add_new_card(Card_In_DB(**card_data), current_user.username)
    return {"message" : "You added new card"}

@router.get("/Cards")
async def show_all_my_cards(current_user : Annotated[User, Depends(get_current_active_user)]):
    cards = await get_all_cards(current_user.username)
    if cards:
        return cards
    else:
        return {"message" : "You have no cards"}

@router.delete("/Cards")
async def freeze_my_card(current_user : Annotated[User, Depends(get_current_active_user)],
                      number : Annotated[str, Query(min_length=16, max_length=16)],):
    if await check_if_card_exists(number, current_user.username):
        frozen = await freeze_card(number, current_user.username)
        if frozen:
            return {"message":"This card is frozen"}
        else:
            raise HTTPException(status_code=400, detail="Something went wrong")
    raise HTTPException(status_code=404, detail="There is no card with this number")