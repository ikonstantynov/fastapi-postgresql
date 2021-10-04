import typing as t
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response

from fastapi_postgresql.core.security import get_password_hash
from fastapi_postgresql.db import schemas
from fastapi_postgresql.db.repositories.user import UserRepository
from fastapi_postgresql.db.schemas import UserInDB

router = APIRouter()


@router.get('/users', response_model=t.List[schemas.User])
async def get_users(offset: int = 0, limit: int = 100):
    return await UserRepository().get_all_users(offset, limit)


@router.post('/users', response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: schemas.UserCreate):
    user = await UserRepository().get_user_by_username_or_email(username=user_in.username, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username or email already exists in the system.",
        )
    db_user = UserInDB(
        id=user_in.id,
        username=user_in.username,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
    )
    return await UserRepository().create_user(db_user)


@router.get('/users/{user_id}', response_model=schemas.User)
async def get_user(user_id: UUID):
    user = await UserRepository().get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@router.put('/users/{user_id}/password', response_model=schemas.User)
async def update_user_password(user_id: UUID, user_in: schemas.UserUpdate):
    user = await UserRepository().get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    user.hashed_password = get_password_hash(user_in.password)
    await UserRepository().update_user(user)
    return user


@router.delete('/users/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID):
    user = await UserRepository().get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    await UserRepository().delete_user(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
