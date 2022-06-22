import socket
import pickle
from database_functions import dobavi_podatak, konekcija
from datetime import datetime
import mysql.connector

from collection_description import Collection_Description


class Worker:
    def _init_(self):
        self.worker_sa_load_balancerom = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.baza = None
        self.worker_sa_readerom = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def konektuj_sa_load_balancerom(self):
        try:
            self.worker_sa_load_balancerom.connect((socket.gethostname(), 8001))
        except socket.error:
            print("Neuspesna konekcija sa loadBalancerom")
            return False
        return True
 

    def primi_podatke(self):
        self.baza = konekcija()
        while(True):
            data = self.worker_sa_load_balancerom.recv(4096)
            try:
                buffer = pickle.loads(data)
            except EOFError:
                continue
            if(buffer == "exit"):
                self.worker_sa_load_balancerom.close()
                exit()
            collection_description = Collection_Description(buffer.id, buffer.dataset)
            for item in buffer.lista_itema :
                collection_description.historical_collection.dodaj_u_niz_propertija(item[0], item[1]) 
                print(collection_description.id)
                #print(collection_description.dataset)
                for item in collection_description.historical_collection.worker_properties:
                    podaci = pickle.dumps((item[0], item[1]))
                    self.worker_sa_readerom.send(podaci)
                    timestamp = datetime.now()
                    rezultat = dobavi_podatak(collection_description.id, self.baza)
                    if len(rezultat) == 0:
                        self.dodaj_element(collection_description.id, collection_description.dataset, item[0], item[1], timestamp)
                    else:
                        iz_baze = rezultat[0]
                        #print(iz_baze[0])

                        deadband = self.izracunaj_deadband(iz_baze[0], item[1])
                        #print(deadband)
                        if deadband <=2 :
                            self.update_element(collection_description.id, collection_description.dataset, item[1])
                            print("Odradio update")
                        else:
                            print("ID vec postoji u bazi. Deadband ne dozvoljava upis.\n")


  

    def dodaj_element(self, id, dataset, code, value, timestamp):
        my_cursor = self.baza.cursor()
        if(dataset == 1):
            my_cursor.execute("INSERT INTO DATASET_1(id, dataset, code, value, timestamp) VALUES (%s, %s, %s, %s, %s)", (id, dataset, code, value, timestamp))
        if(dataset == 2):
            my_cursor.execute("INSERT INTO DATASET_2(id, dataset, code, value, timestamp) VALUES (%s, %s, %s, %s, %s)", (id, dataset, code, value, timestamp))
        if(dataset == 3):
            my_cursor.execute("INSERT INTO DATASET_3(id, dataset, code, value, timestamp) VALUES (%s, %s, %s, %s, %s)", (id, dataset, code, value, timestamp))
        if(dataset == 4):
            my_cursor.execute("INSERT INTO DATASET_4(id, dataset, code, value, timestamp) VALUES (%s, %s, %s, %s, %s)", (id, dataset, code, value, timestamp))
        self.baza.commit()

    def update_element(self, id, dataset, value):
        my_cursor = self.baza.cursor()
        if(dataset == 1):
            my_cursor.execute("UPDATE dataset_1 SET value = %s WHERE dataset_1.id = %s", (value, id))
        if(dataset == 2):
            my_cursor.execute("UPDATE dataset_2 SET value = %s WHERE dataset_2.id = %s", (value, id))
        if(dataset == 3):
            my_cursor.execute("UPDATE dataset_3 SET value = %s WHERE dataset_3.id = %s", (value, id))
        if(dataset == 4):
            my_cursor.execute("UPDATE dataset_4 SET value = %s WHERE dataset_4.id = %s", (value, id))
        self.baza.commit()

    def izracunaj_deadband(self, iz_baze, pristigla_vrednost):
        deadband = abs(pristigla_vrednost - iz_baze) / iz_baze * 100
        return deadband

if _name_ == "_main_":
    worker = Worker()
    if worker.konektuj_sa_load_balancerom():
        print("uspesna konekcija sa LB.\n")
        worker.worker_sa_readerom.connect((socket.gethostname(), 9000))
        worker.primi_podatke()
