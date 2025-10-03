from typing import Annotated
from fastapi import Depends, HTTPException, status, APIRouter, Query
from app.api.dependencies import get_current_active_user
from app.models.user import User, User_In_DB
from app.services.card_service import validate_card
from app.models.card import Payment_system, Card_In_DB, Card_check_functions

from app.crud.card import Card_CRUD

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
    if await Card_check_functions.check_if_card_exists(number, current_user.username):
        raise HTTPException(status_code=400, detail="Card already exists")
    card_data = {"number":number,
                 "carrier_name":carrier_name,
                 "expires_date":expires_date,
                 "payment_system":payment_system,
                 "cvv":cvv}
    await Card_CRUD.add_new_card(Card_In_DB(**card_data), current_user.username)
    return {"message" : "You added new card"}

@router.get("/Cards")
async def show_all_my_cards(current_user : Annotated[User, Depends(get_current_active_user)]):
    cards = await Card_CRUD.get_all_cards(current_user.username)
    if cards:
        return cards
    else:
        return {"message" : "You have no cards"}

@router.delete("/Cards")
async def delete_this_card(current_user : Annotated[User, Depends(get_current_active_user)],
                      number : Annotated[str, Query(min_length=16, max_length=16)],):
    if await Card_check_functions.check_if_card_exists(number, current_user.username):
        if await Card_CRUD.delete_card(number, current_user.username):
            return {"message" : "This card is deleted"}
        else:
            return {"message" : "Something went wrong"}
    raise HTTPException(status_code=404, detail="There is no card with this number")

@router.post("/Cards/unfreeze")
async def unfreeze_this_card(current_user: Annotated[User, Depends(get_current_active_user)],
                            number : Annotated[str, Query(min_length=16, max_length=16)],
                            new_expires_date:date):
    if await Card_check_functions.check_if_card_exists(number, current_user.username):
        if await Card_check_functions.check_if_card_is_frozen(number, current_user.username):
            if await Card_CRUD.change_card_expires_date(number, current_user.username, new_expires_date):
                return {"message" : "This card is active now"}
            else:
                return {"message" : "Something went wrong with changing cards expires date"}
        else:
            return {"message" : "This card is not frozen"}
    else:
        return {"message" : "There is no card with this number"}


