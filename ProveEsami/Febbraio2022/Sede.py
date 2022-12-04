import random, time, os
from threading import Thread,Condition,RLock, get_ident
from queue import Queue

#
# Una sede sarà formata da tanti Uffici
#

class Ufficio:
    def __init__(self,l):
        Thread.__init__(self)
        self.lock = RLock()
        self.condition = Condition(self.lock)
        self.lettera = l
        self.ticketDaRilasciare = 0
        self.ticketDaServire = 0

    #
    # Fornisce un ticket formattato abbinando correttamente lettera e numero
    #
    def formatTicket(self,lettera,numero):
        return "%s%03d" % (lettera, numero)
    
    #
    # Restituisce quanti ticket in attesa ci sono in questo ufficio
    #
    def getTicketInAttesa(self):
        with self.lock:
            return self.ticketDaRilasciare - self.ticketDaServire

    #
    # Invocato da un utente  quando deve prendere un numerino
    #
    def prendiProssimoTicket(self):
        with self.lock:
            #
            # self.ticketDaRilasciare e self.ticketDaServire stanno per diventare diversi e cioè ci sono utenti da smaltire
            #
            if (self.ticketDaRilasciare <= self.ticketDaServire):
                self.condition.notify_all()
            self.ticketDaRilasciare+=1
            
            return self.formatTicket(self.lettera, self.ticketDaRilasciare)

    #
    # Invocato da un impiegato quando deve chiamare la prossima persona
    #
    def chiamaProssimoTicket(self):
        with self.lock:
            #
            # Non ci sono ticket in attesa da elaborare. Attendo
            #
            while(self.ticketDaRilasciare <= self.ticketDaServire):
                self.condition.wait()

            self.ticketDaServire+=1
            
            return self.formatTicket(self.lettera, self.ticketDaServire)
                
 
class Sede:

    def __init__(self,n):
        self.n = n
        #
        # Gestiremo gli n uffici con un dizionario. Esempio: per selezionare l'ufficio "C" si usa self.uffici["C"]
        #
        self.uffici = {} 
        for l in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[0:n]:
            self.uffici[l] = Ufficio(l) 
        self.lock = RLock()
        self.condition = Condition(self.lock)
        self.ultimiTicket = []
        self.lenUltimiTicket = 10
        self.update = False
        self.setPrintAttese = False

    #
    # Preleva ticket da rispettivo ufficio. N.B. si usa il lock del rispettivo ufficio
    #
    def prendiTicket(self,uff):
        return self.uffici[uff].prendiProssimoTicket()

    #
    # Chiama ticket del rispettivo ufficio. N.B. si usa il lock del rispettivo ufficio e poi si aggiorna l'elenco degli ultimi ticket con il lock di SEDE
    #
    def chiamaTicket(self,uff):
        ticket = self.uffici[uff].chiamaProssimoTicket()
        with self.lock:
            self.condition.notifyAll()
            #
            # Questo aggiornamento serve a far capire al display che ci sono novità da stampare a video
            #
            self.update = True
            if(len(self.ultimiTicket) >= 5):
                self.ultimiTicket.pop()
            
            if self.lenUltimiTicket == len(self.ultimiTicket):
                self.ultimiTicket.pop(0)
            self.ultimiTicket.insert(0,ticket)
            

    def waitForTicket(self,ticket):
        with self.lock:
            while(ticket not in self.ultimiTicket):
                self.condition.wait()

    #
    # Serve a segnalare al display di stampare il riepilogo
    #
    def printAttese(self):
        with self.lock:
            self.setPrintAttese = True
        
    #
    #  Stampa gli ultimi numeri chiamati
    #
    def printUltimi(self):
        with self.lock:
            while not self.update:
                self.condition.wait()
            self.update = False
            #os.system('clear')
            #
            # Se qualcuno lo ha chiesto, stampo l'elenco degli utenti in coda per ogni ufficio
            #
            if (self.setPrintAttese):
                for u in self.uffici:
                    print("%s : %d" % (self.uffici[u].lettera, self.uffici[u].getTicketInAttesa()))
                self.setPrintAttese = False
            for t in self.ultimiTicket:
                print(t)
            print ("="*10)

    
    def listIsInUltimi(self, L : list):
        with self.lock:
            for i in L:
                if i in self.ultimiTicket:
                    return True
            return False
        
    def controlloSalto(self, L:list):
        for i in self.ultimiTicket:
            for j in L:
                if(i[0] == j[0]):
                    if(j < i and j not in self.ultimiTicket):
                        return True
        return False

    def waitForTickets(self, L : list):
        with self.lock:
            b = False
            for i in L:
                if(self.waitForTicketSafe(i)):
                    b = True
                if b == False:
                    return False
            while not self.listIsInUltimi(L):
                self.condition.wait()
            return True
            

    def getLettereUltimi(self):
        with self.lock:
            list = []
            for i in self.ultimiTicket:
                list.append(i[0])
            return list

    def waitForTicketSafe(self, ticket):
        with self.lock:
            primaLettera = ticket[0]
            while(primaLettera not in self.getLettereUltimi()):
                self.condition.wait()

            for i in self.ultimiTicket:
                if(i[0] == primaLettera):
                    if(ticket < i and ticket not in self.ultimiTicket):
                        return True
            return False

    def incDecSizeUltimi(self,n : int):
        with self.lock:
            if n < 0 and -n >= len(self.ultimiTicket):
                return False
            self.lenUltimiTicket += n
            
            



