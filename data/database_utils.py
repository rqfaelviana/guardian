import json
import os

#endereço do nosso banco de dados
DB_USER_PATH = 'data/database_user.json'
DB_CLIENT_PATH = 'data/database_client.json'


def init_data_user():
    #garante que a pasta 'data' exista
    os.makedirs("data", exist_ok=True)

    #garante que o arquivo 'database.json' exista
    if not os.path.exists(DB_USER_PATH):
        banco = {
            "empresas": [] #empresa tem os usuários responsáveis + clientes
        }

        with open (DB_USER_PATH, "w", encoding="utf-8") as f:
            json.dump(banco, f, indent=4, ensure_ascii=False)

def init_data_client():
    #garante que a pasta 'data' exista
    os.makedirs("data", exist_ok=True)

    #garante que o arquivo 'database.json' exista
    if not os.path.exists(DB_CLIENT_PATH):
        banco = {
            "clientes": [] #empresa tem os usuários responsáveis + clientes
        }

        with open (DB_CLIENT_PATH, "w", encoding="utf-8") as f:
            json.dump(banco, f, indent=4, ensure_ascii=False)

def load_data_user():
    #lê o database.json e retorna um dicionário
    #sempre chaam o init_data() pra que garantir que o arquivo existe
    init_data_user()

    try:
        with open(DB_USER_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
        
    except json.JSONDecodeError:
        print("⚠️Warning: O banco de dados está corrompido. Ele será recriado.")

        banco = {"empresas": []}
        save_data_user(banco)
        return banco

def load_data_client():
        #lê o database.json e retorna um dicionário
    #sempre chaam o init_data() pra que garantir que o arquivo existe
    init_data_client()

    try:
        with open(DB_CLIENT_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
        
    except json.JSONDecodeError:
        print("⚠️Warning: O banco de dados está corrompido. Ele será recriado.")

        banco = {"clientes": []}
        save_data_client(banco)
        return banco
    
def save_data_user(banco):
    """recebe um dicionário 'banco' atualizado e sobrescreve o arquivo JSON 
    com esses dados


    essa função nao mexe nos dados, nao adiciona e nem altera nada.
    ela salva o estado atual do banco no arquivo.
    evita bugs
    """
    with open(DB_USER_PATH, "w", encoding="utf-8") as f:
        json.dump(banco, f, indent=4, ensure_ascii=False)

def save_data_client(banco):
    """recebe um dicionário 'banco' atualizado e sobrescreve o arquivo JSON 
    com esses dados


    essa função nao mexe nos dados, nao adiciona e nem altera nada.
    ela salva o estado atual do banco no arquivo.
    evita bugs
    """
    with open(DB_CLIENT_PATH, "w", encoding="utf-8") as f:
        json.dump(banco, f, indent=4, ensure_ascii=False)
