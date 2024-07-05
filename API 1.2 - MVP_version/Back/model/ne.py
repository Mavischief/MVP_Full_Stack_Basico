from sqlalchemy import Column, String, Integer, DateTime, Float

from  model import Base

"""cria uma nota de empenho e adiciona o item a tabela_NE"""

class NE(Base):
    __tablename__ = 'tabela_NE'

    ug = Column(Integer, primary_key=True)
    nc = Column(String(12))
    id = Column(String, primary_key=True)
    valor = Column(Float)
	
    def __init__(self, ug:int, nc:str, id:str, valor:float):
        self.ug = ug
        self.nc = nc
        self.id = id
        self.valor = valor
