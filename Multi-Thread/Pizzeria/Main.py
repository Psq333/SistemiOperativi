from Pizzeria import Pizzeria
from Pizzaiolo import Pizzaiolo
from Cliente import Cliente

num_buffer_ordini = 10
num_buffer_pizze = 10
num_clienti = 10
num_pizzaioli = 10
pizzeria_da_toto = Pizzeria(num_buffer_ordini, num_buffer_pizze)

for i in range(num_clienti):
    Cliente(pizzeria_da_toto).start()

for i in range(num_pizzaioli):
    Pizzaiolo(pizzeria_da_toto).start()
