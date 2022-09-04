from threading import RLock
from Transazione import Transazione

class ContoBancario():
    def __init__(self, id, saldo) -> None:
        self.id = id
        self.saldo = saldo
        self.transazioni = []
        self.lock = RLock()
    
    def getSaldo(self):
        with self.lock:
            return self.saldo

    def sommaASaldo(self,v):
        with self.lock:
            self.saldo += v
    
    def add_transazione(self, transazione:Transazione):
        with self.lock:
            if len(self.transazioni) == 50:
                self.transazioni.pop(0)
            self.transazioni.append(transazione)

    def print(self):
        print ("Sono il conto bancario %d con il saldo %d\n" % (self.id,self.saldo))

    
