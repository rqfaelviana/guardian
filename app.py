from database_utils import ler_banco, salvar_banco 
import sys 

def listar_clientes():
    
    pass

def cadastrar_cliente():

    pass

def fluxo_de_login():

    pass

def mostrar_menu():
    print("\n--- 🛡️ GUARDIAN (Python Puro) 🛡️ ---")
    print("  [1] Listar Clientes")
    print("  [2] Cadastrar Novo Cliente")
    print("  [3] Fazer Login")

    print("  [0] Sair")
    return input("Escolha uma opção: ")

def main():
    while True: 
        escolha = mostrar_menu()
        
        match escolha:
            case '1':
                listar_clientes()
            
            case '2':
                cadastrar_cliente() 
            
            case '3':
                fluxo_de_login() 
            
            case '0':
                print("Programa encerrado.")
                sys.exit()
            
            case _: 
                print("Opção inválida. Tente novamente.")


if __name__ == '__main__':
    main()