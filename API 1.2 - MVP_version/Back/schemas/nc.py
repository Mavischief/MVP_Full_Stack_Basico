from pydantic import BaseModel
from typing import List
from model.nc import NC


class NCSchema(BaseModel):
    """ Define como uma nova nota de crédito deve ser representada """
    uasg: str = 160555
    id: str = "2024NC800111"
    valor: float = 35000
    nd: str = "339030"
    aplicacao: str = "PIT"
    descricao: str = "Exemplo de descrição"

class NCBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome da NC. """
    id: str = "Teste"


class ListagemNCSchema(BaseModel):
    """ Define como uma listagem de NC será retornada.
    """
    ncs:List[NCSchema]


def apresenta_ncs(ncs: List[NC]):
    """ Retorna uma representação do NC seguindo o schema definido em
        NCViewSchema.
    """
    result = []
    for nc in ncs:
        result.append({
            "uasg": nc.uasg,
            "id": nc.id,
            "valor": nc.valor,
            "nd": nc.nd,
            "aplicacao": nc.aplicacao,
            "descricao": nc.descricao            
        })

    return {"ncs": result}


class NCViewSchema(BaseModel):
    """ Define como um NC será retornada
    """
    uasg: int = 160555
    id: str = "2024NC800111"
    valor: float = 35000
    nd: str = "339030"
    aplicacao: str = "PIT"
    descricao: str = "Exemplo de descrição"


class NCDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    id: str

def apresenta_nc(nc: NC):
    """ Retorna uma representação de NC seguindo o schema definido em
        NCViewSchema.
    """
    return {
        "uasg": nc.uasg,
        "id": nc.id,
        "valor": nc.valor,
        "nd": nc.nd,
        "aplicacao": nc.aplicacao,
        "descricao": nc.descricao
    }
