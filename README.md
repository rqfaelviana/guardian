# 🛡️ Guardian - Sistema de Gestão Segura de Clientes

**Guardian** é um sistema de gerenciamento de clientes com foco em segurança de dados, desenvolvido em Python. O projeto implementa criptografia de ponta para proteger informações sensíveis de empresas e seus clientes.

## 📋 Sobre o Projeto

O Guardian é uma aplicação de linha de comando (CLI) que permite empresas cadastrarem-se no sistema e gerenciarem seus clientes de forma segura. Todos os dados sensíveis são criptografados antes de serem armazenados, garantindo a privacidade e integridade das informações.

### ✨ Funcionalidades Principais

- **Cadastro de Empresas**: Registro de empresas com validação de CNPJ e email
- **Sistema de Login**: Autenticação segura com senhas criptografadas
- **Gestão de Clientes**: Cadastro e listagem de clientes por empresa
- **Criptografia de Dados**: Proteção de dados sensíveis com criptografia reversível
- **Hash de Senhas**: Proteção de senhas com bcrypt (não reversível)

## 🔒 Segurança

O projeto implementa duas camadas de segurança:

### 1. Criptografia Fernet (Reversível)
- **Biblioteca**: `cryptography` (Fernet)
- **Uso**: Dados de empresas e clientes
- **Campos criptografados**:
  - Nome fantasia, razão social, CNPJ (empresas)
  - Nome, CPF, RG, email, telefone, endereço (clientes)
- **Chave**: Armazenada em `secret.key` (gerada automaticamente)

### 2. Hash Bcrypt (Irreversível)
- **Biblioteca**: `bcrypt`
- **Uso**: Senhas de usuários
- **Vantagem**: Impossível reverter o hash para obter a senha original

> [!IMPORTANT]
> O arquivo `secret.key` contém a chave de criptografia. **NUNCA** compartilhe ou versione este arquivo. Sem ele, os dados criptografados não poderão ser descriptografados.

## 📁 Estrutura do Projeto

```
projeto1/
├── app.py                  # Aplicação principal
├── requirements.txt        # Dependências do projeto
├── secret.key             # Chave de criptografia (NÃO VERSIONAR)
├── models/                # Modelos de dados
│   ├── cliente.py        # Classe Cliente
│   ├── empresa.py        # Classe Empresa
│   └── usuario.py        # Classe Usuario
├── utils/                 # Utilitários
│   └── crypto_utils.py   # Funções de criptografia
└── data/                  # Armazenamento de dados
    └── database_utils.py # Funções de banco de dados
```

## 🚀 Como Executar

### Pré-requisitos

- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/rqfaelviana/guardian.git
cd projeto1
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o programa:
```bash
python app.py
```

## 📦 Dependências

```
tabulate       # Formatação de tabelas no terminal
bcrypt         # Hash de senhas
cryptography   # Criptografia de dados (Fernet)
```

## 💻 Uso

### Menu Principal

1. **Cadastro de Empresa**: Registre uma nova empresa no sistema
2. **Login da Empresa**: Acesse o painel de gestão
3. **Sair**: Encerre o programa

### Após o Login

1. **Listar Clientes**: Visualize todos os clientes da empresa
2. **Cadastrar Novo Cliente**: Adicione um novo cliente
3. **Sair**: Retorne ao menu principal

### Exemplo de Fluxo

```
1. Cadastre uma empresa com CNPJ, nome fantasia, razão social, email e senha
2. Faça login com o email e senha cadastrados
3. Cadastre clientes com informações pessoais e de endereço
4. Liste todos os clientes da empresa (dados descriptografados automaticamente)
```

## 🔐 Validações Implementadas

- **CNPJ**: 14 dígitos numéricos, único no sistema
- **Email**: Formato válido (contém @ e .), único no sistema
- **Senha**: Criptografada com bcrypt antes do armazenamento
- **Login**: Verificação de email e senha com suporte a senhas legadas

## 📊 Armazenamento de Dados

Os dados são armazenados em arquivos JSON no diretório `data/`:
- `empresas.json`: Empresas e usuários (criptografados)
- `clientes.json`: Clientes (criptografados)

> [!WARNING]
> Os arquivos JSON contêm dados criptografados. Sem a chave `secret.key`, os dados não podem ser lidos.

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+**: Linguagem principal
- **Bcrypt**: Hash de senhas
- **Cryptography (Fernet)**: Criptografia simétrica
- **Tabulate**: Formatação de tabelas
- **UUID**: Geração de IDs únicos
- **JSON**: Armazenamento de dados

## 📝 Notas de Desenvolvimento

- O sistema usa `match-case` (Python 3.10+) para menus
- Validações de entrada são feitas em loops `while True`
- Dados são criptografados na camada de modelo (`to_dict()`)
- Dados são descriptografados na leitura (construtor das classes)

