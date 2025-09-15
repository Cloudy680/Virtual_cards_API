from fastapi import FastAPI, Depends
from typing import Annotated
from app.api.endpoints import auth
from app.api.endpoints import cards
from app.api.dependencies import get_current_active_user
from app.models.user import User

app = FastAPI(title="Virtual cards api", version="1.0.0")

app.include_router(auth.router, prefix = "/authentication", tags=["Authentication"])
app.include_router(cards.router, prefix = "/Cards", tags = ["Cards"])

@app.get("/Check", tags = ["Check"])
async def check(current_user : Annotated[User, Depends(get_current_active_user)] ):
    if current_user.full_name:
        return {"message": f"Welcome to FastAPI App {current_user.full_name}!"}
    else:
        return {"message": f"Welcome to FastAPI App {current_user.username}!"}