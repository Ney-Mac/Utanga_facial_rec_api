def aluno_na_turma(turma: dict, id_estudante: str):
    for cadeira in turma.get("cadeiras", []):
        for estudante in cadeira["estudantes"]:
            if estudante["id"] == id_estudante:
                return True
    return False