from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, NC, NE
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
NC_tag = Tag(name="Nota de Crédito", description="Adição, visualização e remoção de notas de créito à base")
NE_tag = Tag(name="Nota de Empenho", description="Adição, visualização e remoção de notas de empenho à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/nc', tags=[NC_tag],
          responses={"200": NCViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_nc(form: NCSchema):
    """Adiciona um nova Nota de crédito à base de dados

    Retorna uma representação da nota de crédito e comentários associados.
    """
    nc = NC(
        uasg=form.uasg,
        id=form.id,
        valor=form.valor,
        nd=form.nd,
        aplicacao=form.aplicacao,
        descricao=form.descricao)
    logger.debug(f"Nota de crédito '{nc.id}' adicionada.")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando NC
        session.add(nc)
        # efetivando o comando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado nota de crédito de id: '{nc.id}'")
        return apresenta_nc(nc), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "NC de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar nota de crédito '{nc.id}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar nota de crédito '{nc.id}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/ncs', tags=[NC_tag],
         responses={"200": ListagemNCSchema, "404": ErrorSchema})
def get_ncs():
    """Faz a busca por todas notas de crédito cadastradas

    Retorna uma representação da listagem de notas de créditos.
    """
    logger.debug(f"Coletando notas de crédito ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    ncs = session.query(NC).all()

    if not ncs:
        # se não há notas cadastradas
        return {"nota de crédito": []}, 200
    else:
        logger.debug(f"%d notas de crédito emcontradas" % len(ncs))
        # retorna a representação de nota de crédito
        print(ncs)
        return apresenta_ncs(ncs), 200


@app.get('/nc', tags=[NC_tag],
         responses={"200": NCViewSchema, "404": ErrorSchema})
def get_nc(query: NCBuscaSchema):
    """Faz a busca por uma nota de crédito a partir da NC

    Retorna uma representação das notas de crédito.
    """
    NC_id = query.id
    logger.debug(f"Coletando dados sobre da nota #{NC_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    nc = session.query(NC).filter(NC.id == NC_id).first()

    if not nc:
        # se a nota não foi encontrado
        error_msg = "Nota não encontrada na base :/"
        logger.warning(f"Erro ao buscar nota de crédito '{NC_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Nota econtrada: '{nc.id}'")
        # retorna a representação de nota
        return apresenta_nc(nc), 200


@app.delete('/nc', tags=[NC_tag],
            responses={"200": NCDelSchema, "404": ErrorSchema})
def del_nc(query: NCBuscaSchema):
    """Deleta uma nota a partir do nome da nota informado

    Retorna uma mensagem de confirmação da remoção.
    """
    nc_id = unquote(unquote(query.id))
    print(nc_id)
    logger.debug(f"Deletando dados sobre nota #{nc_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(NC).filter(NC.id == nc_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Nota de crédito {nc_id} deletada")
        return {"mesage": "Nota de crédito removida", "id": nc_id}
    else:
        # se a nota não foi encontrado
        error_msg = "Nota não encontrado na base :/"
        logger.warning(f"Erro ao deletar nota de crédito #'{nc_id}', {error_msg}")
        return {"mesage": error_msg}, 404

@app.post('/ne', tags=[NE_tag],
          responses={"200": NEViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_ne(form: NESchema):
    """Adiciona um nova Nota de empenho à base de dados

    Retorna uma representação da nota de empenho e comentários associados.
    """
    ne = NE(
        ug=form.ug,
        nc=form.nc,
        id=form.id,
        valor=form.valor)
    logger.debug(f"Nota de empenho '{ne.id}' adicionada.")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando NE
        session.add(ne)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado nota de empenho de id: '{ne.id}'")
        return apresenta_ne(ne), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "NE de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar nota de empenho '{ne.id}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar nota de empenho '{ne.id}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/nes', tags=[NE_tag],
         responses={"200": ListagemNESchema, "404": ErrorSchema})
def get_nes():
    """Faz a busca por todas notas de empenho cadastradas

    Retorna uma representação da listagem de notas de empenhos.
    """
    logger.debug(f"Coletando notas de empenho ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    nes = session.query(NE).all()

    if not nes:
        # se não há notas cadastradas
        return {"nota de empenho": []}, 200
    else:
        logger.debug(f"%d notas de empenho emcontradas" % len(nes))
        # retorna a representação de nota de empenho
        print(nes)
        return apresenta_nes(nes), 200


@app.get('/ne', tags=[NE_tag],
         responses={"200": NEViewSchema, "404": ErrorSchema})
def get_ne(query: NEBuscaSchema):
    """Faz a busca por uma nota de empenho a partir da NE

    Retorna uma representação das notas de empenho.
    """
    NE_id = query.id
    logger.debug(f"Coletando dados sobre da nota #{NE_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    ne = session.query(NE).filter(NE.id == NE_id).first()

    if not ne:
        # se a nota não foi encontrado
        error_msg = "Nota não encontrada na base :/"
        logger.warning(f"Erro ao buscar nota de empenho '{NE_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Nota econtrada: '{ne.id}'")
        # retorna a representação de nota
        return apresenta_ne(ne), 200


@app.delete('/ne', tags=[NE_tag],
            responses={"200": NEDelSchema, "404": ErrorSchema})
def del_ne(query: NEBuscaSchema):
    """Deleta uma nota a partir do nome da nota informado

    Retorna uma mensagem de confirmação da remoção.
    """
    ne_id = unquote(unquote(query.id))
    print(ne_id)
    logger.debug(f"Deletando dados sobre nota #{ne_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(NE).filter(NE.id == ne_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Nota de empenho {ne_id} deletada")
        return {"mesage": "Nota de empenho removida", "id": ne_id}
    else:
        # se a nota não foi encontrado
        error_msg = "Nota não encontrado na base :/"
        logger.warning(f"Erro ao deletar nota de empenho #'{ne_id}', {error_msg}")
        return {"mesage": error_msg}, 404
