from data.database_utils import load_data, save_data 
import sys 
from models.empresa import Empresa
from models.usuario import Usuario
import uuid

#Menu de Login
def fluxo_login():
    print("Bem-vindo ao Guardian")
    print("----------------------")
    print("[1] Cadastro de Empresa")
    print("[2] Login Da Empresa")
    print("[0] Sair")

    return int(input("Escolha uma opção: "))


def cadastrar_usuario():
    nome_fantasia = input("Nome Fantasia: ")
    razao_social = input("Razão Social: ")            
    cnpj = input("CNPJ da Empresa: ")

    empresa_id = str(uuid.uuid4())

    empresaLocal = Empresa(
        id=empresa_id,
        nome_fantasia=nome_fantasia,
        razao_social=razao_social,
        cnpj=cnpj
    )

    email = input("Email da empresa: ")
    senha = input("Senha: ")

    usuarioLocal = Usuario(
        id=str(uuid.uuid4()),
        email=email,
        senha=senha,
        empresa_id=empresa_id   # se existir no modelo
    )

    # SALVA COMO DICIONÁRIO
    empresaLocal.usuarios.append(usuarioLocal.to_dict())

    banco = load_data()
    if "empresas" not in banco:
        banco["empresas"] = []

    banco["empresas"].append(empresaLocal.to_dict())
    save_data(banco)

    print(f'Empresa cadastrada!\nID Cadastrado: {empresa_id}')

    
#Fluxo de login
def login_usuario():
    print("Login do Usuário")
    login_email = input("Email: ")
    login_senha = input("Senha: ")

    banco = load_data()
    for empresa in banco["empresas"]:
        for usuario in empresa["usuarios"]:
            if usuario["email"] == login_email and usuario["senha"] == login_senha:
                print(f'Login feito com sucesso! Bem-vindo(a), empresa: {empresa["nome_fantasia"]}')
                return True

    print("Email ou senha incorretos...")    
    return False

         
def mostrar_menu():
    print("\n--- 🛡 GUARDIAN 🛡 ---")
    print("  [1] Listar Clientes")
    print("  [2] Cadastrar Novo Cliente")
    print("  [0] Sair")
    return input("Escolha uma opção: ")

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
                                listar_clientes()
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
