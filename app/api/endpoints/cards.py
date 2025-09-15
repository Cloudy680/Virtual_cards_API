from typing import Annotated
from fastapi import Depends, HTTPException, status, APIRouter, Query
from app.api.dependencies import get_current_active_user
from app.models.user import User

router = APIRouter()

@router.post("/Cards")
async def get_a_new_card(current_user : Annotated[User, Depends(get_current_active_user)]):
    return {"message" : "You created a new card"}

@router.get("/Cards")
async def products(current_user : Annotated[User, Depends(get_current_active_user)]):
    return {"message" : "There are all you cards"}

@router.delete("/Cards")
async def freeze_card(current_user : Annotated[User, Depends(get_current_active_user)]):
    return {"message": "Your card is frozen"}