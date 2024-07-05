from pydantic import BaseModel
from typing import List
from model.ne import NE


class NESchema(BaseModel):
    """ Define como uma nova nota de crédito deve ser representada """
    ug: int = 186258
    nc: str = "2024NC800111"
    id: str = "2024NE400355"
    valor: float = 25000
    
class NEBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome da NE. """
    id: str = "Teste"


class ListagemNESchema(BaseModel):
    """ Define como uma listagem de NE será retornada.
    """
    nes:List[NESchema]


def apresenta_nes(nes: List[NE]):
    """ Retorna uma representação do NE seguindo o schema definido em
        NEViewSchema.
    """
    result = []
    for ne in nes:
        result.append({
            "ug": ne.ug,
            "nc": ne.nc,
            "id": ne.id,
            "valor": ne.valor
        })

    return {"nes": result}


class NEViewSchema(BaseModel):
    """ Define como um NE será retornada
    """
    ug: int = 186258
    nc: str = "2024NC800111"
    id: str = "2024NE155440"
    valor: float = 25000

class NEDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    id: str

def apresenta_ne(ne: NE):
    """ Retorna uma representação de NE seguindo o schema definido em
        NEViewSchema.
    """
    return {
            "ug": ne.ug,
            "nc": ne.nc,
            "id": ne.id,
            "valor": ne.valor
    }
