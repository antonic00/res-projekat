import pickle
import random
import socket
from time import sleep

lista_kodova = [
    "CODE_ANALOG",
    "CODE_DIGITAL",
    "CODE_CUSTOM",
    "CODE_LIMITSET",
    "CODE_SINGLENODE",
    "CODE_MULTIPLENODE",
    "CODE_CONSUMER",
    "CODE_SOURCE"
]

class Writer:

    def _init_(self):
        self.writer_soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def posalji_podatke(self):
        while(True):
            
            kod = self.dobavi_kod(random.randint(0, 7))
            vrijednost =  random.randint(0,100)
            
            podaci = pickle.dumps((kod, vrijednost))
            sleep(2)
            self.writer_soket.send(podaci)
            print(kod, vrijednost)
    
    def konektuj_sa_load_balancerom(self):
        try:
            self.writer_soket.connect((socket.gethostname(), 1000))

        except socket.error:
            print("Neuspjesna konekcija na loadBalancer.")
            return False
        return True

    def dobavi_kod(self, broj):
        return lista_kodova[broj]

    def inicijalizacija_paljenja(self):
        add = "add"
        podaci = pickle.dumps(add)
        self.writer_soket.send(podaci)

if _name_ == "_main_" :
    writer = Writer()
    if writer.konektuj_sa_load_balancerom() == False:
        exit()

    while(True):
        print("Izaberite jednu od ponudjenih opcija:")
        print("1: Slanje novih informacija")
        print("2: Paljenje novog Worker-a")
        print("3: Gasenje postojeceg Worker-a")
        odgovor = input()

        if(odgovor == "1"):
            writer.posalji_podatke()
        if(odgovor == "2"):
            writer.inicijalizacija_paljenja()
            print("Upaljen novi Worker.\n")
        if(odgovor == "3"):
            print("Usao u 3")
