from pydantic import BaseModel
from src.utils.DiaSemana import DiaSemana
from datetime import time

class TurmaResponse(BaseModel):
    codigo_turma: str
    sala: str
    dia_semana: DiaSemana
    hora_inicio: time
    hora_fim: time
    nome_cadeira: str
    codigo_cadeira: str
    professor_id: int
    
    class Config:
        use_enum_values: True
    
class CreateTurmaResponse(BaseModel):
    message: str
    turma: TurmaResponse

class TurmaAlunoResponse(BaseModel):
    aluno: str
    turma: str    
