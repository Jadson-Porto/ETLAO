from sqlalchemy import Column, Integer, String
from modelos.base import Base, BaseMixin

class User(Base, BaseMixin):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
