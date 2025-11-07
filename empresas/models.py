from django.db import models

# Create your models here.
class Empresa(models.Model):
    nome_fantasia = models.CharField(max_length=100)
    razao_social = models.CharField(max_length=100)

    cnpj = models.CharField(max_length=14, unique=True)

    def __str__(self):
        return self.nome_fantasia