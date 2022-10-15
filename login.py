from pymongo import MongoClient


def get_login():
    """função que entrega os dados de login direto do banco de dados online"""
    url = "mongodb+srv://cosmolustosa123:Tocar123*@cluster-ob-financeiro.rugnw5v.mongodb.net/test"
    myclient = MongoClient(url)
    mydb = myclient["IQOption"]
    mycollection = mydb["dadosLogin"]
    dados = mycollection.find()
    return dados[0]['email'], dados[0]['senha'], dados[0]['url'], dados[0]['api_key']

if __name__=="__main__":
    print(get_login())