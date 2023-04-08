from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.abstract_model import AbstractModel


class Donation(AbstractModel):
    comment = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey('user.id', name='fk_donation_user_id_user'))
