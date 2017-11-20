# -*- coding: utf-8 -*-
"""
This file reads data from a .txt file and inserts it into a PostgreSQL database.
The module psycopg2 is needed.
"""

import psycopg2
import time


class PostgresDataInsert:
    """This class connects and inserts data into a PostgreSQL database."""

    def __init__(self, db_name='gmgi300db', dbuser='postgres',
                 dbpassword='postgres', dbport='5432'):
        """Constructor for the instance. Options for conecting to a database."""
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
                "dbname={0} user={1} password={2} port={3}"
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

    def create_table_loype(self):
        """ Creates the table loype containing the
            collums tid(PK) and point. The table stores the GNSS data from the
            track machine."""

        self.cur.execute(
            "DROP TABLE IF EXISTS loype;")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS loype "
            "(tid TIMESTAMP WITH TIME ZONE PRIMARY KEY, "
            "punkt geometry(POINT,4326,2));")
        self.conn.commit()
        print('Table loype created.')

    def create_table_simulering(self):
        """ Creates the table loype containing the
            collums tid(PK) and point. The table stores the simulated GNSS data
            from the track machine."""

        self.cur.execute(
            "DROP TABLE IF EXISTS simulering;")
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS simulering "
            "(id SERIAL, tid TIMESTAMP WITH TIME ZONE PRIMARY KEY, "
            "punkt geometry(POINT,4326,2));")
        self.conn.commit()
        print('Table simulering created.')

    def insert_into_loype(self):
        """ Inserts GNSS position and time into the PostgreSQL database. Loops
        through the lines in the output file from the extractdatafromfile
        function. Each line is inserted into a new row in the table."""

        print('Started inserting data into loype.')
        for i, line in enumerate(self.output):
            lat = line[0]
            lon = line[1]
            date_time = line[2]
            geo = 'Point({0} {1})'.format(str(lon), str(lat))
            self.cur.execute('INSERT INTO loype (tid, punkt) '
                             'VALUES (%s, (ST_GeometryFromText(%s , 4326)))'
                             , (date_time, geo))
        self.conn.commit()
        print('Finished inserting {0} rows into loype.'.format(i))

    def insert_into_simulation(self, simulation_delay=0.1, track_length=20):
        """ Inserts GNSS position and time into the PostgreSQL database. Loops
        through the lines in the output file from the extractdatafromfile
        function. Each line is inserted into a new row in the table. A time
        delay simulates realtime tracking of the track machine."""

        track_length = track_length
        print('Started inserting data into simulering.')
        for i, line in enumerate(self.output):
            lat = line[0]
            lon = line[1]
            date_time = line[2]
            geo = 'Point({} {})'.format(str(lon), str(lat))
            self.cur.execute('INSERT INTO simulering (tid, punkt) '
                             'VALUES (%s, (ST_GeometryFromText(%s , 4326)))'
                             , (date_time, geo))
            if i > track_length:
                teller = '{0}'.format(str(i - track_length))
                self.cur.execute(
                    'DELETE FROM simulering WHERE ID = {0}'.format(teller))

            self.conn.commit()
            time.sleep(simulation_delay)

    def disconnect(self):
        """ Disconnects from the PostgreSQL database server """
        self.cur.close()
        print('Database connection ended.\n')

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
        self.output = []
        for LINE in indata:
            splitdata = LINE.split(";")

            # Loop that evaluvates if a value is a number or a string.
            # Changes datatype if it is a number.
            for i, value in enumerate(splitdata):
                try:
                    if isinstance(eval(value), (float, int)):
                        splitdata[i] = eval(value)
                except SyntaxError:
                    pass  # String is not float or int.

            self.output.append(splitdata)

        return self.output

    def run_simulation(self, delaytime=0.1):
        """Function that inserts data into the table simulation with a delay."""
        self.create_table_simulering()
        self.insert_into_simulation(delaytime)


if __name__ == '__main__':
    # Reads data from the text file and inserts it into a database.
    database_name = 'gmgi300db'
    database_buser = 'postgres'
    database_password = 'postgres'
    database_port = '5432'
    data_from_file = 'preppemaskin_aas_2010_01-03.txt'
    delay = 0.01

    connect_and_insert = PostgresDataInsert(
        database_name, database_buser, database_password, database_port)
    connect_and_insert.connect()
    connect_and_insert.create_table_loype()
    connect_and_insert.extractdatafromfile(data_from_file)
    connect_and_insert.insert_into_loype()
    connect_and_insert.run_simulation()
    connect_and_insert.disconnect()
