import json
import os

#endereço do nosso banco de dados
DB_PATH = 'data/database.json'


def init_data():
    #garante que a pasta 'data' exista
    os.makedirs("data", exist_ok=True)

    #garante que o arquivo 'database.json' exista
    if not os.path.exists(DB_PATH):
        banco = {
            "empresas": [] #empresa tem os usuários responsáveis + clientes
        }

        with open (DB_PATH, "w", encoding="utf-8") as f:
            json.dump(banco, f, indent=4, ensure_ascii=False)

def load_data():
    #lê o database.json e retorna um dicionário
    #sempre chaam o init_data() pra que garantir que o arquivo existe
    init_data()

    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
        
    except json.JSONDecodeError:
        print("⚠️Warning: O banco de dados está corrompido. Ele será recriado.")

        banco = {"empreas": []}
        save_data(banco)
        return banco

def save_data(banco):
    """recebe um dicionário 'banco' atualizado e sobrescreve o arquivo JSON 
    com esses dados


    essa função nao mexe nos dados, nao adiciona e nem altera nada.
    ela salva o estado atual do banco no arquivo.
    evita bugs
    """
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(banco, f, indent=4, ensure_ascii=False)