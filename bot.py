# -*- coding: utf-8 -*-
import telebot
from connect import get_connection, set_estado, get_estado, get_login, get_sinais
from tools import executa_ordens
from threading import Thread
import json
from catalogo import get_breno_trader, get_tigre_sinais, get_padrão_avulso, get_extensao_vip, get_sinais_gold, \
    get_rick_trader

conn = get_connection()
API_KEY = get_login(conn)[3]
bot = telebot.TeleBot(API_KEY)


def liga_bot():
    # conn = get_connection()
    # print('Conexao: ', conn)
    # estado = get_estado(conn)
    # print('Estado: ', estado)
    # set_estado(conn, 1)

    @bot.message_handler(commands=['executa_ordens'])
    def lista_operacoes(message):
        executa_ordens()
        bot.send_message(message.chat.id, text="Iniciando as operações...")

    @bot.message_handler(commands=['para_bot'])
    def parar_bot(message):
        bot.send_message(message.chat.id, text="Parando Bot...")
        try:
            set_estado(conn, 0)
            bot.stop_bot()
        except:
            print("Bot Parado")

    @bot.message_handler(commands=['mostra_padrao'])
    def mostra_padrao_texto(message):
        bot.send_message(message.chat.id, text="M5 PARPAR 00:00 CALL")

    @bot.message_handler(commands=['mostra_entradas'])
    def mostra_entradas(message):

        entradas = get_sinais(conn)

        if entradas is not None:
            for entrada in entradas:
                texto = f'''========================
Horário: {entrada[3]}
Par: {entrada[1]}
Time Frame: {entrada[4]}
Tipo: {entrada[2]}
Sala de Origem: {entrada[5]}
Status: {entrada[6]}
========================
        '''
                bot.send_message(message.chat.id, text=texto)

        else:

            bot.send_message(message.chat.id, text="Nenhuma entrada aberta!")

    @bot.message_handler(commands=['menu'])
    def menu(message):
        texto = """
            Escolha uma das opções abaixo para continuar:
            /menu - exibe o menu
            /executa_ordens - lista as operações abertas
            /consulta_proxima_operacao - mostra a próxima operação a ser aberta
            /mostra_padrao - mostra o padrao das mensagens de entrada
            /mostra_entradas - mostra entradas que serão efetuadas
            /para_bot - para o robo

        """
        bot.send_message(message.chat.id, text=texto)

    # =============== python verifica o menu por último =========
    def disponibiliza_menu(message):
        return True

    @bot.message_handler(func=disponibiliza_menu)
    def send_welcome(message):
        try:

            mensagem = json.dumps(message.json)  # convert em string json
            dict_text = json.loads(mensagem)  # convert em dict
            print(message.json)

            if "forward_from" in dict_text:

                if dict_text['forward_from']['id'] == 1180878831:
                    get_breno_trader(dict_text['text'])

                if dict_text['forward_from']['id'] == 1660604371:
                    get_rick_trader(dict_text['text'])

            elif "forward_from_chat" in dict_text:

                if dict_text['forward_from_chat']['id'] == -1001397474181:
                    get_tigre_sinais(dict_text['text'])

                if dict_text['forward_from_chat']['id'] == -1001768846032:
                    get_extensao_vip(dict_text['text'])  # sala vip e gale 1

                if dict_text['forward_from_chat']['id'] == -1001687605555:
                    get_extensao_vip(dict_text['text'])  # sala vip e gale 1

                if dict_text['forward_from_chat']['id'] == -1001251628658:
                    get_sinais_gold(dict_text['text'])


            elif dict_text['chat']['id'] == 1682734976:
                get_padrão_avulso(dict_text['text'])

        except IndexError:
            print("Padrão de Texto Desconhecido...")
        except TypeError:
            print("Tipo de Texto Desconhecido...")
        except AttributeError:
            print("Erro de atributo...")

    try:
        # estado_bot = get_estado(conn)
        # if estado_bot == 0:
        #     set_estado(conn, 1)
        bot.infinity_polling()  # inicia o bot
    except TimeoutError:
        print("Erro ao se conectar com o SianisIQBot")


if __name__ == '__main__':
    liga_bot()
