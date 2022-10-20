import re
from connect import get_connection, save_sinal
from datetime import datetime

conn = get_connection()


# def get_bwinary_free(text: str):
#     inputs = re.findall(r'[M][0-9]+ [A-Z]{6} [A-Z]+ [0-9]{2}[:][0-9]{2}', text)
#     if len(inputs) > 0:
#       pass
#     else:
#         get_bwinary_free_avulsa(text)


# pronto
def get_breno_trader(text: str):
    dados = text.strip().split('\n')
    timeframe = dados[0][7]
    par = dados[1].strip()
    hora = dados[2]
    action = "CALL" if "COMPRA" in dados[3] else "PUT"
    dict_info = {}
    # colecao = connect()  # abre a conexão e cria a coleção
    dict_info["Horario"] = datetime.now().strftime("%d/%m/%y") + f" {hora}"
    dict_info["Moeda"] = par
    dict_info["Time_Frame"] = int(timeframe)
    dict_info["Action"] = action
    dict_info["Origem"] = "Breno Trader"
    dict_info["Status"] = 1
    save_sinal(conn, dict_info)


# pronto
def get_tigre_sinais(text: str):
    time_frame = re.findall(r'[M][0-9]+', text)
    time_frame = time_frame[0].replace('M', "")

    entradas = re.findall(r'[0-9]{2}[:][0-9]{2} [A-Z]{6} [-] [A-Z]{3}', text)

    if len(entradas) > 0:
        dict_info = {}
        list_dados = []
        for entrada in entradas:
            dado = entrada.split(" ")
            horario = dado[0]
            par = dado[1]
            action = "CALL" if str(dado[3]) == "CAL" else "PUT"

            dict_info["Horario"] = datetime.now().strftime("%d/%m/%y") + f" {horario}"
            dict_info["Moeda"] = par
            dict_info["Time_Frame"] = int(time_frame)
            dict_info["Action"] = action
            dict_info["Origem"] = "Tigre dos Sinais"
            dict_info["Status"] = 1
            save_sinal(conn, dict_info)
        #     d = dict(dict_info)
        #     list_dados.append(d)
        # mycolecao.insert_many(list_dados)


# pronto
def get_padrão_avulso(text: str):
    dados = text.strip().split(" ")
    dict_info = {}
    action = ""

    if len(dados) >= 4:
        dict_info["Horario"] = datetime.now().strftime("%d/%m/%y") + f" {dados[2]}"
        dict_info["Moeda"] = dados[1]
        dict_info["Time_Frame"] = int(dados[0].replace("M", ""))
        dict_info["Action"] = dados[3]
        dict_info["Origem"] = "Sinal Avulso"
        dict_info["Status"] = 1
        # colecao = connect() #abre a conexão e cria a coleção
        # save_signal(mycolecao, dict_info)


# pronto
def get_extensao_vip(text: str):
    par = re.search(r"[A-Z]{6}", text)
    par = par.group()
    horario = re.search(r"[0-9]{2}:[0-9]{2}", text)
    horario = horario.group()
    time_frame = re.search(r"[M][0-9]+", text)
    time_frame = time_frame.group()
    operacao = re.search(r"PUT", text)
    action = "CALL"
    if operacao:
        action = "PUT"

    dict_info = {}
    dict_info["Horario"] = datetime.now().strftime("%d/%m/%y") + f" {horario}"
    dict_info["Moeda"] = par
    dict_info["Time_Frame"] = int(time_frame.replace("M", ""))
    dict_info["Action"] = action
    dict_info["Origem"] = "Extensão Vip"
    dict_info["Status"] = 1
    # colecao = connect()  # abre a conexão e cria a coleção
    save_sinal(conn, dict_info)


# pronto
def get_sinais_gold(text: str):
    par = re.search(r"[A-Z]{3}[/][A-Z]{3}", text)
    par = par.group().replace("/", "")
    time_frame = re.search(r"[0-9]+[A-Z]{3}", text)
    time_frame = time_frame.group().replace("MIN", "")
    horario = re.search(r"[0-9]{2}:[0-9]{2}", text)
    horario = horario.group()
    action = re.search(r"PUT", text)
    action = "PUT" if action != None else "CALL"
    dict_info = {}
    dict_info["Horario"] = datetime.now().strftime("%d/%m/%y") + f" {horario}"
    dict_info["Moeda"] = par
    dict_info["Time_Frame"] = int(time_frame)
    dict_info["Action"] = action
    dict_info["Origem"] = "Sinais Gold ao Vivo"
    dict_info["Status"] = 1
    save_sinal(conn, dict_info)


def get_rick_trader(text: str):
    horario = re.search(r'[0-9]{2}:[0-9]{2}', text)
    horario = horario.group()
    par = re.search(r'[A-Z]{3}/[A-Z]{3}', text)
    par = par.group().replace('/', '')
    time_frame = re.search(r'[5]{1}[a-z]{3}', text)
    time_frame = time_frame.group().replace('min', '')
    action = "PUT" if re.search(r'VENDA', text) else "CALL"
    dict_info = {}
    dict_info["Horario"] = datetime.now().strftime("%d/%m/%y") + f" {horario}"
    dict_info["Moeda"] = par
    dict_info["Time_Frame"] = int(time_frame)
    dict_info["Action"] = action
    dict_info["Origem"] = "Rick Trader"
    dict_info["Status"] = 1
    save_sinal(conn, dict_info)


def get_eldorado_sinais(text: str):
    horario = re.search(r'[0-9]{2}:[0-9]{2}', text)
    horario = horario.group()
    # print(horario)

    par = re.search(r': [A-Z]{6}', text)
    par = par.group().strip().replace(': ', '')
    # print(par)

    time_frame = re.search(r'[M]{1}[0-9]+', text)
    time_frame = time_frame.group().replace('M', '')
    time_frame = int(time_frame)
    print(time_frame)

    action = "PUT" if re.search(r'PUT', text) else "CALL"
    # action = action.group()
    # print(action)