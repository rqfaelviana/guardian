from cryptography.fernet import Fernet
import os

KEY_FILE = 'secret.key'

def load_key():
    """Carrega a chave do arquivo secret.key. Se não existir, cria uma nova."""
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
    else:
        with open(KEY_FILE, "rb") as key_file:
            key = key_file.read()
    return key

# Carrega a chave uma vez
key = load_key()
cipher_suite = Fernet(key)

def encrypt_data(data):
    """Criptografa uma string."""
    if not data:
        return data
    if isinstance(data, str):
        return cipher_suite.encrypt(data.encode()).decode()
    return data

def decrypt_data(data):
    """Descriptografa uma string."""
    if not data:
        return data
    try:
        if isinstance(data, str):
            return cipher_suite.decrypt(data.encode()).decode()
    except Exception:
        # Se falhar (ex: dado não criptografado), retorna o original
        return data
    return data
