from sqlalchemy import Column, String, Integer, DateTime, Float

from  model import Base

"""cria uma nota de crédito e adiciona o item a tabela_NC"""

class NC(Base):
    __tablename__ = 'tabela_NC'

    uasg = Column(Integer, primary_key=True)
    id = Column(String, primary_key=True)
    valor = Column(Float)
    nd = Column(String(8), nullable=True)
    aplicacao = Column(String(140), nullable=True)
    descricao = Column(String(12))

    def __init__(self, uasg:int, id:str, valor:float, nd:str, aplicacao:str, descricao:str):
        self.uasg = uasg
        self.id = id
        self.valor = valor
        self.nd = nd
        self.aplicacao = aplicacao
        self.descricao = descricao
