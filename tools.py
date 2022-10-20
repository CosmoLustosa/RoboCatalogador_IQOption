from datetime import datetime
from connect import get_connection, get_sinais, get_login, atualiza_sinal
from iqoptionapi.stable_api import IQ_Option
from threading import Thread
import time


conn = get_connection()
login = get_login(conn)

API = IQ_Option(login[1], login[2])
API.connect()
# def save_all(collection_name: collection, lista_sinais):
#     collection_name.insert_many(lista_sinais)
#
#
# def save_signal(collection_name: collection, sinal: dict):
#     collection_name.insert_one(sinal)
#
#
# def get_signals(colection_name, sinais: dict):
#     colecao = colection_name.find(sinais,
#                                   {"_id": 1, "Horario": 1, "Moeda": 1, "Time_Frame": 1, "Action": 1, "Origem": 1,
#                                    "Status": 1}).sort("Horario")
#     return colecao
#
#
# def atualiza_status(collection: collection, id_registro):
#     """atualiza o registro no banco de dado para close (ja fechado)"""
#     consulta = {'_id': id_registro}
#     values = {"$set": {"Status": "Close"}}
#     collection.update_one(consulta, values)


def busca_pares_abertos():
    ativo_aberto = []

    try:
        paridades = API.get_all_open_time()
    except:
        print("Erro ao buscar os pares abertos!")

    for par in paridades['digital']:
        if paridades['digital'][par]['open'] == True:
            ativo_aberto.append((par, "digital"))

    for par in paridades['binary']:
        if paridades['binary'][par]['open'] == True:
            if (par, "digital") not in ativo_aberto:  # exclui os pares que ja estao aberto em digital
                ativo_aberto.append((par, "binary"))

    return ativo_aberto


def abre_ordem_digital(active, amount, action, duration, id_registro):
    try:
        status, order_id = API.buy_digital_spot_v2(active, amount, action, duration)  # abre uma ordem!
        atualiza_sinal(conn, id_registro)
    except KeyError:
        print("Par Inválido...")


    if status:
        print(f'Compra aberta em {active} - {action} - às {datetime.now().strftime("%d/%m/%y %H:%M:%S")} horas!')
        while True:

            st, lucro = API.check_win_digital_v2(order_id)
            if (type(lucro) == float or type(lucro) == int) and lucro <= 0:
                try:
                    API.buy_digital_spot_v2(active, amount*2, action, duration)  # abre uma ordem!
                except KeyError:
                    print("Par Inválido...")
                print("ABRINDO GALE...")
                break
            elif (type(lucro) == float or type(lucro) == int) and lucro > 0:
                print("GAIN SEM GALE...")
                break
    else:
        print("Nenhuma Operação Aberta...")

def abre_ordem_binaria(active, amount, action, duration):
    status, order_id = API.buy(amount, active, action, duration)  # abre uma ordem!
    if status:
        print(f'Compra aberta em {active} - {action} - às {datetime.now().strftime("%d/%m/%y %H:%M:%S")} horas!')
        while True:

            st, lucro = API.check_win_v4(order_id)
            if (type(lucro) == float or type(lucro) == int) and lucro <= 0:
                API.buy(amount*2, active, action, duration)  # abre uma ordem!
                print("ABRINDO GALE...")
                break
            elif (type(lucro) == float or type(lucro) == int) and lucro > 0:
                print("GAIN SEM GALE...")
                break
    else:
        print("Nenhuma Operação Aberta...")


# def executa_ordem(active, amount, action, duration, collection, id_registro, tipo: str):
#     if tipo == "digital":
#
#         status, order_id = API.buy_digital_spot_v2(active, amount, action, duration)  # abre uma ordem!
#
#         if status:
#             # time.sleep(4 * 60)
#             while True:
#                 status, lucro = API.check_win_digital_v2(order_id)
#                 if status and lucro < 0:
#                     API.buy_digital_spot_v2(active, amount + 1, action, duration)  # abre uma ordem!
#                     break
#
#         atualiza_status(collection, id_registro)
#
#     else:
#
#         status, order_id = API.buy(amount, active, action, duration)  # abre uma ordem na op. binária!
#
#         if status:
#             # time.sleep(4 * 60)
#             while True:
#                 status, lucro = API.check_win_v4(order_id)
#                 if status and lucro < 0:
#                     API.buy(amount + 1, active, action, duration)
#                     break
#
#
#         atualiza_status(collection, id_registro)


def executa_ordens():
    while True:
        temp = datetime.now()
        if temp.minute % 5 == 0:
            lista_threads_operacoes = []
            sinais = get_sinais(conn)
            for sinal in sinais:
                data = datetime.strptime(sinal[3], '%d/%m/%y %H:%M') #verifica o horario da entrada
                if data.minute == temp.minute:

                    t = Thread(target=abre_ordem_digital,
                               args=(sinal[1], 5, sinal[2], sinal[4], sinal[0]))
                    lista_threads_operacoes.append(t)
                    t.start()

            time.sleep(4.9*60)
