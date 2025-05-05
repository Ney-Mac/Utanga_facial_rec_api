from src.utils.TipoUsuario import TipoUsuario


class Usuario:
    def __init__(self, nome: str, tipo: TipoUsuario, codigo_acesso: str, foto_hash: str):
        self.nome = nome
        self.tipo = tipo
        self.codigo_acesso = codigo_acesso
        self.foto_hash = foto_hash

    def autenticar(self):
        return "autenticar"

    def obterPerfil(self):
        return "obterPerfil"