class Utente(Thread):
    def __init__(self, sede):
        Thread.__init__(self)
        self.sede = sede
        self.n = len(sede.uffici)

    def run(self):
        while True:
            ticket = self.sede.prendiTicket(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ"[0:self.n]))
            print(f"Sono l'utente {get_ident()} e mi faccio un giro prima di mettermi ad aspettare il mio ticket {ticket}")
            #DIMOSTRAZIONE THREAD VA IN ATTESA BLOCCANTE
            time.sleep(random.randint(1,3))
            if(self.sede.waitForTicketSafe(str(ticket))):
                print("Troppo tardi questo per questo ticket: ", str(ticket))
            print(f"Sono l'utente {get_ident()}, ho preso un caffè e adesso aspetto il mio ticket: {ticket}") 
            self.sede.waitForTicket(str(ticket))

class UtenteSafe(Thread):
    def __init__(self, sede):
        Thread.__init__(self)
        self.sede = sede
        self.n = len(sede.uffici)

    def run(self):
        while True:
            ticket = self.sede.prendiTicket(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ"[0:self.n]))
            print(f"Sono l'utente {get_ident()} e mi faccio un giro prima di mettermi ad aspettare il mio ticket {ticket}")
            time.sleep(random.randint(1,3))
            if(self.sede.waitForTicketSafe(str(ticket))):
                print("Troppo tardi questo per questo ticket: ", str(ticket))
            print(f"Sono l'utente {get_ident()}, ho preso un caffè e adesso aspetto il mio ticket: {ticket}") 
            self.sede.waitForTicketSafe(str(ticket))

class UtenteFurbetto(Thread):
    def __init__(self, sede):
        Thread.__init__(self)
        self.sede = sede
        self.n = len(sede.uffici)

    def run(self):
        while True:
            list = []
            list.append(self.sede.prendiTicket(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ"[0:self.n])))
            list.append(self.sede.prendiTicket(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ"[0:self.n])))
            list.append(self.sede.prendiTicket(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ"[0:self.n])))
            print(f"Sono l'utente {get_ident()} e mi faccio un giro prima di mettermi ad aspettare il mio ticket {str(list)}")
            time.sleep(random.randint(1,3))
            if(self.sede.waitForTickets(list)):
                print("Troppo tardi questo per questo ticket: ", str(list))
            print(f"Sono l'utente {get_ident()}, ho preso un caffè e adesso aspetto il mio ticket: str(list)") 
            self.sede.waitForTicketSafe(str(list))

class Impiegato(Thread):
    def __init__(self, sede, lettera):
        Thread.__init__(self)
        self.sede = sede
        self.ufficio = lettera
 
    def run(self):
        while True:
            self.sede.chiamaTicket(self.ufficio)
            #
            # Simula un certo tempo in cui l'impiegato serve l'utente appena chiamato
            #
            time.sleep(random.randint(1,4))
            #
            # Notifica di voler stampare il riepilogo attese 
            #
            if random.randint(0,5) >= 4:
                self.sede.printAttese()

class U(Thread):
    def __init__(self, sede):
        Thread.__init__(self)
        self.sede = sede
        self.n = len(sede.uffici)

    def run(self):
        while True:
            ticket = "A001"
            print(f"Sono l'utente {get_ident()} e mi faccio un giro prima di mettermi ad aspettare il mio ticket {ticket}")
            #DIMOSTRAZIONE THREAD VA IN ATTESA BLOCCANTE
            time.sleep(random.randint(1,3))
            if(self.sede.bigliettoSaltato(str(ticket))):
                print(str(ticket), "Coglioneeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
            print(f"Sono l'utente {get_ident()}, ho preso un caffè e adesso aspetto il mio ticket: {ticket}") 
            self.sede.waitForTicket(str(ticket))



class Display(Thread):
    def __init__(self, sede):
        Thread.__init__(self)
        self.sede = sede
        

    def run(self):
        while True:
            self.sede.printUltimi()
            





sede = Sede(6)

display = Display(sede)
display.start()


utenti = [Utente(sede) for p in range(10)]
impiegato = [Impiegato(sede, i) for i in "ABCDEF"]


for p in utenti:
    p.start()

for i in impiegato:
    i.start()



time.sleep(10)

print("Parteeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
u = U(sede)
u.start()