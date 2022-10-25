import sqlite3


def get_connection(url='iq_option.db'):
    conn = sqlite3.connect(url, check_same_thread=False)
    return conn


def get_estado(conn: sqlite3.Connection) -> int:
    cursor = conn.cursor()
    estados = cursor.execute('SELECT * FROM estados')
    valor_estado = estados.fetchone()
    valor_estado = valor_estado[1]

    return int(valor_estado)


def set_estado(conn: sqlite3.Connection, value: int):
    try:

        cursor = conn.cursor()
        estados = cursor.execute(f'UPDATE estados SET status = {value} WHERE id = 1')
        conn.commit()
    except ConnectionError:
        print('Erro de Conexão...')


def get_login(conn: sqlite3.Connection):
    cursor = conn.cursor()
    users = cursor.execute('SELECT * FROM users')
    user = users.fetchone()
    return user


def set_login(conn: sqlite3.Connection, email: str, senha: str):
    try:
        cursor = conn.cursor()
        data = cursor.execute(f"UPDATE users SET email = '%s', senha = '%s' WHERE id = 1" % (email, senha))
        conn.commit()
    except ConnectionError:
        print('Erro de Conexão...')


def save_sinal(conn: sqlite3.Connection, sinal: dict):
    try:
        cursor = conn.cursor()
        insere = cursor.execute("INSERT INTO sinais VALUES (?, ?, ?, ?, ?, ?)",
                                (sinal['Moeda'], sinal["Action"], sinal["Horario"], int(sinal["Time_Frame"]),
                                 sinal["Origem"], sinal["Status"]))
        conn.commit()
    except Exception as e:
        print(e)


def get_sinais(conn: sqlite3.Connection):
    cursor = conn.cursor()
    sinais = cursor.execute('SELECT rowid, * FROM sinais WHERE status = 1')
    return sinais.fetchall()


def atualiza_sinal(conn: sqlite3.Connection, rowid: int):
    try:
        cursor = conn.cursor()
        sinal = cursor.execute(f'UPDATE sinais SET status = 0 WHERE rowid = {rowid}')
        conn.commit()
    except ConnectionError:
        print('Erro ao atualizar o sinal...')

