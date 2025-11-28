from utils.crypto_utils import encrypt_data, decrypt_data

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
        self.nome_completo = decrypt_data(nome_completo)
        self.cpf = decrypt_data(cpf)
        self.rg = decrypt_data(rg)
        self.data_nascimento = decrypt_data(data_nascimento)
        self.genero = decrypt_data(genero)
        self.nacionalidade = decrypt_data(nacionalidade)
        self.estado_civil = decrypt_data(estado_civil)
        self.email = decrypt_data(email)
        self.telefone = decrypt_data(telefone)
        self.numero_residencial = decrypt_data(numero_residencial)
        self.logradouro = decrypt_data(logradouro)
        self.bairro = decrypt_data(bairro)
        self.cidade = decrypt_data(cidade)
        self.estado = decrypt_data(estado)
        self.cep = decrypt_data(cep)

    #converte os dados do cliente para dicionário para salvar no JSON
    def to_dict(self):
        return {
            "nome_completo": encrypt_data(self.nome_completo),
            "cpf": encrypt_data(self.cpf),
            "rg": encrypt_data(self.rg),
            "data_nascimento": encrypt_data(self.data_nascimento),
            "genero": encrypt_data(self.genero),
            "nacionalidade": encrypt_data(self.nacionalidade),
            "estado_civil": encrypt_data(self.estado_civil),
            "email": encrypt_data(self.email),
            "telefone": encrypt_data(self.telefone),
            "numero_residencial": encrypt_data(self.numero_residencial),
            "logradouro": encrypt_data(self.logradouro),
            "bairro": encrypt_data(self.bairro),
            "cidade": encrypt_data(self.cidade),
            "estado": encrypt_data(self.estado),
            "cep": encrypt_data(self.cep),
            "empresa_id": getattr(self, 'empresa_id', None) # Garante que empresa_id seja salvo se existir
        }
