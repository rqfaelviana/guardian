class Usuario:
    def __init__(self, id, email, senha, empresa_id=None):
        self.id = id
        self.email = email
        self.senha = senha
        self.empresa_id = empresa_id

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "senha": self.senha
        }