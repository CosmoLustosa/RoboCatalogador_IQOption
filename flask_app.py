from bot import liga_bot
from connect import get_connection, set_estado, get_estado
from flask import Flask, render_template
from threading import Thread


conn = get_connection()
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')



@app.route('/bot')
def ligaBot():

    estado = get_estado(conn)

    if int(estado) == 0:

        t = Thread(target=liga_bot)
        t.start()
        set_estado(conn, 1)

        return render_template('ligabot.html', msg='Ligando Bot')
    else:
        return render_template('ligabot.html', msg='O Bot já está ligado!')


@app.route('/zera_status')
def zera_status():
    estado = get_estado(conn)
    if estado == 1:
        set_estado(conn, 0)
    return render_template('status.html')


if __name__ == '__main__':
    app.run(debug=True)
