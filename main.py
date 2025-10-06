from datetime import datetime

from typing import Annotated

from fastapi import FastAPI, Depends

from app.core.sceduler import scheduler_manager
from app.core.db_core import create_tables

from app.api.endpoints import auth, cards, transactions, account
from app.api.dependencies import get_current_active_user

from app.models.user import User


app = FastAPI(title="Virtual cards api", version="1.0.0")


@app.on_event("startup")
async def startup_event():
    await create_tables()
    scheduler_manager.start_scheduler()

@app.on_event("shutdown")
async def shutdown_event():
    scheduler_manager.shutdown_scheduler()


app.include_router(auth.router, prefix = "/authentication", tags=["Authentication"])
app.include_router(cards.router, prefix = "/Cards", tags = ["Cards"])
app.include_router(transactions.router, prefix = "/Transaction", tags = ["Transactions"])
app.include_router(account.router, prefix = "/Account", tags = ["Account"])


@app.get("/Root", tags = ["Root"])
async def root():
    return {
        "message": "Card Service API",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health", tags = ["Check"])
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/User check", tags = ["Check"])
async def check(current_user : Annotated[User, Depends(get_current_active_user)] ):
    if current_user.name:
        return {"message": f"Welcome to FastAPI App {current_user.name}!"}
    else:
        return {"message": f"Welcome to FastAPI App {current_user.name}!"}


