from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./blog.db"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase, MappedAsDataclass):
    pass


async def get_db():
    async with SessionLocal() as db:
        yield db
