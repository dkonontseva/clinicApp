from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

DATABASE_URL = settings.get_db_url()

engine = create_async_engine(url=DATABASE_URL, echo=True)
# Создаем фабрику сессий для взаимодействия с базой данных
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

def get_db():
    db = async_session_maker()
    try:
        yield db
    finally:
        db.close()

# Базовый класс для всех моделей
class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True