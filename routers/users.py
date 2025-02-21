from typing import Annotated
from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.engine import get_db
from oprations.users import UsersOpration
from schema._input import DeleteUserAccountInput, UpdateUserProfileInput, UserInput
from schema.jwt import JWTPayload
from utils.jwt import JWTHandler

router = APIRouter(
    # prefix = "/users"
         )


@router.post("/register")
async def register(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    data: UserInput = Body(),
):
    user = await UsersOpration(db_session).create(
        username=data.username,
        password=data.password,
    )
    return user


@router.get("/{username}/")
async def get_user_profile( db_session: Annotated[AsyncSession, Depends(get_db)],username: str):
    user_profile = await UsersOpration(db_session).get_user_by_username(username)
    return user_profile


@router.put("/")
async def user_update_profile(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    data: UpdateUserProfileInput = Body(),
):
    user_update = await UsersOpration(db_session).update_user_by_username(data.old_username, data.new_username)
    return user_update

'''@router.delete("/")
async def delete_user( db_session: Annotated[AsyncSession, Depends(get_db)],
    data: DeleteUserAccountInput = Body(),):
    user_delete = await UsersOpration(db_session).delete_user_by_username(data.username, data.password)
    return user_delete'''


@router.delete("/")
async def delete_user(
    db_session: Annotated[AsyncSession,Depends(get_db)],
    token_data: JWTPayload = Depends(JWTHandler.verify_token),
    ):
    user_delete = await UsersOpration(db_session).delete_user_by_username(token_data.username)
    return user_delete

@router.post("/login")
async def login_user( db_session: Annotated[AsyncSession, Depends(get_db)],
    data: UserInput = Body(),):
    token = await UsersOpration(db_session).login_user_by_username(data.username, data.password)
    return token