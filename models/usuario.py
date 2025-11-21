class Usuario:
    def __init__(self, id, nome, email, senha_hash, empresa_id=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash
        self.empresa_id = empresa_id