from sqlalchemy import Column, String, Text

from app.models.abstract_model import AbstractModel


class CharityProject(AbstractModel):
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return (f'CharityProject(name={self.name}, '
                f'full_amount={self.full_amount})')
