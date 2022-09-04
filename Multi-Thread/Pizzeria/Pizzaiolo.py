from random import randint
from threading import Thread
from time import sleep
from Pizzeria import Pizzeria

class Pizzaiolo(Thread):
    def __init__(self, p: Pizzeria) -> None:
        super().__init__()
        self.pizzeria = p
    
    def run(self):
        #while True:
            print("Prendo ordine sul Buffer Ordini - sono pizzaiolo %s" % self.name)
            #self.pizzeria.getOrdine()
            print("Preparazione pizze - sono pizzaiolo %s" % self.name)
            sleep(randint(1,3)) # c)
            self.pizzeria.putPizze()  # d)
            print("Pizze pronte - sono pizzaiolo %s" % self.name)
            sleep(1)