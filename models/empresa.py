from utils.crypto_utils import encrypt_data, decrypt_data

class Empresa:
    def __init__(self, id, nome_fantasia, razao_social, cnpj, usuarios=None, clientes=None):
        self.id = id
        self.nome_fantasia = decrypt_data(nome_fantasia)
        self.razao_social = decrypt_data(razao_social)
        self.cnpj = decrypt_data(cnpj)
        self.usuarios = usuarios or []
        self.clientes = clientes or []

    def to_dict(self):
        return {
            "id": self.id,
            "nome_fantasia": encrypt_data(self.nome_fantasia),
            "razao_social": encrypt_data(self.razao_social),
            "cnpj": encrypt_data(self.cnpj),
            "usuarios": [u if isinstance(u, dict) else u.to_dict() for u in self.usuarios],
        }