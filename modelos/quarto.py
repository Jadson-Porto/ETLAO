from sqlalchemy import Column, Integer, Float, String
from modelos.base import Base

class Quarto(Base, Base.Base):
    __tablename__ = "Quarto"

    Nro = Column(Integer, primary_key=True)
    Preco = Column(Float, nullable=False)
    Descricao = Column(String(100))
