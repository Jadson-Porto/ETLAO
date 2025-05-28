from sqlalchemy import Column, Integer, Float, String
from modelos.base import Base, BaseMixin

class Quarto(Base, BaseMixin):
    __tablename__ = "Quarto"

    Nro = Column(Integer, primary_key=True)
    Preco = Column(Float, nullable=False)
    Descricao = Column(String(100))
