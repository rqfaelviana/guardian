from django.db import models
from empresas.models import Empresa
# Create your models here.
class Cliente(models.Model):
    nome = models.CharField(max_length=100)

    cpf = models.CharField(max_length=14, unique=True, null=True, blank=True)

    data_nascimento = models.DateField(null=True, blank=True)

    class Genero(models.TextChoices):
        MASCULINO = 'M', 'Masculino'
        FEMININO = 'F', 'Feminino'
        OUTRO = 'O', 'Outro'
        NAO_INFORMADO = 'N', 'Não informado'
    
    genero = models.CharField(
        max_length=1,
        choices=Genero.choices,
        default=Genero.NAO_INFORMADO
    )

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
    