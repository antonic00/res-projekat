from socket import socket
import socket

class Reader:
    def __init__(self):
        self.reader_to_worker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def konektuj_sa_workerom(self):  
        try:
            soket, adresa = self.reader_to_worker.accept()
        except socket.error:
            print("Neuspesna konekcija sa workerom")
            return False
        print("Konektovao se sa Workerom.")
        return soket

    def priprema_soketa(self):
            self.reader_to_worker.bind((socket.gethostname(), 9000))
            self.reader_to_worker.listen(4)



if __name__ == "__main__":
    reader = Reader()
    reader.priprema_soketa()
    while(True):
        soket = reader.konektuj_sa_workerom()
