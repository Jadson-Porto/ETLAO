# from typing import List, Type

# import pandas as pd
# from sqlalchemy.ext.declarative import declarative_base

# class Base:
#     Base = declarative_base()

#     @classmethod
#     def from_dataframe(cls: Type["Base"], df: pd.DataFrame) -> List["Base"]:
#         """
#         Este método converte os registros de um DataFrame em uma lista de objetos a serem incluídos no banco de dados
#         """
#         objects = []
#         for _, row in df.iterrows():
#             row = row.dropna()
#             instance = cls(**row.to_dict())
#             objects.append(instance)
#         return objects

from sqlalchemy.orm import declarative_base
import pandas as pd
from typing import List, Type

Base = declarative_base()

class BaseMixin:
    @classmethod
    def from_dataframe(cls: Type["BaseMixin"], df: pd.DataFrame) -> List["BaseMixin"]:
        objects = []
        for _, row in df.iterrows():
            instance = cls(**row.dropna().to_dict())
            objects.append(instance)
        return objects

