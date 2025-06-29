from sqlmodel import create_engine, Session
from app.core.config import settings

if settings.DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not set in the environment or .env file")

engine = create_engine(str(settings.DATABASE_URL), echo=True)

def get_db():
    with Session(engine) as session:
        yield session 