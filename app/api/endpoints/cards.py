from typing import Annotated
from fastapi import Depends, HTTPException, status, APIRouter, Query
from app.api.dependencies import get_current_active_user
from app.models.user import User, User_In_DB
from app.services.card_validate_service import validate_card_by_luna_algorithm
from app.models.card import Payment_system, Card_In_DB, Card_check_functions, Card

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
    if validate_card_by_luna_algorithm(number):
        if await Card_check_functions.check_if_card_exists(number, current_user.username):
            raise HTTPException(status_code=400, detail="Card already exists")
        card_data = {"number":number,
                     "carrier_name":carrier_name,
                     "expires_date":expires_date,
                     "payment_system":payment_system,
                     "cvv":cvv}
        await Card_CRUD.add_new_card(Card_In_DB(**card_data), current_user.username)
        return {"message" : "You added new card"}
    else:
        raise HTTPException(status_code=400, detail="A card with this number cannot exist")

@router.get("/Cards")
async def show_all_my_cards(current_user : Annotated[User, Depends(get_current_active_user)]):
    cards = await Card_CRUD.get_all_cards(current_user.username)
    if cards:
        return cards
    else:
        raise HTTPException(status_code=404, detail="You have no cards")

@router.delete("/Cards")
async def delete_this_card(current_user : Annotated[User, Depends(get_current_active_user)],
                           id : int):
    card = await Card_CRUD.get_card_by_id(id, current_user.username)
    if card is not None:
        if await Card_CRUD.delete_card(id, current_user.username):
            return {"message" : "This card is deleted"}
        else:
            return {"message" : "Something went wrong with deleting this card"}
    else:
        raise HTTPException(status_code=404, detail="There is no card with this id")

@router.post("/Cards/unfreeze")
async def unfreeze_this_card(current_user: Annotated[User, Depends(get_current_active_user)],
                            id : int,
                            new_expires_date:date):
    card = await Card_CRUD.get_card_by_id(id, current_user.username)
    if card is not None:
        if await Card_CRUD.change_card_expires_date(id, current_user.username, new_expires_date):
            return {"message" : "This card is active now"}
        else:
            return {"message" : "Something went wrong with changing cards expires date"}
    else:
        raise HTTPException(status_code=404, detail="There is no card with this id")


