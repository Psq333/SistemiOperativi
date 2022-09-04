import Transazione
from Banca import Banca
from ContoBancario import ContoBancario
from Cliente import Cliente
from time import sleep

NCLIENTI = 3
banca = Banca()
clienti = []

for i in range(0,NCLIENTI):
    conto_bancario = ContoBancario(i,100)
    banca.addContoBancario(conto_bancario)
    c = Cliente(banca,i)
    c.start()
    clienti.append(c)

sleep(10)

banca.printContiBancari()
    