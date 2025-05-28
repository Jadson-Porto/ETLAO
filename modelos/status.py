from sqlalchemy import Column, String
from modelos.base import Base, BaseMixin

class Status(Base, BaseMixin):
    __tablename__ = "Status"

    Nome = Column(String(20), primary_key=True)
