from fastapi import HTTPException, responses
from sqlalchemy.orm import Session
from datetime import datetime

from src.models.solicitacao_acesso_especial import TableSolicitacaoAcessoEspecial
from src.utils.tipo_solicitacao import SituacaoSolicitacao
from src.entities.SolicitacaoAcessoEspecial import SolicitacaoAcessoEspecial

from src.utils.buscar_usuario_api import buscar_usuario_api
from src.utils.buscar_turma_api import buscar_turma_api

from src.utils.mensagem import enviar_mensagem


async def consultar_estado_solicitacao(id_usuario: str, id_turma_destino: str, db: Session):
    solicitante = await buscar_usuario_api(id_usuario)
    turma = await buscar_turma_api(id_turma_destino)
    cadeira = turma["cadeiras"][0]

    if cadeira and turma and solicitante:
        existe_solicitacao = db.query(TableSolicitacaoAcessoEspecial).filter_by(
            id_turma=id_turma_destino,
            id_usuario=id_usuario,
            id_cadeira=cadeira["id"]
        ).first()

        if existe_solicitacao:
            return {
                "id_solicitacao": existe_solicitacao.id,
                "status_solicitacao": existe_solicitacao.situacao,
                "solicitante": solicitante["nome"],
                "turma": id_turma_destino
            }
        else:
            return {
                "message": "Nenhuma solicitação feita.",
                "status_solicitacao": None
            }


async def solicitar_acesso(id_usuario: str, id_turma_destino: str, db: Session):
    solicitante = await buscar_usuario_api(id_usuario)
    turma = await buscar_turma_api(id_turma_destino)
    cadeira = turma["cadeiras"][0]

    if cadeira and turma and solicitante:
        existe_solicitacao = db.query(TableSolicitacaoAcessoEspecial).filter_by(
            id_turma=id_turma_destino,
            id_usuario=id_usuario,
            id_cadeira=cadeira["id"]
        ).first()

        if not existe_solicitacao:
            nova_solicitacao = TableSolicitacaoAcessoEspecial(
                situacao=SituacaoSolicitacao.PENDDENTE,
                data_hora_pedido=datetime.now(),
                id_turma=id_turma_destino,
                id_cadeira=cadeira["id"],
                id_usuario=id_usuario,
            )

            db.add(nova_solicitacao)
            db.commit()
            db.refresh(nova_solicitacao)

            enviar_mensagem(
                "Recebei um pedidio de acesso especial. Verifique.")

            return {
                "message": "Solicitação pendente, aguarde a resposta do Professor.",
                "solicitacao": {
                    "id_solicitacao": nova_solicitacao.id,
                    "status_solicitacao": nova_solicitacao.situacao,
                    "solicitante": solicitante["nome"],
                    "turma": id_turma_destino
                }
            }
        return responses.JSONResponse(
            status_code=401,
            content={
                "message": "Já solicitou acesso especial para esta cadeira.",
                "turma": id_turma_destino,
                "cadeira": cadeira["id"],
                "status_solicitacao": existe_solicitacao.situacao.value,
                "solicitante": solicitante["nome"],
                "id_solicitacao": existe_solicitacao.id
            }
        )
    raise HTTPException(status_code=404, detail="Nenhuma cadeira em aulas.")


async def responder_pedido(id_solicitacao: int, aceitar: bool, db: Session):
    solicitacao_acesso = db.query(
        TableSolicitacaoAcessoEspecial).filter_by(id=id_solicitacao).first()
    if not solicitacao_acesso:
        raise HTTPException(
            status_code=400, detail="Nenhum pedido com esse id.")

    nova_solicitacao = SolicitacaoAcessoEspecial(
        id=solicitacao_acesso.id,
        situacao=solicitacao_acesso.situacao,
        data_hora_pedido=solicitacao_acesso.data_hora_pedido,
        data_hora_resposta=solicitacao_acesso.data_hora_resposta,
        id_turma=solicitacao_acesso.id_turma,
        id_cadeira=solicitacao_acesso.id_cadeira,
        estudante=solicitacao_acesso.id_usuario
    )

    resposta = nova_solicitacao.aceitar_acesso_especial(
        db) if aceitar else nova_solicitacao.negar_acesso_especial(db)
    return f"Pedido {'aceito' if resposta else 'rejeitado'}."


async def listar_solicitacoes_acesso_filtrado(db: Session, id_turma: str = None, id_cadeira: str = None):
    query = db.query(TableSolicitacaoAcessoEspecial)

    if id_turma:
        query = query.filter(
            TableSolicitacaoAcessoEspecial.id_turma == id_turma)
    if id_cadeira:
        query = query.filter(
            TableSolicitacaoAcessoEspecial.id_cadeira == id_cadeira)

    solicitacoes = query.all()
    resultado = []

    for s in solicitacoes:
        try:
            estudante_data = await buscar_usuario_api(s.id_usuario)
            resultado.append({
                "id": s.id,
                "situacao": s.situacao,
                "data_hora_pedido": s.data_hora_pedido,
                "data_hora_resposta": s.data_hora_resposta,
                "id_turma": s.id_turma,
                "id_cadeira": s.id_cadeira,
                "estudante": {
                    "id": estudante_data["id"],
                    "nome": estudante_data["nome"],
                }
            })
        except Exception as e:
            print(f"Erro ao buscar dados do estudante {s.estudante}: {e}")
            continue

    return resultado
