from random import randint
from threading import Thread
from time import sleep
import Banca
class Cliente(Thread):
    def __init__(self, banca:Banca, id_cb:int) -> None:
        super().__init__()
        self.banca = banca
        self.conto = id_cb
    
    def run(self):
        print("Salve, sono il cliente %s e ho il conto %d" % (self.name, self.conto))
        ultimo_cb = self.banca.get_num_cb()
        des = randint(0,ultimo_cb-1)
        while des == self.conto:
            des = randint(0,ultimo_cb-1)
            sleep(1)
        val = randint(0,50)
        if self.banca.trasferisci(self.conto, des ,val):
            print("Ho fatto la mia transazione, ciao da %s" % self.name)
        else:
            print("Non ho abbastanza soldi per la transazione, ciao da %s" % self.name)