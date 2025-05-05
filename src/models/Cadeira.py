class Cadeira:
    def __init__(self, nome: str, codigo: str):
        self.nome = nome
        self.codigo = codigo

    def obterDescricao(self):
        return f"Cadeira: {self.nome}; Código: {self.codigo}"