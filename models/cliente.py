class Cliente:
    def __init__(
        self,
        nome_completo,
        cpf,
        rg,
        data_nascimento,
        genero, 
        nacionalidade, 
        estado_civil,
        email, 
        telefone,
        numero_residencial, 
        logradouro,
        bairro, 
        cidade, 
        estado, 
        cep
    ):
        self.nome_completo = nome_completo
        self.cpf = cpf
        self.rg = rg
        self.data_nascimento = data_nascimento
        self.genero = genero
        self.nacionalidade = nacionalidade
        self.estado_civil = estado_civil
        self.email = email
        self.telefone = telefone
        self.numero_residencial = numero_residencial
        self.logradouro = logradouro
        self.bairro = bairro
        self.cidade = cidade 
        self.estado = estado 
        self.cep = cep

        #converte os dados do cliente para dicionário para salvar no JSON
    def to_dict(self):
        return self.__dict__
