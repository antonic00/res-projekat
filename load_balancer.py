import socket
import pickle
from description import Description
import random
import time

class Load_Balancer:
    def __init__(self):
        self.load_balancer_to_writer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.load_balacer_to_worker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def konekcija_sa_writerom(self):
        try:
            self.load_balancer_to_writer.bind((socket.gethostname(), 1000))
            self.load_balancer_to_writer.listen(4)
            print("Slusam...")
            konekcija, adresa = self.load_balancer_to_writer.accept()
            buffer = list()
            vrijeme_prikupljanja = time.time()

            while(True):
                data = konekcija.recv(4096)
                (kod, vrijednost) = pickle.loads(data)

                id = random.randint(0, 100)
                dataset = self.odredi_data_set(kod)
                description = Description(id, dataset)

                description.dodaj_u_listu(kod, vrijednost)
                
                buffer.append(description)

                if((time.time() - vrijeme_prikupljanja) >= 10):
                    podaci = pickle.dumps(buffer)
                    self.load_balacer_to_worker.send(podaci)
                    buffer.clear()
                    vrijeme_prikupljanja = time.time()


        except socket.error:
            print("Neuspjesna konekcija sa writer-om.")
            return False
        return True

    def konekcija_sa_workerom(self):
        try:
            self.load_balacer_to_worker.connect((socket.gethostname(), 1001))
        except socket.error:
            print("Neuspesna konekcija sa Workerom")
            return False
        return True

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

    if load_balancer.konekcija_sa_workerom():
        print("Konekcija sa workerom uspesna.")
        if load_balancer.konekcija_sa_writerom():
            print("Uspesna konekcija sa writerom")
            input()
