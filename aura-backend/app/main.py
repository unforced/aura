from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.db.graph_db import GraphDB
from app.api.v1 import auth, users, documents

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: connect to the graph database
    app.state.graph_db = GraphDB(
        uri=settings.NEO4J_URI,
        user=settings.NEO4J_USER,
        password=settings.NEO4J_PASSWORD,
    )
    yield
    # Shutdown: close the graph database connection
    app.state.graph_db.close()

app = FastAPI(title="Aura API", version="0.1.0", lifespan=lifespan)

app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["auth"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(documents.router, prefix=f"{settings.API_V1_STR}/documents", tags=["documents"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Aura API"} 