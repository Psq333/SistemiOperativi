from threading import Thread, RLock, Condition
from time import sleep
from tkinter.tix import Tree


class Cliente(Thread):
    def __init__(self,salone):
        super().__init__()
        self.salone = salone

    def run(self):
        print("Entro nel salone %s" % self.name)
        if self.salone.testaEOccupaPoltrona() == False:
            print("Che seccatura, sono 10 persone in fila, vado via %s" % self.name)
            return

        print("Sono in fila %s" % self.name)
        sleep(10)
        self.salone.fineTaglioCapelli()
        print("Capelli tagliati %s" % self.name)
            



class Barbiere(Thread):
    def __init__(self, salone):
        super().__init__()
        self.salone = salone

    def run(self):
        i = 0
        while True:
            print("Inizio il mio lavoro" + str(i))
            i+=1
            self.salone.tagliaCapelli_Barbiere()
            sleep(1)
        print ("Fine lavoro")
            


class Salone:
    def __init__(self):
        self.poltrona = False
        self.attesa = 0
        self.lock = RLock()
        self.salone_vuoto = Condition(self.lock)
        self.poltrona_piena = Condition(self.lock)

    def testaEOccupaPoltrona(self):
        with self.lock:
            self.salone_vuoto.notify_all()
            if self.attesa == 10:
                return False
            self.attesa += 1
            while self.poltrona == True:
                self.poltrona_piena.wait()
            if self.poltrona == False and self.attesa == 0:
                self.poltrona = True
    
    def fineTaglioCapelli(self):
        with self.lock:
            self.poltrona = False
            self.poltrona_piena.notify_all()
            self.attesa -= 1

    def tagliaCapelli_Barbiere(self):
        with self.lock:
            #print(str(self.poltrona) + "  " + str(self.attesa) +"\n")
            while self.poltrona == False and self.attesa == 0:
                print("Sono dentro")
                self.salone_vuoto.wait()
            

    

salone = Salone()

barbiere = Barbiere(salone)
barbiere.start()

for i in range(0,20):
    c = Cliente(salone)
    c.start()

