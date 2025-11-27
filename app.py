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

#Menu de Login
def fluxo_login():
    print("Bem-vindo ao Guardian")
    print("----------------------")
    print("[1] Cadastro de Empresa")
    print("[2] Login Da Empresa")
    print("[0] Sair")
    
    op = input("Escolha uma opção: ")
    if op.isdigit():
        return int(op)
    return -1
    #return int(input("Escolha uma opção: "))


def cadastrar_usuario():
    print("\n====================================")
    print("        CADASTRO DE EMPRESA")
    print("====================================\n")
    nome_fantasia = input("Nome Fantasia: ").strip().title()
    razao_social = input("Razão Social: ").strip().title()  

    #validação do cnpj
    while True:          
        cnpj = input("CNPJ da Empresa: ").strip()

        if len(cnpj) == 14 and cnpj.isdigit():
            break
        else:
            print("\n[Erro] CNPJ inválido. Digite exatamente 14 números.\n")
    

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

        if "@" not in email and "." not in email:
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

def listar_clientes(empresa):
    banco_todos_clientes = load_data_client() 
    lista_clientes = banco_todos_clientes.get("clientes", [])



    for cliente in lista_clientes:
        
        if cliente['empresa_id'] == empresa['id']:
            print(f"Nome: {cliente['nome_completo']}")
            print(f"CPF: {cliente['cpf']}")
            print(f"Email: {cliente['email']}")
            print("\n")
            
# Cadastro de Clientes
def cadastrar_cliente(empresa):
    print("\n===== CADASTRAR NOVO CLIENTE =====")

    # --- 1. VALIDAÇÃO DO NOME (Apenas letras) ---
    nome_validado = ""
    while True:
        entrada_nome = input("Nome completo: ").strip()
        # O replace tira os espaços só para testar se o resto é letra
        # Ex: "Joao Silva" vira "JoaoSilva" -> isalpha() diz True
        if len(entrada_nome) > 0 and entrada_nome.replace(" ", "").isalpha():
            nome_validado = entrada_nome
            break
        else:
            print("❌ Erro: O nome deve conter apenas letras (sem números).")

    # --- 2. VALIDAÇÃO DO CPF (11 números) ---
    cpf_validado = "" 
    while True:
        entrada_cpf = input("CPF (apenas números): ").strip()

        if len(entrada_cpf) == 11 and entrada_cpf.isdigit():
            cpf_validado = entrada_cpf
            break 
        else:
            print("❌ Erro: O CPF precisa ter exatamente 11 números.")

    # --- 3. VALIDAÇÃO DA DATA (6 números - DDMMAA) ---
    data_validada = ""
    while True:
        entrada_data = input("Data de nascimento (DDMMAA - 6 dígitos): ").strip()

        if len(entrada_data) == 6 and entrada_data.isdigit():
            data_validada = entrada_data
            break
        else:
            print("❌ Erro: A data deve ter apenas 6 números (Ex: 251290).")

    # --- CRIAÇÃO DO DICIONÁRIO ---
    cliente = {
        "id": str(uuid.uuid4()),
        "empresa_id": empresa["id"],

        "nome_completo": nome_validado,   # <--- Nome validado
        "cpf": cpf_validado,              # <--- CPF validado
        "data_nascimento": data_validada, # <--- Data validada
        
        # Os outros campos continuam com input normal
        "rg": input("RG: "),
        "genero": input("Gênero: "),
        "nacionalidade": input("Nacionalidade: "),
        "estado_civil": input("Estado civil: "),
        "endereco": input("Endereço (logradouro): "),
        "numero": input("Número: "),
        "complemento": input("Complemento: "),
        "bairro": input("Bairro: "),
        "cidade": input("Cidade: "),
        "estado": input("Estado: "),
        "cep": input("CEP: "),
        "pais": input("País: "),
        "email": input("E-mail: "),
        "telefone_celular": input("Telefone celular: "),
        "telefone_fixo": input("Telefone fixo: "),
        "whatsapp": input("WhatsApp: "),
        "redes_sociais": input("Redes sociais: "),
        "profissao": input("Profissão: ")
    }

    banco = load_data_client()
    if "clientes" not in banco:
        banco["clientes"] = []

    banco["clientes"].append(cliente)
    save_data_client(banco)

    print("\n------------------------------------")
    print("✔ Cliente cadastrado com sucesso!")
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
