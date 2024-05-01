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


class ServiceBase(SQLModel):
    date: str
    name: str
    company_id: int = Field(default=None, foreign_key="company.id")
    service_type: str
    scrapping_type: str
    scrapping_config: str


class Service(ServiceBase, table=True):
    id: int = Field(default=None, primary_key=True)


# -------------------------------------------------------------------------------------------------#


class UserBase(SQLModel):
    name: str
    email: EmailStr
    phone: str
    password: str
    role: Roles = Field(default="user")
    disabled: bool | None = None


class UserCreate(UserBase):
    password: str

class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    phone: str = Field(index=True, unique=True)
