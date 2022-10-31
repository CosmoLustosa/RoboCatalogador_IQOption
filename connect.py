import mysql.connector

db = mysql.connector.connect(host='localhost', user='root', password='tocar123', database="iq_option")


def get_connection(db=db):
    return db


def get_estado(conn: mysql.connector.MySQLConnection) -> int:
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM estados')
    estados = cursor.fetchone()
    return estados[1]


def set_estado(conn: mysql.connector.MySQLConnection, value: int):
    try:

        cursor = conn.cursor()
        cursor.execute(f'UPDATE estados SET status = {value} WHERE id = 1')
        conn.commit()
    except ConnectionError:
        print('Erro de Conexão...')


def get_login(conn: mysql.connector.MySQLConnection):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    user = cursor.fetchone()
    return user


def set_login(conn: mysql.connector.MySQLConnection, email: str, senha: str):
    try:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE users SET email = '%s', senha = '%s' WHERE id = 1" % (email, senha))
        conn.commit()
    except ConnectionError:
        print('Erro de Conexão...')


def save_sinal(conn: mysql.connector.MySQLConnection, sinal: dict):
    try:
        cursor = conn.cursor()
        query = 'INSERT INTO sinais (ativo, action, horario, time, origem, status)  VALUES (%s, %s, %s, %s, %s, %s)'
        valores = (sinal["Moeda"], sinal["Action"], sinal["Horario"], sinal["Time_Frame"], sinal["Origem"], sinal["Status"])
        cursor.execute(query, valores)
        conn.commit()
    except Exception as e:
        print(e)


# dict_dado = {'Moeda': 'GBPUSD', 'Action': 'PUT', 'Horario': '31/10/2022 13:15', 'Time_Frame': 5, 'Origem': 'ultimo lancamento',
#              'Status': 1}
# save_sinal(db, dict_dado)
# print('Salvou os dados')


def get_sinais(conn: mysql.connector.MySQLConnection):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sinais WHERE status = 1')
    return cursor.fetchall()


def atualiza_sinal(conn: mysql.connector.MySQLConnection, id: int):
    try:
        cursor = conn.cursor()
        cursor.execute(f'UPDATE sinais SET status = 0 WHERE id = {id}')
        conn.commit()
    except ConnectionError:
        print('Erro ao atualizar o sinal...')


