from flask import Flask, render_template

app = Flask(__name__, template_folder="../Openlayers")

@app.route('/')
def index(name=None):
    return render_template('HTML5.html',name=name)

@app.route('/kjor_simulering', methods=['GET', 'POST'])
def parse(name=None):
    import simulering
    db_name = 'gmgi300db'
    dbuser = 'postgres'
    dbpassword = 'postgres'
    dbport = '5432'
    data_from_file = 'preppemaskin_aas_2010_01-03.txt'

    connect_and_insert = simulering.PostgresDataInsert(db_name, dbuser, dbpassword, dbport)
    connect_and_insert.connect()
    connect_and_insert.extractdatafromfile(data_from_file)
    connect_and_insert.run_simulation(0.001)
    connect_and_insert.disconnect()
    print("done")
    return render_template('HTML5.html',name=name)


if __name__ == '__main__':
    app.run()
    app.debug = True