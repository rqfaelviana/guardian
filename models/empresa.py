class Empresa:
    def __init__(self, id, nome_fantasia, razao_social, cnpj, usuarios=None, clientes=None):
        self.id = id
        self.nome_fantasia = nome_fantasia
        self.razao_social = razao_social
        self.cnpj = cnpj
        self.usuarios = usuarios or []
        self.clientes = clientes or []

    def to_dict(self):
        return {
            "id": self.id,
            "nome_fantasia": self.nome_fantasia,
            "razao_social": self.razao_social,
            "cnpj": self.cnpj,
            "usuarios": [u if isinstance(u, dict) else u.to_dict() for u in self.usuarios],
        }