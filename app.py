from data.database_utils import load_data_user, save_data_user, save_data_client, load_data_client
import sys 
from models.empresa import Empresa
from models.usuario import Usuario
import uuid

#função pra verificar se o email ja existe
def email_existe(email, banco):
    for empresa in banco.get("empresas", []):
        for usuario in empresa.get("usuarios", []):
            if usuario["email"] == email:
                return True
    return False

def cnpj_existe(cnpj, banco):
    for empresa in banco.get("empresas", []):
        if empresa["cnpj"] == cnpj:
            return True
        return False

#Menu de Login
def fluxo_login():
    print("Bem-vindo ao Guardian")
    print("----------------------")
    print("[1] Cadastro de Empresa")
    print("[2] Login Da Empresa")
    print("[0] Sair")

    return int(input("Escolha uma opção: "))


def cadastrar_usuario():
    print("\n====================================")
    print("        CADASTRO DE EMPRESA")
    print("====================================\n")
    nome_fantasia = input("Nome Fantasia: ").strip().title()
    razao_social = input("Razão Social: ").strip().title()  

    #validação do cnpj
    while True:          
        cnpj = input("CNPJ da Empresa: ").strip()

        if len(cnpj) != 14 or not cnpj.isdigit():
            print("\n[Erro] CNPJ inválido. Digite exatamente 14 números.\n")
            continue
        banco = load_data_user()
        
        if cnpj_existe(cnpj, banco):
            print("\n[Erro] Já existe uma empresa cadastrada com este CNPJ.\n")
            continue
        break

    empresa_id = str(uuid.uuid4())

    empresaLocal = Empresa(
        id=empresa_id,
        nome_fantasia=nome_fantasia,
        razao_social=razao_social,
        cnpj=cnpj
    )

    #validação do email
    while True:
        email = input("Email da empresa: ").strip().lower()

        if "@" not in email or "." not in email:
            print("[Erro] Email inválido. Tente novamente.")
            continue

        banco = load_data_user()

        if email_existe(email, banco):
            print("[Erro] Email já cadastrado. Utilize outro.")
            continue
        
        break

    senha = input("\nSenha: ")

    usuarioLocal = Usuario(
        id=str(uuid.uuid4()),
        email=email,
        senha=senha,
        empresa_id=empresa_id   # se existir no modelo
    )

    # SALVA COMO DICIONÁRIO
    empresaLocal.usuarios.append(usuarioLocal.to_dict())

    banco = load_data_user()
    if "empresas" not in banco:
        banco["empresas"] = []

    banco["empresas"].append(empresaLocal.to_dict())
    save_data_user(banco)
    print("\n------------------------------------")
    print(f'Empresa cadastrada!\nID Cadastrado: {empresa_id}')
    print("------------------------------------\n")

    
#Fluxo de login
def login_usuario():
    print("\n====================================")
    print("              LOGIN")
    print("====================================\n")

    login_email = input("Email: ").strip().lower()
    login_senha = input("Senha: ")

    banco = load_data_user()

    #verifica se tem empressas cadastradas
    if "empresas" not in banco or len(banco["empresas"]) == 0:
        print("\n[Erro] Nenhuma empresa cadastrada no sistema.\n")
        return False
    
    for empresa_logada in banco["empresas"]:
        for usuario in empresa_logada["usuarios"]:
            if usuario["email"] == login_email and usuario["senha"] == login_senha:
                print("\n------------------------------------")
                print(f'Login realizado com êxito! Bem-vindo(a), empresa: {empresa_logada["nome_fantasia"]}')
                print("\n------------------------------------")
                return empresa_logada

    print("\n[Erro] Email ou senha incorretos.\n")  
    return False

         
def mostrar_menu():
    print("\n--- 🛡 GUARDIAN 🛡 ---")
    print("  [1] Listar Clientes")
    print("  [2] Cadastrar Novo Cliente")
    print("  [0] Sair")
    return input("Escolha uma opção: ")

from tabulate import tabulate

def listar_clientes(empresa):
    banco_todos_clientes = load_data_client() 
    lista_clientes = banco_todos_clientes.get("clientes", [])


    dados_tabela = []
    cabecalhos = ["Nome Completo", "CPF", "Email"] 
    
    for cliente in lista_clientes:
        
        if cliente['empresa_id'] == empresa['id']:
            
            dados_tabela.append([
                cliente['nome_completo'],
                cliente['cpf'],
                cliente['email']
            ])

    print(f"\n--- CLIENTES DA EMPRESA: {empresa.get('nome', 'Desconhecida')} ---")
    
    if dados_tabela:
        print(tabulate(dados_tabela, headers=cabecalhos, tablefmt="fancy_grid"))
    else:
        print("Nenhum cliente encontrado para esta empresa.")
    print("-" * 75)
            

#Menu principal
def main():
    while True:
        opcao = fluxo_login()
        match opcao:
            case 1:
                cadastrar_usuario()
            case 2:
                logado = login_usuario()
                if logado:
                    while True:
                        escolha = mostrar_menu()
                        match escolha:
                            case '1':
                                listar_clientes(logado)
                            case '2':
                                cadastrar_cliente()
                            case '0':
                                print("Programa encerrado.")
                                sys.exit()
                            case _:
                                print("Opção inválida. Tente novamente.")
            case 0:
                print("Saindo do programa!")
                break
            case _:
                print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
