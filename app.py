from data.database_utils import load_data_user, save_data_user, save_data_client, load_data_client
import sys 
from models.empresa import Empresa
from models.usuario import Usuario
from models.cliente import Cliente
import uuid
from tabulate import tabulate
import bcrypt
from utils.crypto_utils import decrypt_data
from datetime import datetime

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

def validar_cpf(cpf):
    cpf = cpf.strip().replace(".", "").replace("-", "")

    #cpf deve ter exatamente 11 dígitos
    if len(cpf) != 11 or not cpf.isdigit():
        return False

    # nega cpf's com todos os números iguais
    if cpf == cpf[0] * 11:
        return False

    # Cálculo do 1º dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = (soma * 10) % 11
    digito1 = 0 if digito1 == 10 else digito1

    # Cálculo do 2º dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma * 10) % 11
    digito2 = 0 if digito2 == 10 else digito2

    return cpf[-2:] == f"{digito1}{digito2}"

def validar_data_nascimento(data):
    try:
        datetime.strptime(data, "%d/%m/%Y")
        return True
    except ValueError:
        return False

#função pra formatar o cpf
def formatar_cpf(cpf):
    cpf = cpf.strip().replace(".", "").replace("-", "")
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

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

        if "@" not in email or "." not in email or email.split("@")[0] == "":
            print("\n[Erro] Email inválido. Tente novamente.\n")
            continue
        
        banco = load_data_user()

        if email_existe(email, banco):
            print("\n[Erro] Email já cadastrado. Utilize outro.\n")
            continue
        
        break

    senha = input("Senha: ")

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

    banco = load_data_user()

    # verifica se há empresas cadastradas
    if "empresas" not in banco or len(banco["empresas"]) == 0:
        print("\n[Erro] Nenhuma empresa cadastrada no sistema.\n")
        return False

    # 1) Procurar o email primeiro
    usuario_encontrado = None
    empresa_logada = None

    for empresa in banco["empresas"]:
        for usuario in empresa["usuarios"]:
            email_banco = decrypt_data(usuario["email"])
            if email_banco == login_email:
                usuario_encontrado = usuario
                empresa_logada = empresa
                break
        if usuario_encontrado:
            break

    if not usuario_encontrado:
        print("\n[Erro] Email não encontrado.\n")
        return False

    # 2) loop até acertar a senha
    while True:
        login_senha = input("Senha: ")

        senha_armazenada = usuario_encontrado["senha"]
        senha_valida = False

        try:
            if bcrypt.checkpw(login_senha.encode('utf-8'), senha_armazenada.encode('utf-8')):
                senha_valida = True
        except ValueError:
            if senha_armazenada == login_senha:
                senha_valida = True

        if senha_valida:
            nome_fantasia = decrypt_data(empresa_logada["nome_fantasia"])
            print("\n------------------------------------")
            print(f'Login realizado com êxito! Bem-vindo(a), empresa: {nome_fantasia}')
            print("\n------------------------------------")
            return empresa_logada
        else:
            print("\n[Erro] Senha incorreta. Tente novamente!\n")


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
    cabecalhos = ["Nome Completo", "Gênero", "Data de nascimento", "CPF"] 
    
    for cliente in lista_clientes:
        
        if cliente['empresa_id'] == empresa['id']:
            
            dados_tabela.append([
                decrypt_data(cliente['nome_completo']),
                decrypt_data(cliente['genero']),
                decrypt_data(cliente['data_nascimento']),
                decrypt_data(cliente['cpf'])
            ])

    nome_fantasia_empresa = decrypt_data(empresa.get('nome_fantasia', 'Desconhecida'))
    print(f"\n--- CLIENTES DA EMPRESA: {nome_fantasia_empresa} ---")
    
    if dados_tabela:
        print(tabulate(dados_tabela, headers=cabecalhos, tablefmt="fancy_grid"))
    else:
        print("Nenhum cliente encontrado para esta empresa.")
    print("-" * 75)

