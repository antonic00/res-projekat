import pickle
from socket import socket
from _thread import *
from database_functions import dobavi_podatak, konekcija
import socket

class Reader:
    def __init__(self): # pragma: no cover
        self.reader_to_worker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.baza = None
    def konektuj_sa_workerom(self): # pragma: no cover
        try:
            soket, adresa = self.reader_to_worker.accept()
        except socket.error:
            print("Neuspesna konekcija sa workerom")
            return False
        print("Konektovao se sa Workerom.")
        return soket
    
    def primi_podatke(self, soket):
        self.baza = konekcija()
        while(True):
            data = soket.recv(4096)
            try:
                buffer = pickle.loads(data)
            except EOFError:
                continue

            kod = buffer[0]
            vrednost = buffer[1]

            rezultat = self.citanje_iz_baze(self.baza, kod)
            
            for line in rezultat:
                print(line)


    def priprema_soketa(self): # pragma: no cover
            self.reader_to_worker.bind((socket.gethostname(), 10000))
            self.reader_to_worker.listen(4)
    
    def citanje_iz_baze(self, baza, kod):
        my_cursor = baza.cursor()
        lista = list()
        lista.append(kod)
        my_cursor.execute("SELECT * FROM baza_podataka.dataset_1 WHERE dataset_1.code = %s", lista)
        rezultat = my_cursor.fetchall()
        if len(rezultat) != 0:
            return rezultat

        my_cursor.execute("SELECT * FROM baza_podataka.dataset_2 WHERE dataset_2.code = %s", lista)
        rezultat = my_cursor.fetchall()
        if len(rezultat) != 0:
            return rezultat

        my_cursor.execute("SELECT * FROM baza_podataka.dataset_3 WHERE dataset_3.code = %s", lista)
        rezultat = my_cursor.fetchall()
        if len(rezultat) != 0:
            return rezultat

        my_cursor.execute("SELECT * FROM baza_podataka.dataset_4 WHERE dataset_4.code = %s", lista)
        rezultat = my_cursor.fetchall()
        return rezultat

if __name__ == "__main__": # pragma: no cover
    reader = Reader()
    reader.priprema_soketa()
    while(True):
        soket = reader.konektuj_sa_workerom()
        start_new_thread(reader.primi_podatke, (soket, ))
