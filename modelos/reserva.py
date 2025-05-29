from sqlalchemy import Column, Integer, String, Date, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from modelos.base import Base

class Reserva(Base, Base.Base):
    __tablename__ = "Reserva"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Nro = Column(Integer, nullable=False) 
    Nome_status = Column(String(20), nullable=True)

    Data_inicio_data = Column(Date, nullable=False)
    Numero_quarto_data_inicio = Column(Integer, nullable=False)

    Data_fim_data = Column(Date, nullable=False)
    Nro_quarto_data_fim = Column(Integer, nullable=False)

    Data = Column(Date, nullable=True)  
    Id_cliente = Column(Integer, nullable=True) 

    __table_args__ = (
        ForeignKeyConstraint(
            ['Data_inicio_data', 'Numero_quarto_data_inicio'],
            ['Data.Data', 'Data.Nro_quarto'],
            name='FK_Reserva_DataInicio'
        ),
        ForeignKeyConstraint(
            ['Data_fim_data', 'Nro_quarto_data_fim'],
            ['Data.Data', 'Data.Nro_quarto'],
            name='FK_Reserva_DataFim'
        ),
    )

    
    data_inicio = relationship(
        "Data",
        foreign_keys=[Data_inicio_data, Numero_quarto_data_inicio],
        back_populates="reservas_inicio"
    )

    data_fim = relationship(
        "Data",
        foreign_keys=[Data_fim_data, Nro_quarto_data_fim],
        back_populates="reservas_fim"
    )