def cadastrar_cliente(empresa):
    print("\n====================================")
    print("        CADASTRO DE CLIENTE")
    print("====================================\n")

    #validação do nome completo
    while True:
        nome_completo = input("Nome Completo: ").strip().title()

        if len(nome_completo) < 3:
            print("\n[Erro] Nome inválido.\n")
            continue

        break
    
    #validação do CPF
    while True:
        cpf = input("CPF: ").strip()

        if not validar_cpf(cpf):
            print("\n[Erro] CPF inválido. Digite um CPF válido.\n")
            continue

        cpf = formatar_cpf(cpf)
    
        break
    
    #validação do RG
    while True:
        rg = input("RG: ").strip()

        if len(rg) < 5:
            print("\n[Erro] RG inválido.\n")
            continue

        break

    #validação da data de nascimento
    while True:
        data_nascimento = input("Data de Nascimento (DD/MM/AAAA): ").strip()
        
        if not validar_data_nascimento(data_nascimento):
            print("\n[Erro] Data inválida. Use o formato DD/MM/AAAA.\nExemplo válido: 25/08/2004\n")
            continue
        
        break

    #validação de gênero
    while True:
        print("\nGênero:")
        print("[1] Masculino")
        print("[2] Feminino")
        print("[3] Não informado")
        opcao_genero = input("Escolha uma opção: ")

        if opcao_genero == "1":
            genero = "Masculino"
            break
        elif opcao_genero == "2":
            genero = "Feminino"
            break
        elif opcao_genero == "3":
            genero = "Não informado"
            break
        else:
            print("\n[Erro] Opção inválida.\n")

    nacionalidade = input("Nacionalidade: ").strip()

    #validação do estado civil
    while True:
        print("\nEstado Civil:")
        print("[1] Solteiro(a)")
        print("[2] Casado(a)")
        print("[3] Divorciado(a)")
        print("[4] Viúvo(a)")
        opcao_estado = input("Escolha uma opção: ")

        if opcao_estado == "1":
            estado_civil = "Solteiro(a)"
            break
        elif opcao_estado == "2":
            estado_civil = "Casado(a)"
            break
        elif opcao_estado == "3":
            estado_civil = "Divorciado(a)"
            break
        elif opcao_estado == "4":
            estado_civil = "Viúvo(a)"
            break
        else:
            print("\n[Erro] Opção inválida.\n")
    
    #validação do email do cliente
    while True:
        email = input("Email: ").strip().lower()

        if "@" not in email or "." not in email or email.split("@")[0] == "":
            print("\n[Erro] Email inválido. Tente novamente.\n")
            continue
        break
    
    #validação do telefone
    while True:
        telefone = input("Telefone: ").strip()

        if not telefone.isdigit() or len(telefone) < 10:
            print("\n[Erro] Telefone inválido.\n")
            continue

        break
    
    print("\n--- Endereço ---")
    #validação do CEP
    while True:
        cep = input("CEP: ").strip()

        if not cep.isdigit() or len(cep) != 8:
            print("\n[Erro] CEP inválido. Digite 8 números.\n")
            continue

        break

    #validação do logradouro
    while True:
        logradouro = input("Logradouro: ").strip()
        if len(logradouro) < 3:
            print("\n[Erro] Logradouro inválido.\n")   
            continue
        break

    #validação do numero residencial
    while True:
        numero_residencial = input("Número: ").strip().lower()
        if not numero_residencial.isdigit() and numero_residencial != "s/n":
            print("\n[Erro] Número inválido.\n")
            continue
        break

    #validação do bairro
    while True:
        bairro = input("Bairro: ").strip()
        if len(bairro) < 3:
            print("\n[Erro] Bairro inválido.\n")
            continue
        break

    #validação da cidade
    while True:
        cidade = input("Cidade: ").strip()
        if len(cidade) < 3:
            print("\n[Erro] Cidade inválida.\n")
            continue
        break
    
    #validação do estado
    estados_validos = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", 
                       "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS",
                       "RO", "RR", "SC", "SP", "SE", "TO"]
    while True:
        estado = input("Estado (UF): ").strip().upper()
        if estado not in estados_validos:
            print("\n[Erro] Estado inválido.\n")
            continue
        break

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
                print("Programa encerrado.")
                break
            case _:
                print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
