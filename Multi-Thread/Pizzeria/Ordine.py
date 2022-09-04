import string


class Ordine:
    def __init__(self, n_o, id_pizza, quantita):
        self.numero_ordine = n_o
        self.id = id_pizza
        self.quantita = quantita
    
    def get_N_ordine(self):
        return self.numero_ordine


    def printOrdine(self):
        print (str(self.numero_ordine) + ": <" + str(self.id) + "," + str(self.quantita) + ">")

#o = Ordine("1","20")
#o.printOrdine("1")

