from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_current_active_user

from app.models.user import User

from app.crud.user import user_CRUD_operations

router = APIRouter()


@router.get("/Get info", response_model=User)
async def get_my_account_info(current_user : Annotated[User, Depends(get_current_active_user)]):
    return current_user


@router.delete("/Delete account")
async def delete_this_account(current_user : Annotated[User, Depends(get_current_active_user)]):
    result = await user_CRUD_operations.delete_account_by_username(current_user.username)
    if result:
        return {"message" : "This account is deleted"}
    else:
        raise HTTPException(status_code=400, detail="Something went wrong")
