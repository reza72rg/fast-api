import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from db.models import User
from sqlalchemy.future import select


class UsersOpration:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(self, username: str, password: str):
        query = sa.select(User).where(User.username == username)

        async with self.db_session as session:
            user_data = await session.scalar(query)

            if user_data:
                raise HTTPException(status_code=409, detail=f"User {username} already exists")

            user = User(password=password, username=username)
            session.add(user)

            await session.commit()
            await session.refresh(user)

        return {"id": user.id, "username": user.username}

    async def get_user_by_username(self, username: str ):
        query = sa.select(User).where(User.username == username)
        async with self.db_session as session:
            user_data = await session.scalar(query)
            if user_data is None:
                raise HTTPException(status_code=404, detail="User do not exists")
            return user_data

    async def update_user_by_username(self, old_username: str , new_username: str):
        query = sa.select(User).where(User.username == old_username)
        new_query = sa.select(User).where(User.username == new_username)
        update_query = sa.update(User).where(User.username == old_username).values(username = new_username)

        async with self.db_session as session:
            user_data = await session.scalar(query)
            new_user = await session.scalar(new_query)
            if user_data is None:
                raise HTTPException(status_code=404, detail=f"User {old_username} do not exists")
            if new_user:
                raise HTTPException(status_code=409, detail=f"User {new_username} already exists")

            await session.execute(update_query)
            await session.commit()
            user_data.username = new_username
            return {"id": user_data.id, "username": user_data.username}

    async def delete_user_by_username(self, username: str, password: str):
        async with self.db_session as session:
            result = await session.execute(select(User).where(User.username == username, User.password == password))
            wrong_password = await session.execute(select(User).where(User.username == username, User.password != password))
            user_data = result.scalar_one_or_none()
            user_wrong_password = wrong_password.scalar_one_or_none()

            if user_wrong_password:
                raise HTTPException(status_code=404, detail=f"User {username} wrong password")

            if user_data is None:
                raise HTTPException(status_code=404, detail=f"User {username} do not exists")


            await session.delete(user_data)
            await session.commit()
            return {"details": "user is delete successfully"}