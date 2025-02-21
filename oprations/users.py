import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from db.models import User
from sqlalchemy.future import select
from exception import UserNotFound, UserAlreadyExists, IncorrectPassword
from secret import password_manager
from schema.output import RegisterOutput
from sqlalchemy.exc import IntegrityError
class UsersOpration:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session


    async def create(self, username: str, password: str):
        user_pwd = password_manager.hash(password)
        user = User(password=user_pwd, username=username)
        async with self.db_session as session:
            try:
                session.add(user)
                await session.commit()
                await session.refresh(user)
            except IntegrityError:
                raise UserAlreadyExists

        #return {"id": user.id, "username": user.username, "password": user.password}
        return RegisterOutput(username= user.username, id= user.id)

    '''async def create(self, username: str, password: str):
        query = sa.select(User).where(User.username == username)

        async with self.db_session as session:
            user_data = await session.scalar(query)

            if user_data:
                raise HTTPException(status_code=409, detail=f"User {username} already exists")
            user_pwd = password_manager.hash(password)
            user = User(password=user_pwd, username=username)
            session.add(user)

            await session.commit()
            await session.refresh(user)

        #return {"id": user.id, "username": user.username, "password": user.password}
        return RegisterOutput(username= user.username, id= user.id)'''

    async def get_user_by_username(self, username: str ):
        query = sa.select(User).where(User.username == username)
        async with self.db_session as session:
            user_data = await session.scalar(query)
            if user_data is None:
                raise UserNotFound("/get user")
            return user_data

    async def update_user_by_username(self, old_username: str , new_username: str):
        query = sa.select(User).where(User.username == old_username)
        new_query = sa.select(User).where(User.username == new_username)
        update_query = sa.update(User).where(User.username == old_username).values(username = new_username)

        async with self.db_session as session:
            user_data = await session.scalar(query)
            new_user = await session.scalar(new_query)
            if user_data is None:
                raise UserNotFound("/update")
            if new_user:
                raise UserNotFound("/update")

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

    async def login_user_by_username(self, username: str, password: str):
        query = sa.select(User).where(User.username == username)
        async with self.db_session as session:
            user_data = await session.scalar(query)
            if user_data is None:
                raise UserNotFound("/login")
            if not password_manager.verify(password, user_data.password):
                raise IncorrectPassword("/login")

            return "login yes"

