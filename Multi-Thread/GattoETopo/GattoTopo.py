from threading import Thread, RLock
from random import randint
from time import sleep

class Spazio:
    def __init__(self, NSpazio):
        self.spazio = [" " for i in range(NSpazio)]
        self.posGatto = randint(0,NSpazio-1)
        self.dirGatto = -1
        self.posTopo = randint(0,NSpazio-1)
        self.dirTopo = 0
        self.spazio[self.posGatto] = "*"
        self.spazio[self.posTopo] = "."
        self.FinePartita = False
        self.lock = RLock()

    def prints(self):
        with self.lock:
            print("|%s|" % ''.join(self.spazio))
            return self.FinePartita
    
    def spostamentoGatto(self):
        with self.lock:
            if self.FinePartita:
                return True

            self.spazio[self.posGatto] = " "

            self.posGatto += self.dirGatto
            if self.posGatto == len(self.spazio):
                self.dirGatto = -1
                self.posGatto = len(self.spazio)-1
            if self.posGatto == -1:
                self.dirGatto = +1
                self.posGatto = 0
            
            self.spazio[self.posGatto] = "*"

            if self.posGatto == self.posTopo:
                self.FinePartita = True
                self.spazio[self.posGatto] = "@"

            return False

    def spostamentoTopo(self):
        with self.lock:
            if self.FinePartita:
                return True

            self.spazio[self.posTopo] = " "

            self.dirTopo = randint(-1,1)
            self.posTopo += self.dirTopo

            if self.posTopo == len(self.spazio):
                self.posTopo = len(self.spazio)-1
            if self.posTopo == -1:
                self.posTopo = 0
            
            self.spazio[self.posTopo] = "."

            if self.posGatto == self.posTopo:
                self.FinePartita = True
                self.spazio[self.posTopo] = "@"

            return False


class Display(Thread):
    def __init__(self, spazio : Spazio):
        super().__init__()
        self.spazio = spazio
    
    def run(self):
        while (not self.spazio.prints()):
            sleep(0.200)
        

    


    


class Gatto(Thread):
    def __init__(self, spazio : Spazio):
        super().__init__()
        self.spazio = spazio

    def run(self):
        while (not self.spazio.spostamentoGatto()):
            sleep(0.100)




class Topo(Thread):
    def __init__(self, spazio : Spazio):
        super().__init__()
        self.spazio = spazio

    def run(self):
        while (not self.spazio.spostamentoTopo()):
            sleep(0.100)



spazio = Spazio(20)

topo = Topo(spazio)
gatto = Gatto(spazio)

display = Display(spazio)

topo.start()
gatto.start()
display.start()