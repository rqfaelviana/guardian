class Empresa:
    def __init__(self, id, nome_fantasia, razao_social, cnpj, usuarios=None, clientes=None):
        self.id = id
        self.nome_fantasia = nome_fantasia
        self.razao_social = razao_social
        self.cnpj = cnpj
        self.usuarios = usuarios or []
        self.clientes = clientes or []