import typing as t
from uuid import UUID

import sqlalchemy
from sqlalchemy.sql import or_

from ...db.base import database
from ...db.tables import UserTable
from ..schemas import UserInDB


class UserRepository:
    def __init__(self):
        self._db = database

    @property
    def _table(self) -> sqlalchemy.Table:
        return UserTable

    async def get_all_users(self, offset: int = 0, limit: int = 100) -> t.List[t.Mapping]:
        query = self._table.select().offset(offset).limit(limit)
        return await self._db.fetch_all(query=query)

    async def get_user_by_username_or_email(self, username: str = None, email: str = None) -> t.Mapping:
        query = self._table.select().where(or_(self._table.c.username == username, self._table.c.email == email))
        return await self._db.fetch_one(query)

    async def create_user(self, user: UserInDB) -> UserInDB:
        query = self._table.insert(values=user.dict())
        await self._db.execute(query=query, values=user.dict())
        return user

    async def get_user_by_id(self, user_id: UUID) -> UserInDB or None:
        query = self._table.select().where(self._table.c.id == user_id)
        user = await self._db.fetch_one(query)
        return UserInDB(**user) if user else None

    async def delete_user(self, user_id: UUID) -> t.Mapping:
        query = self._table.delete().where(self._table.c.id == user_id)
        return await self._db.execute(query)

    async def update_user(self, user: UserInDB) -> UserInDB:
        query = self._table.update().where(self._table.c.id == user.id)

        return await self._db.execute(query, values={'hashed_password': user.hashed_password})
