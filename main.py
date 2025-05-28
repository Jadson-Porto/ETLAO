import os
from dotenv import load_dotenv
from etl.etl import ETL

load_dotenv()

usuario = os.getenv("USUARIO")
senha = os.getenv("SENHA")
host = os.getenv("HOST")
banco = os.getenv("BANCO_DE_DADOS")

origem = "reservas_hotel.xlsx"
destino = f"mssql+pyodbc://{usuario}:{senha}@{host}/{banco}?driver=ODBC+Driver+17+for+SQL+Server"

etl = ETL(origem, destino)

etl.extract()
etl.transform()
etl.load()
