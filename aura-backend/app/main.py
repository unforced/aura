from fastapi import FastAPI
from app.core.config import settings
from app.api.v1 import auth as auth_router
from app.api.v1 import users as users_router
from app.api.v1 import documents as documents_router

app = FastAPI(title=settings.PROJECT_NAME)

@app.get("/")
def read_root():
    return {"message": "Welcome to Aura"}

app.include_router(auth_router.router, prefix=settings.API_V1_STR, tags=["auth"])
app.include_router(users_router.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(documents_router.router, prefix=f"{settings.API_V1_STR}/documents", tags=["documents"]) 