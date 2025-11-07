from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.db import transaction
from empresas.models import Empresa

class CustomRegisterSerializer(RegisterSerializer):
    username = None

    nome_fantasia = serializers.CharField(max_length=100, required=True)
    razao_social = serializers.CharField(max_length=100, required=True)
    cnpj = serializers.CharField(max_length=14, required=True)

    @transaction.atomic
    def save(self, request):
        user = super().save(request)

        nome_fantasia = self.validated_data.get('nome_fantasia')
        razao_social = self.validated_data.get('razao_social')
        cnpj = self.validated_data.get('cnpj')

        empresa = Empresa.objects.create(
            nome_fantasia=nome_fantasia,
            razao_social=razao_social,
            cnpj=cnpj
        )

        user.empresa = empresa
        user.save()

        return user
    
    def validate_cnpj(self, value):
        if Empresa.objects.filter(cnpj=value).exists():
            raise serializers.ValidationError("uma empresa com este CNPJ já está cadastrada.")
        return value