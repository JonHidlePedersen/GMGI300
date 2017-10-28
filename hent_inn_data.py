# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import psycopg2

class Postgres_data_insert:
    """This class inserts data into a PostgreSQL database.
    
    Parameters
    ----------
    db_name : 
    """
    
    
    def __init__(self, db_name = 'gmgi300db', dbuser = 'postgres', dbpassword = 'postgres'):
        """Constructor for the instance."""
        self.db_name = db_name
        self.dbuser = dbuser
        self.dbpassword = dbpassword   
    
    
     
    def connect(self):
        """ Connect to the PostgreSQL database server """
        try:
           
            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            self.conn = psycopg2.connect("dbname='gmgi300db' user='postgres' password='postgres'")
     
            # create a cursor
            self.cur = self.conn.cursor()
            
            # execute a statement
            print('PostgreSQL database version:')
            self.cur.execute('SELECT version()')
     
            # display the PostgreSQL database server version
            self.db_version = self.cur.fetchone()
            print(self.db_version)
           
            
            print('Database connection established.')
            
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        
        
     
    
    
    def insert_data(self):
        # execute a statement
        self.cur.execute("INSERT INTO loype (punkt) VALUES (ST_GeometryFromText('POINT(50 20)'))")
        self.conn.commit()
        print('Data added.')

    
    def disconnect(self):
        # close the communication with the PostgreSQL
        self.cur.close()
        print('Database connection ended.')
 
if __name__ == '__main__':
    sette_inn_data = Postgres_data_insert()
    sette_inn_data.connect()
    sette_inn_data.insert_data()
    sette_inn_data.disconnect()
    
    