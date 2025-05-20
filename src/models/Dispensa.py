class Dispensa:
    def __init__(self, id: int, nota_p1: float, nota_p2: float, id_cadeira: int):
        self.id = id
        self.nota_p1 = nota_p1
        self.nota_p2 = nota_p2
        self.id_cadeira = id_cadeira    
    
    def calcular_media(self):
        return (self.nota_p1 + self.nota_p2)/2
    
    def verificar_elegibilidade(self):
        return self.calcular_media() >= 14
        