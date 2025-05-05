from src.utils.TipoProva import TipoProva
from datetime import date

class Prova:
    def __init__(self, tipo: TipoProva, data: date):
        self.tipo = tipo
        self.data = data

    def oberTipo(self):
        return self.tipo
