from utils.crypto_utils import encrypt_data, decrypt_data

class Usuario:
    def __init__(self, id, email, senha, empresa_id=None):
        self.id = id
        self.email = decrypt_data(email)
        self.senha = senha
        self.empresa_id = empresa_id

    def to_dict(self):
        return {
            "id": self.id,
            "email": encrypt_data(self.email),
            "senha": self.senha
        }