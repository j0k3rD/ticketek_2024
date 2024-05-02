from sqlmodel import Field, SQLModel, Relationship
from pydantic import EmailStr
from enum import Enum

# -------------------------------------------------------------------------------------------------#


class Roles(str, Enum):
    admin = "admin"
    user = "user"


# -------------------------------------------------------------------------------------------------#


class Token(SQLModel):
    access_token: str | None
    refresh_token: str | None


# -------------------------------------------------------------------------------------------------#


class EventsBase(SQLModel):
    event_id: str
    created_at: str
    name: str
    description: str
    location: str
    organizer: str
    user_id: int = Field(default=None, foreign_key="user.id")


class Events(EventsBase, table=True):
    id: int = Field(default=None, primary_key=True)


# -------------------------------------------------------------------------------------------------#


class UserBase(SQLModel):
    name: str
    email: EmailStr
    phone: str
    dni: str


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    phone: str = Field(index=True, unique=True)
    dni: str = Field(index=True, unique=True)
