# -*- coding: utf-8 -*-
"""
This file reads data from a .txt file and inserts it into a PostgreSQL database.
The module psycopg2 is needed.
"""

import psycopg2


class PostgresDataInsert:
    """This class inserts data into a PostgreSQL database.
    
    Parameters
    ----------
    db_name : 
    """

    def __init__(self, db_name='gmgi300db', dbuser='postgres',
                 dbpassword='postgres'):
        """Constructor for the instance."""
        self.db_name = db_name
        self.dbuser = dbuser
        self.dbpassword = dbpassword

    def connect(self):
        """ Connect to the PostgreSQL database server """
        try:

            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            self.conn = psycopg2.connect(
                "dbname='gmgi300db' user='postgres' password='postgres'")

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

    def insert_data(self, lat=59.672, long=10.795,
                    date_time='2011-03-03 10:56:04+00'):
        """ Inserts position and time data into the Postgre database. """
        self.cur.execute(
            "INSERT INTO loype (punkt,tid) \
             VALUES (ST_GeometryFromText('POINT(%s %s)'), %s)",
            (lat, long, date_time))
        self.conn.commit()
        print('Data added.')

    def disconnect(self):
        """ Disconnects from the PostgreSQL database server """
        self.cur.close()
        print('Database connection ended.')


def extractdatafromfile(filnamn):
    """
    Inputt: text or csv file.
    This function reads data from a file and stores it in a list. Each line is stored in a seperate list and changes the inputt to str, int or float.
    Outputt: A nested list.
    """

    ## Reads the file.
    infile = open(filnamn, "r")
    indata = infile.readlines()
    infile.close()

    ## Splits data using ; and changes numbers from str to int/float.
    splitdata = []
    outputt = []
    for line in indata:
        splitdata = line.split(";")

        # Loop that evaluvates if a value is a number or a string. Changes datatype if it is a number.
        for i, value in enumerate(splitdata):
            try:
                if isinstance(eval(value), (float, int)):
                    splitdata[i] = eval(value)
            except:
                """String is not float or int."""

        outputt.append(splitdata)

    return outputt


if __name__ == '__main__':
    kk = extractdatafromfile('preppemaskin_aas_2010_01-03.txt')
    print(kk[1][2])

    for line in kk:

    # sette_inn_data = PostgresDataInsert()
    # sette_inn_data.connect()
    # sette_inn_data.insert_data()
    # sette_inn_data.disconnect()
