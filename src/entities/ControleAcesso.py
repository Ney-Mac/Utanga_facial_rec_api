from sqlalchemy.orm import Session
from src.models.controle_acesso import TableControleAcesso
from fastapi import HTTPException

from src.utils.tipo_acesso import TipoAcesso
from datetime import date, time
from typing import Optional
from src.utils.mensagem import enviar_mensagem


class ControleAcesso:
    def __init__(self, data_criacao: date, hora_criacao: time, tipo: TipoAcesso, id_turma: str, id_cadeira: str, id_usuario: Optional[int] = None):
        self.data_criacao = data_criacao
        self.hora_criacao = hora_criacao
        self.tipo = tipo
        self.id_turma = id_turma
        self.id_cadeira = id_cadeira
        self.id_usuario = id_usuario

    def registrar_entrada(self, db: Session):
        novo_acesso = TableControleAcesso(
            data_criacao=self.data_criacao,
            hora_criacao=self.hora_criacao,
            tipo=self.tipo,
            id_turma=self.id_turma,
            id_cadeira=self.id_cadeira,
            id_usuario=self.id_usuario
        )

        try:
            db.add(novo_acesso)
            db.commit()
            db.refresh(novo_acesso)
            
            if self.tipo == TipoAcesso.REJEITADO:
                enviar_mensagem(
                    "Alerta: Houve uma tentativa de acesso.\n"
                    "Detalhes:\n"
                    f"Data: {self.data_criacao}"
                    f"Hora: {self.hora_criacao}"
                    f"Turma: {self.id_turma}"
                    f"Estado: {self.tipo}"
                )
        except Exception as e:
            print(f"Erro ao adiconar ControleAcesso: {e}")
            raise HTTPException(status_code=500, detail="Erro ao registar Acesso.")

    def verificar_status(self):
        return f"Acesso {str(self.tipo).lower()}"
