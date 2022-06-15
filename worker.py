import socket

class Worker:
    def __init__(self):
        self.worker_sa_load_balancerom = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def konektuj_sa_load_balancerom(self):
        try:
            self.worker_sa_load_balancerom.bind((socket.gethostname(), 1001))
            self.worker_sa_load_balancerom.listen(4)
            print("Slusam...")
            konekcija, adresa = self.worker_sa_load_balancerom.accept()
            
        except socket.error:
            print("Neuspesna konekcija sa loadBalancerom")
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
    worker = Worker()
    if worker.konektuj_sa_load_balancerom():
        print("Sve konektovano.")
        input()
         
