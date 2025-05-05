from src.models.Usuario import Usuario
from src.models.Aluno import Aluno
from src.models.Prova import Prova
from src.models.NotaProva import NotaProva
from src.utils.TipoUsuario import TipoUsuario
from src.utils.NivelAdmin import NivelAdmin


class Administrador(Usuario):
    def __init__(self, nome: str, numFuncionario: str, foto_hash: str, nivel: NivelAdmin):
        super().__init__(nome, TipoUsuario.ADMIN, numFuncionario, foto_hash)
        self.nivel = nivel

    def criarUsuario(self, usuario: Usuario, tipo: TipoUsuario) -> Usuario:
        return

    def lancarNota(self, aluno: Aluno, prova: Prova, nota: float) -> NotaProva:
        return
