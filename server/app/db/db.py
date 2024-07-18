from datetime import datetime
from databases.core import Database

from .migration import apply_migrations
from .migrations_to_apply import MIGRATIONS

from typing import Optional
from sqlmodel import Field, SQLModel

from sqlalchemy.types import JSON


def current_date():
    return datetime.now().isoformat()

class User(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    username: str = Field(unique=True)
    email: str = Field(unique=True)
    password: str
    pincode: int
    name: Optional[str] = None
    number: Optional[str] = None
    address: Optional[str] = None
    joined_on: str = Field(default_factory=current_date)
    latitude: float   
    longitude: float
class Topic(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    name: str = Field(unique=True)

class UserTopic(SQLModel, table=True):
    __tablename__: str = "user_topic" # type: ignore
    id: int = Field(primary_key=True, default=None)
    topic_id: int = Field(foreign_key="topic.id")
    user_id: int = Field(foreign_key="user.id")

class Session(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    user_id: int = Field(foreign_key="user.id")
    token: str = Field(unique=True)

class Message(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    client_id: str = Field(unique=True)
    sender: int = Field(foreign_key="user.id")
    reciever: int = Field(foreign_key="user.id")
    content: str
    sent_at: str = Field(default_factory=current_date)

class FriendRequest(SQLModel, table=True):
    __tablename__: str = "friend_request" # type: ignore
    id: int = Field(primary_key=True, default=None)
    sender: int = Field(foreign_key="user.id")
    reciever: int = Field(foreign_key="user.id")
    
