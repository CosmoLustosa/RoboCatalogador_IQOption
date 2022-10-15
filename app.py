from bot import liga_bot
from datetime import datetime
from flask import Flask
from flask_restful import Resource, Api
from tools import executa_ordens


app = Flask(__name__)
api = Api(app)

class Bot(Resource):
    def get(self):
        return liga_bot()

class Ordem(Resource):
    def get(self):
        return executa_ordens()


# adiciona as rotas
api.add_resource(Bot, '/bot')
api.add_resource(Ordem, '/ordens')




# @app.route('/liga_bot')
# def ligaBot():
#     print (f'Bot Ligado...{datetime.now()}')
#     liga_bot()
#     return None
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

