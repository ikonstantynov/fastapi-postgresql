from sqlalchemy import Column, DateTime, String, Table
from sqlalchemy.dialects.postgresql import UUID

from ..db.base import metadata

UserTable = Table(
    'user',
    metadata,
    Column('id', UUID(), primary_key=True),
    Column('username', String),
    Column('email', String),
    Column('hashed_password', String),
    Column('register_date', DateTime),
)
