# -*- coding: utf-8 -*-
"""
This file reads data from a .txt file and inserts it into a PostgreSQL database.
The module psycopg2 is needed.
"""

import psycopg2
import time


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
                "dbname={0} user={1} password={2} port={3}" \
                    .format(self.db_name,
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


    def create_table_loypetid(self):
        """ Creates the table loypetid containing the
            collums id(PK), time and point"""

        self.cur.execute(
            "DROP TABLE IF EXISTS loypetid;")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS loypetid (id SERIAL PRIMARY KEY, \
            tid TIMESTAMP WITH TIME ZONE, punkt geometry(POINT,4326,2));")
        self.conn.commit()
        print('Table loypetid created.')

    def insert_position_data(self, delay=0):
        """ Inserts position and time data into the Postgre database. """

        print('Started inserting data into loype.')
        for i, line in enumerate(self.outputt):
            lat = line[0]
            lon = line[1]
            date_time = line[2]
            geo = 'Point({} {})'.format(str(lon), str(lat))
            self.cur.execute('INSERT INTO loypetid (tid, punkt) '
                             'VALUES (%s, (ST_GeometryFromText(%s , 4326)))'
                             , (date_time, geo))
            self.conn.commit()
            time.sleep(delay)
            print(i)
        print('Finished inserting {0} rows into loype.'.format(i))

    def disconnect(self):
        """ Disconnects from the PostgreSQL database server """
        self.cur.close()
        print('Database connection ended.')

    def extractdatafromfile(self, filnamn):
        """
        Inputt: text or csv file.
        This function reads data from a file and stores it in a list. Each line
        is stored in a seperate list and changes the inputt to str, int or
        float.
        Outputt: A nested list.
        """

        # Reads the file.
        infile = open(filnamn, "r")
        indata = infile.readlines()
        infile.close()

        # Splits data using ; and changes numbers from str to int/float.
        self.outputt = []
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

            self.outputt.append(splitdata)

        return self.outputt

    def run_simulation(self, delaytime):
        self.create_table_loypetid()
        self.insert_position_data(delaytime)


if __name__ == '__main__':
    # Reads data from the text file and inserts it into a database.
    db_name = 'gmgi300db'
    dbuser = 'postgres'
    dbpassword = 'postgres'
    dbport = '5432'
    data_from_file = 'preppemaskin_aas_2010_01-03.txt'

    connect_and_insert = PostgresDataInsert(db_name, dbuser, dbpassword, dbport)
    connect_and_insert.connect()
    connect_and_insert.extractdatafromfile(data_from_file)
    connect_and_insert.run_simulation(0.01)
    connect_and_insert.disconnect()
