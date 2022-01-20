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
        

    def findRecords(self, table, attribute, **kwargs):
        '''
        Restituisce la sequenza corrispondente ad 
        un dato comando
        
        '''
        sql = f'SELECT {attribute} FROM {table}'
        if 'condition' in kwargs:
            sql += f' WHERE {kwargs.get("condition")}'
        print(sql)
        self.cur.execute(sql)
        seq = self.cur.fetchall()
        print(seq)

        return seq
    
    def add(self, table, *args, **kwargs):
        try:
            val = ','.join(f'"{i}"' for i in args)
            if 'columns' in kwargs:
                name_col = kwargs.get('columns')
                sql = f'INSERT INTO {table} ({name_col}) VALUES ({val})'
            else:
                sql = f'INSERT INTO {table} VALUES ({val})'

            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            return False
        return True
    

    def close(self):
        '''chiude la connessione con il db'''
        self.cur.close()
        self.conn.close()
