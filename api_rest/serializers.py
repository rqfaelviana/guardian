from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.db import transaction
from .models import Empresa

# Este é o serializer customizado que informamos no settings.py
class CustomRegisterSerializer(RegisterSerializer):
    username = None  # <-- Esta linha
    # Adicionamos os campos do model 'Empresa' que queremos 
    # receber durante o cadastro do usuário.
    nome_fantasia = serializers.CharField(max_length=100, required=True)
    razao_social = serializers.CharField(max_length=100, required=True)
    cnpj = serializers.CharField(max_length=14, required=True)

    # Sobrescrevemos o método 'save' para lidar com os novos campos
    @transaction.atomic # Garante que ou tudo é salvo, ou nada é
    def save(self, request):
        
        # 1. Chama o método 'save' original do dj-rest-auth.
        #    Isso vai criar o 'Usuario' (user) com email, senha, etc.
        #    Os campos da empresa (nome_fantasia, etc.) serão ignorados
        #    pelo 'save' original, mas estarão em self.validated_data.
        user = super().save(request)

        # 2. Extraímos os dados da empresa do dicionário de dados validados
        nome_fantasia = self.validated_data.get('nome_fantasia')
        razao_social = self.validated_data.get('razao_social')
        cnpj = self.validated_data.get('cnpj')

        # 3. Criamos o objeto 'Empresa' no banco de dados
        #    (A validação de CNPJ duplicado abaixo vai impedir erros)
        empresa = Empresa.objects.create(
            nome_fantasia=nome_fantasia,
            razao_social=razao_social,
            cnpj=cnpj
        )

        # 4. Finalmente, associamos a 'Empresa' que acabamos de criar
        #    ao 'Usuario' que foi criado.
        user.empresa = empresa
        user.save()

        # 5. Retorna o usuário pronto
        return user

    # --- Validação (Boa Prática) ---

    def validate_cnpj(self, value):
        """
        Verifica se já existe uma empresa com este CNPJ.
        """
        if Empresa.objects.filter(cnpj=value).exists():
            # Se o CNPJ já existir, levantamos um erro de validação
            raise serializers.ValidationError("Uma empresa com este CNPJ já está cadastrada.")
        
        # Aqui você poderia adicionar mais lógicas, como verificar 
        # se o formato do CNPJ é válido (só números, 14 dígitos, etc.)
        
        return value