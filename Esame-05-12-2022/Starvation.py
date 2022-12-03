from threading import RLock,Condition, Thread, Barrier
import random
import time

class BlockingStack:
    
    def __init__(self,size):
        self.size = size
        self.elementi = []
        self.lock = RLock()
        self.wait = 0
        self.conditionTuttoPieno = Condition(self.lock)
        self.conditionTuttoVuoto = Condition(self.lock)
        
    def __find(self,t):
        try:
            if self.elementi.index(t) >= 0:
                return True
        except(ValueError): #Se l'elemento t non è in self.element esce un errore. L'errore viene gestito dall'except
            return False
    
    def put(self,t):
        self.lock.acquire()
        while len(self.elementi) == self.size:
            self.conditionTuttoPieno.wait()
        self.conditionTuttoVuoto.notify_all()
        self.elementi.append(t)
        self.lock.release()
    
    
    def take(self,t=None):
        self.lock.acquire()
        try:
            if t == None:
                while len(self.elementi) == 0:
                    self.conditionTuttoVuoto.wait()
                
                if len(self.elementi) == self.size: 
                    #Se la condizione viene soddifatta, vuol dire che ci sono Thread in sleep, altrimenti non risveglio nulla
                    self.conditionTuttoPieno.notify()
                return self.elementi.pop()
            else:
                while not self.__find(t):
                    self.conditionTuttoVuoto.wait()
                if len(self.elementi) == self.size:
                    self.conditionTuttoPieno.notify()
                self.elementi.remove(t)    
                return t    
        finally:
            self.lock.release()
    
    

class Consumer(Thread): 
    
    b = Barrier(3)
    soglia = 10

    def __init__(self,buffer):
        self.queue = buffer
        Thread.__init__(self)
        self.cont = 0

    def run(self):
        while True:
            if(self.cont == self.soglia):
                self.b.wait()
                self.cont = 0
            self.cont+=1
            time.sleep(random.random()*2)
            print(f"Estratto elemento {self.queue.take()}")


class Producer(Thread):

    b = Barrier(5)
    soglia = 10

    def __init__(self,buffer):
        self.queue = buffer
        Thread.__init__(self)
        self.cont = 0

    def run(self): 
        while True:
            if(self.cont == self.soglia):
                self.b.wait()
                self.cont = 0
            self.cont+=1
            time.sleep(random.random() * 2)
            self.queue.put(self.name)
            
#  Main
#
buffer = BlockingStack(10)

producers = [Producer(buffer) for x in range(5)]
consumers = [Consumer(buffer) for x in range(3)]

for p in producers:
    p.start()

for c in consumers:
    c.start()
    
