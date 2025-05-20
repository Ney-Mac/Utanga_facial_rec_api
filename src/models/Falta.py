from datetime import date


class Falta:
    def __init__(self, id: int, tipo_falta: str, data: date, id_cadeira: int):
        self.id = id
        self.tipo_falta = tipo_falta
        self.data = data
        self.id_cadeira = id_cadeira
        
    def registrar_falta(self):
        pass
    
    def verificar_faltas(self):
        pass
        