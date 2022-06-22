class Broj_Workera:
    def __init__(self):
        self.broj_workera = -1

    def povecaj_broj_workera(self):
        self.broj_workera += 1
    
    def smanji_broj_workera(self):
        self.broj_workera -= 1
    
    def get_broj_workera(self):
        return self.broj_workera
