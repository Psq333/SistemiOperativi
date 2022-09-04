from threading import RLock, Condition
from Ordine import Ordine


class Pizzeria:

    def __init__(self, O, P):
        self.BO = []
        self.dimBO = O

        self.BP = {}
        self.dimBP = P

        self.numero_ordini = -1
        self.lock = RLock()
        self.condition_cliente = Condition(self.lock)
        self.condition_pizzaiolo = Condition(self.lock)

    def putOrdine(self,id,quantita):    #verrà richiamato dal cliente
        with self.lock:
            while self.dimBO == len(self.BO):
                self.condition_cliente.wait()
            self.numero_ordini += 1
            self.BO.append(Ordine(self.numero_ordini, id, quantita))
            self.condition_pizzaiolo.notify_all()
            self.condition_cliente.notify_all()
            return self.numero_ordini
            

    
    def getOrdine(self):    #richiamata da putPizze, che viene richiamata da pizzaioli
        with self.lock:
            while len(self.BO) == 0:
                self.condition_pizzaiolo.wait()
            self.condition_cliente.notify_all()     #cliente - per putOrdine()
            self.condition_pizzaiolo.notify_all()
            ordine = self.BO.pop(0)
            return ordine

    
    def putPizze(self):  #verrà richiamato dal pizzaiolo
        with self.lock:
            ordine = self.getOrdine()
            while self.dimBP == len(self.BP):
                self.condition_pizzaiolo.wait()
            self.BP[ordine.get_N_ordine()] = ordine
            self.condition_cliente.notify_all()
            self.condition_pizzaiolo.notify_all()


    def getPizze(self, n_ordine):   #verrà richiamata dal cliente
        with self.lock:
            while n_ordine not in self.BP:
                self.condition_cliente.wait()
            self.BP.pop(n_ordine)
            self.condition_pizzaiolo.notify_all()   #pizzaiolo - per putPizze()
            self.condition_cliente.notify_all()     #cliente - per putOrdine()
