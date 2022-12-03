from threading import Lock,RLock, Condition, Thread
from time import sleep
from random import random, randint

debug = True

#
# Stampa sincronizzata
#
plock = Lock()
def sprint(s):
    with plock:
        print(s)    

#
# Stampa solo in debug mode
#

def dprint(s):
    with plock:
        if debug:
            print(s)

class RunningSushiBuffer:

    theBuffer : list
    dim : int
    lock : RLock
    condition : Condition

    def __init__(self, dim):
        self.theBuffer = [None] * dim
        self.zeroPosition = 0
        self.dim = dim
        self.lock = RLock()
        self.condition = Condition(self.lock)

    def _getRealPosition(self,i : int):
        return (i + self.zeroPosition) % self.dim

    def get(self, pos : int):
        with self.lock:
            while self.theBuffer[self._getRealPosition(pos)] == None:
                self.condition.wait()

            palluzza = self.theBuffer[self._getRealPosition(pos)]
            self.theBuffer[self._getRealPosition(pos)] = None
        self.condition.notifyAll() #TURNO1
        return palluzza

    def put(self, t):
        with self.lock:
            while self.theBuffer[self._getRealPosition(0)] != None:
                self.condition.wait()
            
            self.theBuffer[self._getRealPosition(0)] = t

    def shift(self, j = 1):
        with self.lock:
            #
            # uso zeroPosition per spostare la posizione 0 solo virtualmente,
            # anziche' dover ricopiare degli elementi
            #
            self.zeroPosition = (self.zeroPosition + j) % self.dim
            #
            # E' solo grazie a uno shift che puo' crearsi la condizione per svegliare un thread
            # in attesa, rispettivamente su put() o su get()
            #
            self.condition.notifyAll()

    #TURNO1
    def putList(self,L):
        with self.lock:
            while not (self.libereDa0aL(len(L))):
                self.condition.wait()
            for i in L:
                self.put(i)
                self.shift()
    
    #TURNO1
    def libereDa0aL(self, lenL):
        for i in range(0, lenL):
            if self.theBuffer[self._getRealPosition(i)] != None:
                return False
        return True

    
    #TURNO2
    def getList(self,N,t,i):
        with self.lock:
            coda = []
            for i in range(0,N):
                while (self.theBuffer[self._getRealPosition(i)] == None or
                    self.theBuffer[self._getRealPosition(i)] == t):
                    self.condition.wait()
                
                coda.append(self.theBuffer.pop(self._getRealPosition(i)))
            return coda
            


class NastroRotante(Thread):

    def __init__(self, d : RunningSushiBuffer):
        super().__init__()
        self.iterazioni = 10000
        self.d = d

    def run(self):
        while(self.iterazioni > 0):
            sleep(0.1)
            self.iterazioni -= 1
            self.d.shift()

class Cuoco(Thread):

    piatti = [ "*", ";", "^", "%"]

    def __init__(self, d : RunningSushiBuffer):
        super().__init__()
        self.iterazioni = 1000
        self.d = d

    def run(self):
        while(self.iterazioni > 0):
            sleep(0.5 * random())
            self.iterazioni -= 1
            randPiatto = randint(0,len(self.piatti)-1)
            self.d.put(self.piatti[randPiatto])
            print ( f"Il cuoco {self.ident} ha cucinato <{self.piatti[randPiatto]}>")
            print ( f"Il cuoco {self.ident} ha finito il suo turno e va via")

class Cliente(Thread):

    def __init__(self, d : RunningSushiBuffer, pos : int):
        super().__init__()
        self.coseCheVoglioMangiare = randint(1,20)
        self.d = d
        self.pos = pos

    def run(self):
        while(self.coseCheVoglioMangiare > 0):
            sleep(5 * random())
            self.coseCheVoglioMangiare -= 1
            print ( f"Il cliente {self.ident} aspetta cibo")
            print ( f"Il cliente {self.ident} mangia <{self.d.get(self.pos)}>")
            print ( f"Il cliente {self.ident} ha la pancia piena e va via")

class ClienteEsigente(Thread):

    def __init__(self, d: RunningSushiBuffer, pos : int):
        super().__init__()
        self.coseCheVoglioMangiare = randint(1,5)
        self.d = d
        self.pos = pos

    def run(self):
        while(self.coseCheVoglioMangiare > 0):
            sleep(5 * random())
            self.coseCheVoglioMangiare -= 1

            alimento_detestato = Cuoco.piatti[randint(0,3)]
            quantita_cibo = randint(1,6)

            print ( f"Il cliente {self.ident} aspetta cibo")
            print ( f"Il cliente {self.ident} mangia tutto tranne {alimento_detestato} prende quindi {self.d.getList(quantita_cibo, alimento_detestato, self.pos)}")
            print ( f"Il cliente {self.ident} ha la pancia piena e va via")

size = 20
D = RunningSushiBuffer(size)
NastroRotante(D).start()

for i in range(0,2):
    Cuoco(D).start()
for i in range(1,size):
    if i == 5:
           ClienteEsigente(D,i).start()
    Cliente(D,i).start()