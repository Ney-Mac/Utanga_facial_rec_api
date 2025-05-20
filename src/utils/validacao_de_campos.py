from fastapi import HTTPException


def validar_campos_por_tipo(tipo: str, matricula, curso, ano_lectivo, id_turma):
    if tipo == 'aluno':
        if not all([matricula, curso, ano_lectivo, id_turma]):
            raise HTTPException(status_code=400, detail="Campos obrigatórios para aluno não informados.")
    elif tipo == 'prof':
        if any([matricula, curso, ano_lectivo]):
            raise HTTPException(status_code=400, detail="Professor não deve ter matrícula, curso ou ano letivo.")
    elif tipo == "adm":
        if any([matricula, curso, ano_lectivo, id_turma]):
            raise HTTPException(status_code=400, detail="Administrador não deve ter matrícula, curso, turma ou ano letivo.")
    else:
        raise HTTPException(status_code=400, detail="Tipo inválido.")    
    