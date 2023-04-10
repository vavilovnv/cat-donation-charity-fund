from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    pass


class DonationView(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDB(DonationView):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
