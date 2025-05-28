from sqlalchemy import Column, Integer, String, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from modelos.base import Base, BaseMixin

class Data(Base, BaseMixin):
    __tablename__ = "Data"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Data = Column(Date, nullable=False)
    Nro_quarto = Column(Integer, ForeignKey('Quarto.Nro'), nullable=False)
    Status = Column(String(50))

    __table_args__ = (
        UniqueConstraint('Data', 'Nro_quarto', name='UQ_Data_Data_NroQuarto'),
    )

    # Relacionamentos com Reserva (opcional, se quiser fazer)
    reservas_inicio = relationship(
        "Reserva",
        foreign_keys="[Reserva.Data_inicio_data, Reserva.Numero_quarto_data_inicio]",
        back_populates="data_inicio"
    )

    reservas_fim = relationship(
        "Reserva",
        foreign_keys="[Reserva.Data_fim_data, Reserva.Nro_quarto_data_fim]",
        back_populates="data_fim"
    )
