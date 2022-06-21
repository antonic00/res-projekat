import socket
import pickle
from collection_description import Collection_Description

from description import Description
from historical_collection import Historical_Collection

class Worker:
    def _init_(self):
        self.worker_sa_load_balancerom = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def konektuj_sa_load_balancerom(self):
        try:
            self.worker_sa_load_balancerom.bind((socket.gethostname(), 1001))
            self.worker_sa_load_balancerom.listen(4)
            print("Slusam...")
            konekcija, adresa = self.worker_sa_load_balancerom.accept()
            print("Sve konektovano.")
            while(True):
                data = konekcija.recv(4096)
                buffer = pickle.loads(data)
                for description in buffer:
                    collection_description = Collection_Description(description.id, description.dataset)
                    for item in description.lista_itema :
                        collection_description.historical_collection.dodaj_u_niz_propertija(item[0], item[1]) 
                        print(collection_description.id)
                        print(collection_description.dataset)
                        for item in collection_description.historical_collection.worker_properties:
                            print(item[0])
                            print(item[1])
        except socket.error:
            print("Neuspesna konekcija sa loadBalancerom")
            return False
        

    

if _name_ == "_main_":
    worker = Worker()
    worker.konektuj_sa_load_balancerom()
