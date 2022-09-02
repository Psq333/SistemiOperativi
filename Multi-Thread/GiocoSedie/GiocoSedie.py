
from random import randrange
from threading import Lock, Thread
from time import sleep

class Sedie: #DATI CONDIVISI
    def __init__(self):
        self.lock = Lock()
        self.occupato = False

    def testaEOccupa(self):
        with self.lock:
            if (self.occupato == False):
                self.occupato = True
                return True
            else:
                return False

    def libero(self):
        with self.lock:
            return not self.occupato
        


class Partecipante(Thread):
    def __init__(self, sedie):
        super().__init__()
        self.sedie = sedie
    
    def run(self):
        sleep(randrange(5))
        for i in range(0, len(self.sedie)):
            if self.sedie[i].testaEOccupa():
                print ("Sono il thread %s e occupo il posto %d" % (self.name, i))
                return 
        print ("Sono il thread %s e ho perso" % self.name)



class Display(Thread):
    def __init__(self, sedie):
        super().__init__()
        self.s = sedie

    def run(self):
        while(True):
            sleep(1)
            for i in range(0, len(self.s)):
                if self.s[i].libero():
                    print("-", end="", flush=True)
                else:
                    print("o", end="", flush=True)
                print('') 





N_SEDIE = 10


SEDIE = [Sedie() for i in range(0, N_SEDIE)]


display = Display(SEDIE)
#display.start()

for i in range(0, N_SEDIE+1):
    t = Partecipante(SEDIE)
    t.start()