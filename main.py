from fastapi import FastAPI
from app.api.endpoints import auth

app = FastAPI(title="Virtual cards api", version="1.0.0")

app.include_router(auth.router, prefix = "/authentication", tags=["Authentication"])

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI App"}