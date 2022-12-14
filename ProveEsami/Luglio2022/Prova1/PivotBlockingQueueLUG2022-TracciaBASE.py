from threading import Thread,RLock,Condition, get_ident
from time import sleep
from random import random,randint

'''
Il codice fornito implementa una struttura dati detta PivotBlockingQueue, simile alla Blocking Queue. 
La differenza principale sta nel fatto che l’operazione take() opera su due elementi. 
Quando si fa un prelievo, un certo elemento da individuare, detto PIVOT, viene eliminato dalla coda, 
mentre un altro elemento viene individuato secondo l’usuale politica FIFO, quindi estratto dalla coda e restituito. 
Proprio come le code bloccanti standard, una PivotBlockingQueue può contenere al massimo N elementi, 
dove N è specificato in fase di creazione della struttura dati. Le regole per determinare l’elemento PIVOT
vengono scelte secondo un particolare criterio che è possibile impostare con un metodo apposito.
'''

plock = RLock()
def prints(s):
    plock.acquire()
    print(s)
    print("\n")
    plock.release()

class PivotBlockingQueue:
    def __init__(self,dim):
        self.dim = dim
        self.buffer = []
        self.criterio = True
        self.lock = RLock()
        self.condNewElement = Condition(self.lock)

        self.condSum = Condition(self.lock) #ADD3
        self.pivotNumber = 1 #ADD1


    '''
    take(self) -> int: 

    individua l’elemento PIVOT e lo elimina dalla coda; quindi estrae e restituisce un elemento 
    secondo il consueto ordine FIFO. Il metodo si pone in attesa bloccante se non sono presenti nella coda almeno due elementi.
    '''

    def take(self) -> int:
        with self.lock:
            while len(self.buffer) < self.pivotNumber+1: #ADD1
                self.condNewElement.wait()
            
            for i in range(self.pivotNumber): #ADD1
                self.__removePivot__()
            return self.buffer.pop(0)

    '''
    put(self,T : int)
    inserisce l’elemento T nella Blocking Queue. Se la coda contiene già N elementi,  
    individua ed elimina l’elemento PIVOT, quindi inserisce subito l’elemento T. 
    Questo metodo dunque non è mai bloccante, poiché quando non si trova posto per T, 
    questo viene creato eliminando l’elemento PIVOT.
    '''          

    def put(self,v : int):
        with self.lock:
            if len(self.buffer) == self.dim:
                self.__removePivot__()

            for i in range(self.pivotNumber): #ADD1
                self.buffer.append(v)
    
            if len(self.buffer) == 2:
                self.condNewElement.notify()
            
            self.condSum.notifyAll() #ADD3

    '''
    setCriterioPivot(minMax : boolean)
    Definisce il criterio di scelta dell’elemento PIVOT. Il criterio di scelta dell’elemento PIVOT
    serve a definire come la coda individua l’elemento PIVOT. Si può impostare la coda per prendere 
    il massimo oppure il minimo tra gli elementi attualmente presenti nella coda.
    Se minMax = True, al termine della chiamata il criterio di scelta dell’elemento PIVOT diventerà 
    quello del minimo elemento tra quelli presenti nella coda. Se minMax = False, al termine della 
    chiamata il criterio di scelta dell’elemento PIVOT diventerà quello del massimo elemento tra quelli presenti. 
    Se ci sono più di un valore massimo (o più di un valore minimo), viene selezionato l’elemento inserito più recentemente. 
    Inizialmente il criterio di scelta dell’elemento PIVOT viene impostato su quello del minimo elemento.
    '''

    def setCriterioPivot(self,minMax : bool):
        with self.lock:
            self.criterio = minMax
    
    '''
        Funzione usata per definire il criterio di scelta del pivot (max o min)
    '''
    def __migliore__(self,a :int, b: int) -> bool:
    
        return a < b if self.criterio else a > b
    
    '''
        Funzione privata che trova e rimuove il pivot secondo le regole stabilite.
        Si noti che non ci si aspetta che questa funzione venga chiamata direttamente essendo privata.
    '''
    def __removePivot__(self):
        pivot = self.buffer[0]
        pivotMultipli = False
        for i in range(1,len(self.buffer)):
            if self.__migliore__(self.buffer[i],pivot):
                pivot = self.buffer[i]
                pivotMultipli = False
            elif self.buffer[i] == pivot:
                pivotMultipli = True

        self.buffer.remove(pivot) if not pivotMultipli else self.buffer.pop()


    def print(self):
        with self.lock:
            prints(self.getStringa())

    def getStringa(self):
        stringa = ""
        for i in self.buffer:
            stringa += str(i) + " "
        return stringa

    #ADD : punto 1 (ADD1)
    def setPivotNumber(self, n : int):
        with self.lock:
            if n < 1 or n > self.dim -1:
                prints("Numero non compreso tra 1 e dim-1")
            else:
                self.pivotNumber = n

    #ADD : punto 2 (ADD2)
    def doubleTake(self):
        with self.lock:
            while len(self.buffer) < 2 + self.pivotNumber:
                self.condNewElement.wait()
            
            for i in range(self.pivotNumber): #ADD1
                self.__removePivot__()
            x = self.buffer.pop(0)
            y = self.buffer.pop(0)
            return x, y
    
    #ADD : punto 3 (ADD3)
    def waitFor(self, n : int) -> None:
        while (self.sum() <= n):
            self.condSum.wait()
            
            

    def sum(self):
        sum = 0
        for i in self.buffer:
            sum += i
        return sum


'''
    Thread di test
'''       
class Operator(Thread):
    
    def __init__(self,c):
        super().__init__()
        self.coda = c
        
    def run(self):
        #for i in range(1000):
        sleep(random())
        coda.put(randint(-100,100))
        coda.put(randint(-100,100))
        sleep(random())
        prints (f"Il thread TID={get_ident()} ha estratto il valore {coda.take()}" )


class Display(Thread):
    def __init__(self, coda : PivotBlockingQueue):
        super().__init__()
        self.coda = coda

    def run(self):
        while(1):
            self.coda.print()

            sleep(0.15)


if __name__ == '__main__':
            
    coda = PivotBlockingQueue(10)  
    coda.setPivotNumber(2)    
    d = Display(coda)
    d.start()  
    operatori = [Operator(coda) for i in range(50)] 
    for o in operatori:
        o.start()     
    