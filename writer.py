import pickle
import random
import socket
from time import sleep
import time

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

    def __init__(self):
        self.writer_soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def posalji_podatke(self):
            vrijeme_prikupljanja = time.time()
            while(True):
                kod = self.dobavi_kod(random.randint(0, 7))
                vrijednost =  random.randint(1,100)

                podaci = pickle.dumps((kod, vrijednost))
                sleep(2)
                self.writer_soket.send(podaci)
                print(kod, vrijednost)

                if((time.time() - vrijeme_prikupljanja) >= 11):
                    podaci = pickle.dumps("zaustavi")
                    self.writer_soket.send(podaci)
                    break
        
    def konektuj_sa_load_balancerom(self):
        try:
            self.writer_soket.connect((socket.gethostname(), 1000))

        except Exception:
            print("Neuspjesna konekcija na loadBalancer.")
            return False
        return True

    def dobavi_kod(self, broj):
        return lista_kodova[broj]

    def inicijalizacija_gasenja(self):
        poruka = "exit"
        podaci = pickle.dumps(poruka)
        self.writer_soket.send(podaci)
    
    def inicijalizacija_paljenja(self):
        add = "add"
        podaci = pickle.dumps(add)
        self.writer_soket.send(podaci)

    def main(self):
        if self.konektuj_sa_load_balancerom() == False:
            exit()

        while (True):
            print("Izaberite jednu od ponudjenih opcija:")
            print("1: Slanje novih informacija")
            print("2: Paljenje novog Worker-a")
            print("3: Gasenje postojeceg Worker-a")
            odgovor = input()

            if (odgovor == "1"):
                self.posalji_podatke()
            if (odgovor == "2"):
                self.inicijalizacija_paljenja()
                print("Upaljen novi Worker.\n")
            if (odgovor == "3"):
                self.inicijalizacija_gasenja()
                print("Ugasen Worker\n")


if __name__ == "__main__" :
    writer = Writer()
    writer.main()
