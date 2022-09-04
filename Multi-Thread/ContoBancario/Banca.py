from threading import RLock
from ContoBancario import ContoBancario
from Transazione import Transazione

class Banca:
    def __init__(self) -> None:
        self.conti_bancari = {}
        self.num_cb = 0
        self.lock = RLock()

    def get_num_cb(self) -> int:
        return self.num_cb

    def addContoBancario(self,ContoBancario):
        self.conti_bancari[self.num_cb] = ContoBancario
        self.num_cb += 1
        
    def getSalfo(self,C):
        with self.lock:
            if self.conti_bancari[C]:
                return self.conti_bancari[C].getSaldo()

    def trasferisci(self, A:int, B:int, N:int):
        with self.lock:
            if(self.conti_bancari[A].getSaldo() < N):
                return False
            self.conti_bancari[A].sommaASaldo(-N)
            self.conti_bancari[B].sommaASaldo(N)
            transazione = Transazione(A,B,N)
            self.conti_bancari[A].add_transazione(transazione)
            self.conti_bancari[B].add_transazione(transazione)
            transazione.printTransazione()
            return True

    def printContiBancari(self):
        with self.lock:
            for i in range(self.num_cb):
                self.conti_bancari[i].print()

            
