from sqlalchemy import Column, Integer, String, Date, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from modelos.base import Base, BaseMixin

class Reserva(Base, BaseMixin):
    __tablename__ = "Reserva"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Nro = Column(Integer, nullable=False)  # Número da reserva
    Nome_status = Column(String(20), nullable=True)

    Data_inicio_data = Column(Date, nullable=False)
    Numero_quarto_data_inicio = Column(Integer, nullable=False)

    Data_fim_data = Column(Date, nullable=False)
    Nro_quarto_data_fim = Column(Integer, nullable=False)

    Data = Column(Date, nullable=True)  # Outro dado qualquer
    Id_cliente = Column(Integer, nullable=True)  # FK opcional a Cliente

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

    # Relacionamentos
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
