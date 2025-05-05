from datetime import datetime


class RegistroAcesso:
    def __init__(self, data_hora, autorizado: bool, motivo: str):
        self.data_hora = data_hora
        self.autorizado = autorizado
        self.motivo = motivo

    def registrar(self) -> bool:
        print("Salvar na BD")
        return True
