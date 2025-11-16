from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class UserCreate(BaseModel):
    email: str
    password: str
    name: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    email: str
    name: Optional[str]
    role: str

    class Config:
        orm_mode = True


class EstablishmentCreate(BaseModel):
    name: str
    address: Optional[str]
    phone: Optional[str]


class EstablishmentOut(EstablishmentCreate):
    id: int

    class Config:
        orm_mode = True


class ProfessionalCreate(BaseModel):
    name: str
    establishment_id: Optional[int]


class ProfessionalOut(ProfessionalCreate):
    id: int

    class Config:
        orm_mode = True


class ClientCreate(BaseModel):
    name: str
    phone: Optional[str]


class ClientOut(ClientCreate):
    id: int

    class Config:
        orm_mode = True


class AgendaCreate(BaseModel):
    professional_id: int
    cliente_id: Optional[int]
    start: datetime
    end: datetime
    description: Optional[str]


class AgendaOut(AgendaCreate):
    id: int

    class Config:
        orm_mode = True
