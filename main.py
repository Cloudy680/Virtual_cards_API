from fastapi import FastAPI, Depends
from typing import Annotated
from app.api.endpoints import auth
from app.api.endpoints import cards
from app.api.dependencies import get_current_active_user
from app.models.user import User


from app.core.db_core import create_tables

app = FastAPI(title="Virtual cards api", version="1.0.0")


@app.on_event("startup")
async def startup_event():
    await create_tables()


app.include_router(auth.router, prefix = "/authentication", tags=["Authentication"])
app.include_router(cards.router, prefix = "/Cards", tags = ["Cards"])

@app.get("/Check", tags = ["Check"])
async def check(current_user : Annotated[User, Depends(get_current_active_user)] ):
    if current_user.name:
        return {"message": f"Welcome to FastAPI App {current_user.name}!"}
    else:
        return {"message": f"Welcome to FastAPI App {current_user.name}!"}