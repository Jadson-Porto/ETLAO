from abc import ABC, abstractmethod


class AbstractETL(ABC):
    def __init__(self, origem: str, destino: str):
        self.origem = origem
        self.destino = destino
        self._dados_extraidos = None
        self.transformed_data = None

    @abstractmethod
    def extract(self):
        pass

    @abstractmethod
    def transform(self):
        pass

    @abstractmethod
    def load(self):
        pass

