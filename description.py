class Description:
    def __init__(self, id, dataset) :
        self.id = id
        self.lista_itema = list()
        self.dataset = dataset
    def dodaj_u_listu(self, kod, vrijednost):
        self.lista_itema.append((kod, vrijednost))
        
