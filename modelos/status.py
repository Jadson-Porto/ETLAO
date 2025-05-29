from sqlalchemy import Column, String
from modelos.base import Base

class Status(Base, Base.Base):
    __tablename__ = "Status"

    Nome = Column(String(20), primary_key=True)
