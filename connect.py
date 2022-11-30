import mysql.connector
import sqlite3

# db = mysql.connector.connect(host='localhost', user='root', password='tocar123', database="iq_option")
db = sqlite3.connect('iq_option.db')

def get_connection(db: sqlite3.Connection):
    return db


def get_estado(db: sqlite3.Connection) -> int:
    cursor = db.cursor()
    cursor.execute('SELECT * FROM estados')
    estados = cursor.fetchone()
    return estados[1]


def set_estado(conn: sqlite3.Connection, value: int):
    try:

        cursor = conn.cursor()
        cursor.execute(f'UPDATE estados SET status = {value} WHERE id = 1')
        conn.commit()
    except ConnectionError:
        print('Erro de Conexão...')


def get_login(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    user = cursor.fetchone()
    return user


def set_login(conn: sqlite3.Connection, email: str, senha: str):
    try:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE users SET email = '%s', senha = '%s' WHERE id = 1" % (email, senha))
        conn.commit()
    except ConnectionError:
        print('Erro de Conexão...')


def save_sinal(conn: sqlite3.Connection, sinal: dict):
    try:
        cursor = conn.cursor()
        query = 'INSERT INTO sinais (ativo, action, horario, time, origem, status)  VALUES (%s, %s, %s, %s, %s, %s)'
        valores = (sinal["Moeda"], sinal["Action"], sinal["Horario"], sinal["Time_Frame"], sinal["Origem"], sinal["Status"])
        cursor.execute(query, valores)
        conn.commit()
    except Exception as e:
        print(e)


def get_sinais(conn=db):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sinais WHERE status = 1')
    return cursor.fetchall()


def atualiza_sinal(conn: sqlite3.Connection, id:int):
    try:
        cursor = conn.cursor()
        cursor.execute(f'UPDATE sinais SET status = 0 WHERE id = {id}')
        conn.commit()
    except ConnectionError:
        print('Erro ao atualizar o sinal...')


print(get_sinais(db))