import mysql.connector


def konekcija():
    baza = mysql.connector.connect(
        host = "localhost",
        database = "baza_podataka",
        user = "root",
        password = "admin")
    
    if baza.is_connected():
        print('Uspesna konekcija na bazu podataka!')
        
    return baza

def dobavi_podatak(id, baza):
    my_cursor = baza.cursor()
    lista = list()
    lista.append(id)
    my_cursor.execute("SELECT dataset_1.value FROM baza_podataka.dataset_1 WHERE dataset_1.id = %s", lista)
    rezultat = my_cursor.fetchall()
    if len(rezultat) != 0:
        return rezultat
    my_cursor.execute("SELECT dataset_2.value FROM baza_podataka.dataset_2 WHERE dataset_2.id = %s", lista)
    rezultat = my_cursor.fetchall()
    if len(rezultat) != 0:
        return rezultat
    my_cursor.execute("SELECT dataset_3.value FROM baza_podataka.dataset_3 WHERE dataset_3.id = %s", lista)
    rezultat = my_cursor.fetchall()
    if len(rezultat) != 0:
        return rezultat
    my_cursor.execute("SELECT dataset_4.value FROM baza_podataka.dataset_4 WHERE dataset_4.id = %s", lista)
    rezultat = my_cursor.fetchall()
    return rezultat
    
