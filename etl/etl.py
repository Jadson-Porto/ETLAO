import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from modelos.cliente import Cliente
from modelos.data import Data
from modelos.quarto import Quarto
from modelos.status import Status
from modelos.reserva import Reserva
from etl.abstract_etl import AbstractETL


class ETL(AbstractETL):
    def __init__(self, origem, destino):
        super().__init__(origem, destino)
        engine = create_engine(destino)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def extract(self):
        try:
            print("Extraindo dados do Excel...")
            planilhas = ["cliente", "data", "quarto", "reserva", "status"]
            self._dados_extraidos = {
                sheet: pd.read_excel(self.origem, sheet_name=sheet)
                for sheet in planilhas
            }
            print("Extração concluída!")
        except Exception as e:
            print(f"Erro na extração: {e}")
            raise

    def transform(self):
        try:
            print("Transformando dados...")
            self.transformed_data = {}

            for nome, df in self._dados_extraidos.items():
                df = df.drop_duplicates().dropna(how='all')

                if nome == 'quarto':
                    print("Tratando dados da planilha Quarto...")
                    df = df.rename(columns=lambda x: x.strip())

                if nome == 'cliente':
                    print("Tratando dados da planilha Cliente...")

                    
                    def format_cpf(cpf):
                        cpf_num = ''.join(filter(str.isdigit, str(cpf)))
                        if len(cpf_num) == 11:
                            return f"{cpf_num[:3]}.{cpf_num[3:6]}.{cpf_num[6:9]}-{cpf_num[9:]}"
                        return cpf

                    df['Cpf'] = df['Cpf'].apply(format_cpf)

                    
                    def format_telefone(tel):
                        tel_num = ''.join(filter(str.isdigit, str(tel)))
                        return tel_num

                    df['Telefone'] = df['Telefone'].apply(format_telefone)

                if nome == 'reserva':
                    print("Tratando dados da planilha Reserva...")
                    df = df.rename(columns={
                        'Numero_reserva': 'Nro',
                        'Status_nome': 'Nome_status',
                        'Data_inicio_data': 'Data_inicio_data',
                        'Numero_quarto_data_inicio': 'Numero_quarto_data_inicio',
                        'Data_fim_data': 'Data_fim_data',
                        'Nro_quarto_data_fim': 'Nro_quarto_data_fim',
                        'Data_reserva': 'Data',
                        'Cliente_id': 'Id_cliente'
                    })

                    for col in ['Nro', 'Numero_quarto_data_inicio', 'Nro_quarto_data_fim', 'Id_cliente']:
                        if col in df.columns:
                            df[col] = df[col].astype(int)
                        else:
                            print(f"Coluna {col} não encontrada no DataFrame!")

                    for date_col in ['Data_inicio_data', 'Data_fim_data', 'Data']:
                        if date_col in df.columns:
                            df[date_col] = pd.to_datetime(df[date_col], errors='coerce').dt.date

                self.transformed_data[nome] = df

            print("Transformação concluída!")
        except Exception as e:
            print(f"Erro na transformação: {e}")
            raise



    def load(self):
        try:
            print("Carregando dados no banco...")

            
            for _, row in self.transformed_data.get('quarto', pd.DataFrame()).iterrows():
                quarto_obj = Quarto(
                    Nro=row.get('Nro'),
                    Preco=row.get('Preco'),
                    Descricao=row.get('Descricao')
                )
                self.session.merge(quarto_obj)
            self.session.commit()

            
            cliente_df = self.transformed_data.get('cliente', pd.DataFrame())

            if not cliente_df.empty:
                for _, row in cliente_df.iterrows():
                    cliente_existente = self.session.query(Cliente).filter_by(Id=row.get('Id')).first()

                    if cliente_existente:
                        print(f"Atenção: Cliente com ID {row.get('Id')} já existe no banco. Registro não será inserido novamente.")
                    else:
                        cliente_obj = Cliente(
                            Id=row.get('Id'),
                            Nome=row.get('Nome', 'Sem Nome'),
                            Telefone=row.get('Telefone', 'Sem Telefone'),
                            Cpf=row.get('Cpf', '000.000.000-00')
                        )
                        self.session.add(cliente_obj)

                self.session.commit()
            else:
                print("Planilha Cliente está vazia ou não encontrada!")

            
            for _, row in self.transformed_data.get('data', pd.DataFrame()).iterrows():
                existing_data = self.session.query(Data).filter_by(
                    Data=row.get('Data'),
                    Nro_quarto=row.get('Nro_quarto')
                ).first()

                if existing_data:
                    existing_data.Status = row.get('Status')
                else:
                    new_data = Data(
                        Data=row.get('Data'),
                        Nro_quarto=row.get('Nro_quarto'),
                        Status=row.get('Status')
                    )
                    self.session.add(new_data)

            self.session.commit()

            
            for _, row in self.transformed_data.get('status', pd.DataFrame()).iterrows():
                status_obj = Status(
                    Nome=row.get('Nome')
                )
                self.session.merge(status_obj)
            self.session.commit()

            
            for _, row in self.transformed_data.get('reserva', pd.DataFrame()).iterrows():
                
                for data_val, nro_quarto_col in [
                    (row.get('Data_inicio_data'), row.get('Numero_quarto_data_inicio')),
                    (row.get('Data_fim_data'), row.get('Nro_quarto_data_fim'))
                ]:
                    if data_val and nro_quarto_col:
                        existing_data = self.session.query(Data).filter_by(
                            Data=data_val,
                            Nro_quarto=nro_quarto_col
                        ).first()
                        if not existing_data:
                            print(f"Criando Data ausente para Data={data_val}, Nro_quarto={nro_quarto_col}")
                            new_data = Data(
                                Data=data_val,
                                Nro_quarto=nro_quarto_col,
                                Status=None
                            )
                            self.session.add(new_data)
                            self.session.flush()

                reserva_obj = Reserva(
                    Nro=row.get('Nro'),
                    Nome_status=row.get('Nome_status'),
                    Data_inicio_data=row.get('Data_inicio_data'),
                    Numero_quarto_data_inicio=row.get('Numero_quarto_data_inicio'),
                    Data_fim_data=row.get('Data_fim_data'),
                    Nro_quarto_data_fim=row.get('Nro_quarto_data_fim'),
                    Data=row.get('Data'),
                    Id_cliente=row.get('Id_cliente')
                )
                self.session.merge(reserva_obj)

            self.session.commit()

            print("Dados carregados com sucesso!!!")
        except Exception as e:
            self.session.rollback()
            print(f"Erro ao carregar no banco: {e}")
            raise

