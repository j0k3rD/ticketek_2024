from sqlmodel import Field, SQLModel, Relationship, AutoString
from pydantic import EmailStr
from enum import Enum
from datetime import datetime
from typing import Dict
from sqlalchemy import Column, JSON

# -------------------------------------------------------------------------------------------------#


# class Roles(str, Enum):
#     admin = "admin"
#     user = "user"


# -------------------------------------------------------------------------------------------------#


# class Token(SQLModel):
#     access_token: str | None
#     refresh_token: str | None


# -------------------------------------------------------------------------------------------------#


class EventBase(SQLModel):
    title: str
    description: str
    max_attendees: int
    # Lista para almacenar los usuarios aprobados
    attendees: Dict = Field(default_factory=dict, sa_column=Column(JSON))


class Event(EventBase, table=True):
    id: int = Field(default=None, primary_key=True)
    location: Dict = Field(default_factory=dict, sa_column=Column(JSON))
    date: datetime
    registrations: list["Registration"] = Relationship(back_populates="event")


# -------------------------------------------------------------------------------------------------#


class RegistrationStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class RegistrationBase(SQLModel):
    name: str
    email: EmailStr = Field(unique=True, index=True, sa_type=AutoString)
    phone: str
    dni: int
    status: RegistrationStatus = RegistrationStatus.pending
    token: str = Field(default=None)
    event_id: int = Field(foreign_key="event.id")


class Registration(RegistrationBase, table=True):
    id: int = Field(default=None, primary_key=True)
    # email: str = Field(index=True, unique=True)
    # dni: str = Field(index=True, unique=True)
    event: "Event" = Relationship(back_populates="registrations")
