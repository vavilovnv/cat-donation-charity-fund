from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, validator


class CharityProjectUpdate(BaseModel):
    name: str = Field(None, min_length=1, max_length=100)
    description: str = Field(None, min_length=1)
    full_amount: int = Field(None, gt=0)

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectUpdate):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: int = Field(..., gt=0)

    @validator('name', 'description')
    def check_value_is_empty(cls, value: str):
        if value is None or not value:
            raise ValueError('Поля обязательны для заполнения.')
        return value


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
