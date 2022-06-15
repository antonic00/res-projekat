class Historical_Collection:
    def __init__(self):
        self.worker_properties = []
    def dodaj_u_niz_propertija(self, code, value):
        self.worker_properties.append((code, value))
