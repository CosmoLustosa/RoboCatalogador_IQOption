from bot import liga_bot
from connect import get_connection, set_estado, get_estado
from flask import Flask
from flask_restful import Resource, Api
from threading import Thread


app = Flask(__name__)
api = Api(app)

# class Bot(Resource):
#     def get(self):
#         conn = get_connection()
#         print('Conexao: ', conn)
#         estado = get_estado(conn)
#         print('Estado: ', estado)
#         if int(estado) == 0:
#             set_estado(conn, 1)
#             liga_bot()
#             return json.loads({'Bot': 'Ligado'})
#         else:
#             return {'Status Bot': 'Bot já ligado'.encode('utf-8')}

# class Ordem(Resource):
#     def get(self):
#         return executa_ordens()
#
#
# # adiciona as rotas
#
# api.add_resource(Ordem, '/ordens')




@app.route('/bot')
def ligaBot():
    conn = get_connection()
    print('Conexao: ', conn)
    estado = get_estado(conn)
    print('Estado: ', estado)


    if int(estado) == 0:
        t = Thread(target=liga_bot)
        t.start()
        set_estado(conn, 1)

        return 'Ligando Bot'
    else:
        return 'O Bot já está ligado...'
#




# @app.route('/executa_ordens')
# def executa_ordem():
#     executa_ordens()
#     return None
#
#
#
# @app.route('/')
# def index():
#     return 'Index'







if __name__ == '__main__':
    app.run(debug=True)

