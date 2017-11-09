# -*- coding: utf-8 -*-
"""
This file reads data from a .txt file and inserts it into a PostgreSQL database.
The module psycopg2 is needed.
"""

import psycopg2


class PostgresDataInsert:
    """This class connects and inserts data into a PostgreSQL database.
    
    Parameters
    ----------
    db_name : 
    """

    def __init__(self, db_name='gmgi300db', dbuser='postgres',
                 dbpassword='postgres', dbport='5432'):
        """Constructor for the instance."""
        self.db_name = db_name
        self.dbuser = dbuser
        self.dbpassword = dbpassword
        self.dbport = dbport

    def connect(self):
        """ Connect to the PostgreSQL database server """
        try:

            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            self.conn = psycopg2.connect(
                "dbname={0} user={1} password={2} port={3}".format(self.db_name,
                                                                   self.dbuser,
                                                                   self.dbpassword,
                                                                   self.dbport))

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

    def create_loype(self):
        """ Creates the table loype containing the
            collums id(PK), time and point"""

        self.cur.execute(
            "DROP TABLE IF EXISTS loype;")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS loype (id SERIAL PRIMARY KEY, \
            tid TIMESTAMP WITH TIME ZONE, punkt geometry(POINT,4326,2));")
        self.conn.commit()
        print('Table loype created.')

    def create_loypetid(self):
        """ Creates the table loype_tid containing the
                    collums time and point"""

        self.cur.execute(
            "DROP TABLE IF EXISTS loypetid;")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS loypetid AS select tid from loype;")
        self.conn.commit()
        print('Table loypetid created.')

    def insert_data(self, lat=59.672, long=10.795,
                    date_time='2011-03-03 10:56:04+00'):
        """ Inserts position and time data into the Postgre database. """

        geo = 'Point({} {})'.format(str(long), str(lat))
        self.cur.execute('INSERT INTO loype (tid, punkt) '
                         'VALUES (%s, (ST_GeometryFromText(%s , 4326)))'
                         , (date_time, geo))
        self.conn.commit()

    def disconnect(self):
        """ Disconnects from the PostgreSQL database server """
        self.cur.close()
        print('Database connection ended.')


def extractdatafromfile(filnamn):
    """
    Inputt: text or csv file.
    This function reads data from a file and stores it in a list. Each line is
    stored in a seperate list and changes the inputt to str, int or float.
    Outputt: A nested list.
    """

    # Reads the file.
    infile = open(filnamn, "r")
    indata = infile.readlines()
    infile.close()

    # Splits data using ; and changes numbers from str to int/float.
    outputt = []
    for LINE in indata:
        splitdata = LINE.split(";")

        # Loop that evaluvates if a value is a number or a string.
        # Changes datatype if it is a number.
        for i, value in enumerate(splitdata):
            try:
                if isinstance(eval(value), (float, int)):
                    splitdata[i] = eval(value)
            except:
                """String is not float or int."""

        outputt.append(splitdata)

    return outputt


if __name__ == '__main__':
    # Reads data from the text file and inserts it into a database.
    db_name = 'gmgi300db'
    dbuser = 'postgres'
    dbpassword = 'postgres'
    dbport = '5432'

    lopyemaskin_data = extractdatafromfile('preppemaskin_aas_2010_01-03.txt')
    connect_and_insert = PostgresDataInsert(db_name, dbuser, dbpassword dbport)
    connect_and_insert.connect()
    connect_and_insert.create_loype()


    for i, line in enumerate(lopyemaskin_data):
        connect_and_insert.insert_data(line[0], line[1], line[2])
    connect_and_insert.create_loypetid()
    connect_and_insert.disconnect()
