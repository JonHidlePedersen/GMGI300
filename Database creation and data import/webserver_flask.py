from flask import Flask, render_template
import hent_inn_data

app = Flask(__name__, template_folder="../Openlayers")


# Starts the webserver and opens the .html file.
@app.route('/')
def index(name=None):
    return render_template('prosjekt_web.html', name=name)


# When button is clicked a script is run. The webpage is reloaded.
@app.route('/kjor_hent_inn_data', methods=['GET', 'POST'])
def parse1(name=None):
    data_from_file = 'preppemaskin_aas_2010_01-03.txt'

    connect_and_insert = hent_inn_data.PostgresDataInsert()
    connect_and_insert.connect()
    connect_and_insert.create_table_loype()
    connect_and_insert.extractdatafromfile(data_from_file)
    connect_and_insert.insert_into_loype()
    connect_and_insert.disconnect()
    return render_template('prosjekt_web.html', name=name)


# When button is clicked a script is run. The webpage is reloaded.
@app.route('/kjor_simulering', methods=['GET', 'POST'])
def parse2(name=None):
    data_from_file = 'preppemaskin_aas_2010_01-03.txt'

    connect_and_insert = hent_inn_data.PostgresDataInsert()
    connect_and_insert.connect()
    connect_and_insert.create_table_simulering()
    connect_and_insert.extractdatafromfile(data_from_file)
    connect_and_insert.run_simulation(0.1)
    connect_and_insert.disconnect()
    return render_template('prosjekt_web.html', name=name)


if __name__ == '__main__':
    app.run()
    app.debug = True
