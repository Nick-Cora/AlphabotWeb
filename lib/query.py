'''
Andrea Tomatis

Verifica 25/11/2021

database lib
'''

import sqlite3
from sqlite3 import Error



class Db_Connection():
    '''
    Classe per interfacciarsi con il database. Contiene diverse funzioni per 
    le query e la chiusura della connessione con il db.
    '''
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = self.create_connection(db_file)
        self.cur = self.conn.cursor()
        
    def create_connection(self, db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)
        return conn
        

    def findCommand(self, cn):
        '''
        Restituisce la sequenza corrispondente ad 
        un dato comando
        '''
        self.cur.execute(f'SELECT sequenza FROM Movimenti WHERE nome = "{cn}"')
        seq = self.cur.fetchall()
        print(seq)

        return seq[0][0].split(';')
    

    def close(self):
        '''chiude la connessione con il db'''
        self.cur.close()
        self.conn.close()