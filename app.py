from data.database_utils import load_data_user, save_data_user, save_data_client, load_data_client
import sys 
from models.empresa import Empresa
from models.usuario import Usuario
from models.cliente import Cliente
import uuid
from tabulate import tabulate
import bcrypt
from utils.crypto_utils import decrypt_data

#função pra verificar se o email ja existe
def email_existe(email, banco):
    for empresa in banco.get("empresas", []):
        for usuario in empresa.get("usuarios", []):
            # Descriptografa o email do banco para comparar
            email_banco = decrypt_data(usuario["email"])
            if email_banco == email:
                return True
    return False

def cnpj_existe(cnpj, banco):
    for empresa in banco.get("empresas", []):
        # Descriptografa o CNPJ do banco para comparar
        cnpj_banco = decrypt_data(empresa["cnpj"])
        if cnpj_banco == cnpj:
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

    # Criptografar a senha antes de salvar
    salt = bcrypt.gensalt()
    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), salt)

    usuarioLocal = Usuario(
        id=str(uuid.uuid4()),
        email=email,
        senha=senha_hash.decode('utf-8'), # Salva como string
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
            # Verifica se a senha armazenada é hash (bcrypt) ou texto plano (legado)
            senha_armazenada = usuario["senha"]
            senha_valida = False

            try:
                # Tenta verificar como hash bcrypt
                if bcrypt.checkpw(login_senha.encode('utf-8'), senha_armazenada.encode('utf-8')):
                    senha_valida = True
            except ValueError:
                # Se der erro (ex: salt inválido), assume que é texto plano (legado)
                if senha_armazenada == login_senha:
                    senha_valida = True
            
            # Descriptografa o email para comparar no login
            email_banco = decrypt_data(usuario["email"])
            
            if email_banco == login_email and senha_valida:
                # Descriptografa o nome fantasia para exibir
                nome_fantasia = decrypt_data(empresa_logada["nome_fantasia"])
                print("\n------------------------------------")
                print(f'Login realizado com êxito! Bem-vindo(a), empresa: {nome_fantasia}')
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

def listar_clientes(empresa):
    banco_todos_clientes = load_data_client() 
    lista_clientes = banco_todos_clientes.get("clientes", [])


    dados_tabela = []
    cabecalhos = ["Nome Completo", "CPF", "Email"] 
    
    for cliente in lista_clientes:
        
        if cliente['empresa_id'] == empresa['id']:
            
            dados_tabela.append([
                decrypt_data(cliente['nome_completo']),
                decrypt_data(cliente['cpf']),
                decrypt_data(cliente['email'])
            ])

    nome_fantasia_empresa = decrypt_data(empresa.get('nome_fantasia', 'Desconhecida'))
    print(f"\n--- CLIENTES DA EMPRESA: {nome_fantasia_empresa} ---")
    
    if dados_tabela:
        print(tabulate(dados_tabela, headers=cabecalhos, tablefmt="grid"))
    else:
        print("Nenhum cliente encontrado para esta empresa.")
    print("-" * 75)

def cadastrar_cliente(empresa):
    print("\n====================================")
    print("        CADASTRO DE CLIENTE")
    print("====================================\n")

    nome_completo = input("Nome Completo: ").strip().title()
    cpf = input("CPF: ").strip()
    rg = input("RG: ").strip()
    data_nascimento = input("Data de Nascimento (DD/MM/AAAA): ").strip()
    genero = input("Gênero: ").strip()
    nacionalidade = input("Nacionalidade: ").strip()
    estado_civil = input("Estado Civil: ").strip()
    email = input("Email: ").strip().lower()
    telefone = input("Telefone: ").strip()
    
    print("\n--- Endereço ---")
    cep = input("CEP: ").strip()
    logradouro = input("Logradouro: ").strip()
    numero_residencial = input("Número: ").strip()
    bairro = input("Bairro: ").strip()
    cidade = input("Cidade: ").strip()
    estado = input("Estado: ").strip()

    novo_cliente = Cliente(
        nome_completo=nome_completo,
        cpf=cpf,
        rg=rg,
        data_nascimento=data_nascimento,
        genero=genero,
        nacionalidade=nacionalidade,
        estado_civil=estado_civil,
        email=email,
        telefone=telefone,
        numero_residencial=numero_residencial,
        logradouro=logradouro,
        bairro=bairro,
        cidade=cidade,
        estado=estado,
        cep=cep
    )
    
    # Associa o cliente à empresa logada
    novo_cliente.empresa_id = empresa['id']

    banco = load_data_client()
    if "clientes" not in banco:
        banco["clientes"] = []

    banco["clientes"].append(novo_cliente.to_dict())
    save_data_client(banco)

    print("\n------------------------------------")
    print("Cliente cadastrado com sucesso!")
    print("------------------------------------\n")

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
                                cadastrar_cliente(logado)
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
