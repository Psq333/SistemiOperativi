class Transazione:
    def __init__(self, s_id, d_id, valore) -> None:
        self.sorgente = s_id
        self.destinazione = d_id
        self.valore = valore
    
    def printTransazione(self):
        print("Sorgente: " + str(self.sorgente) + " Destinazione: " + str(self.destinazione) + " Saldo: " + str(self.valore))