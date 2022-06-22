import socket
import pickle
from broj_workera import Broj_Workera
from description import Description
import random

class Load_Balancer:
    def __init__(self):
        self.load_balancer_to_writer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.load_balancer_to_worker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.writer_socket = None
        self.worker_socket = list()
        self.broj_workera = Broj_Workera()
    def konekcija_sa_writerom(self):
        try:
            self.load_balancer_to_writer.bind((socket.gethostname(), 1000))
            self.load_balancer_to_writer.listen(4)
            print("Slusam...")
            konekcija, adresa = self.load_balancer_to_writer.accept()
            self.writer_socket = konekcija
        except socket.error:
            print("Neuspjesna konekcija sa writer-om.")
            return False
        return True
    
    def posalji_podatke(self):
            buffer = list()
            novi_ciklus = 0
            trenutni_soket = 0
            while(True):
                data = self.writer_socket.recv(4096) 
                try:
                    (kod, vrijednost) = pickle.loads(data)
                    if novi_ciklus == 0:
                        novi_ciklus = 1
                except ValueError:
                    try:
                        poruka = pickle.loads(data)
                        if(poruka == "zaustavi"):
                            while True:
                                podaci = pickle.dumps(buffer[0])
                                print(len(buffer))
                                buffer.pop(0)
                                self.worker_socket[trenutni_soket].send(podaci)
                                if len(buffer) == 0:
                                    break
                                trenutni_soket += 1
                                if trenutni_soket == self.broj_workera.get_broj_workera() + 1:
                                    trenutni_soket = 0
                            novi_ciklus = 0
                            continue
                    except Exception as e:
                        print(e)
                        exit()
                except Exception as e:
                    print(e)
                    exit()

                id = random.randint(0, 100)
                dataset = self.odredi_data_set(kod)
                description = Description(id, dataset)

                description.dodaj_u_listu(kod, vrijednost)

                buffer.append(description)

    def priprema_soketa(self):
            self.load_balancer_to_worker.bind((socket.gethostname(), 8001))
            self.load_balancer_to_worker.listen(4)
    def konekcija_sa_workerom(self):
        try:
            print("Slusam...")
            konekcija, adresa = self.load_balancer_to_worker.accept()
            self.dodaj_u_listu(konekcija)
        except socket.error:
            print("Neuspesna konekcija sa Workerom")
            return False
        return True

    def dodaj_u_listu(self, konekcija):
        self.worker_socket.append(konekcija)
        self.broj_workera.povecaj_broj_workera()

    def gasi_workera(self):
        podaci = pickle.dumps("exit")
        self.worker_socket[self.broj_workera.get_broj_workera()].send(podaci)
    

    def odredi_data_set(self, code):
        if code in ["CODE_ANALOG", "CODE_DIGITAL"]:
            return 1
        if code in ["CODE_CUSTOM", "CODE_LIMITSET"]:
            return 2
        if code in ["CODE_SINGLENODE", "CODE_MULTIPLENODE"]:
            return 3
        if code in ["CODE_CONSUMER", "CODE_SOURCE"]:
            return 4


if __name__ == "__main__":
    load_balancer = Load_Balancer()

    if load_balancer.konekcija_sa_writerom():
        print("Uspesna konekcija sa writerom")
        load_balancer.priprema_soketa()
        load_balancer.posalji_podatke()
