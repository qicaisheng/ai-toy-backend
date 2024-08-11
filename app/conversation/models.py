import uuid
from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel
from sqlmodel import SQLModel, Field, JSON, Column


class Conversation(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID
    created_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Author(BaseModel):
    role: str
    name: str


class Message(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field()
    content: str
    audio_id: Optional[str] = None
    author: dict = Field(sa_column=Column(JSON))
    parent_id: Optional[uuid.UUID] = Field(default=None)
    created_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class MessageBase(SQLModel):
    conversation_id: uuid.UUID
    content: str
    parent_id: Optional[uuid.UUID]


class UserMessageCreate(BaseModel):
    conversation_id: Optional[uuid.UUID]
    content: str
    audio_id: Optional[str] = None
    parent_id: Optional[uuid.UUID] = None
