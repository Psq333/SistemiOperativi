from threading import RLock,Condition, Thread
import random
import time

plock = RLock()
def prints(self, s):
    with plock:
        print(s)

class BlockingStack:
    
    def __init__(self,size):
        self.size = size
        self.elementi = [1,2,3,4,5,6,7]
        self.lock = RLock()
        self.conditionTuttoPieno = Condition(self.lock)
        self.conditionTuttoVuoto = Condition(self.lock)
        self.condition = Condition(self.lock)
        
    def __find(self,t):
        try:
            if self.elementi.index(t) >= 0:
                return True
        except(ValueError): 
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
        
    def print(self):
        with self.lock:
            stringa = ""
            for i in self.elementi:
                stringa = i + " ";
            return stringa


    
    

class Consumer(Thread): 
    
    def __init__(self,buffer):
        self.queue = buffer
        Thread.__init__(self)

    def run(self):
        while True:
            time.sleep(random.random()*2)
            x, y = self.queue.doubleTakePop()
            prints(f"Estratto elemento {x,y}")
            


class Producer(Thread):

    def __init__(self,buffer):
        self.queue = buffer
        Thread.__init__(self)

    def run(self): 
        while True:
            time.sleep(random.random() * 2)
            self.queue.put(self.name)
            


class Display(Thread):

    def __init__(self, buffer):
        self.buffer = buffer
        Thread.__init__(self)

    def run(self):
        while True:
            time.sleep(0.5)
            prints(self.buffer.print())

#  Main
#
buffer = BlockingStack(10)

producers = [Producer(buffer) for x in range(5)]
consumers = [Consumer(buffer) for x in range(3)]

for p in producers:
    p.start()

for c in consumers:
    c.start()
    
