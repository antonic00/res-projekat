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
