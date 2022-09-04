from random import randint
from statistics import quantiles
from threading import Thread
from time import sleep
from Pizzeria import Pizzeria

class Cliente(Thread):
    def __init__(self, p: Pizzeria) -> None:
        super().__init__()
        self.pizzeria = p
    
    def run(self):
        #while True:
            print("Entro nella pizzeria - sono %s" % self.name)
            id_pizza = randint(0,7)
            quantita = randint(1,20)
            sleep(1) # a) inattività
            num_ordine = self.pizzeria.putOrdine(id_pizza, quantita) # b)
            print("Ordine sul Buffer Ordini - sono %s" % self.name)
            sleep(randint(1,2)) # c)
            self.pizzeria.getPizze(num_ordine)  # d)
            print("Pizze prese, urrà - sono %s" % self.name)
            sleep(1)
        