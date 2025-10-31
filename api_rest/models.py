from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

# class UsuarioManager(BaseUserManager):  
#     '''
#     Esta classe é o "Manual De Instruções" para criar usuários 
#     do modelo Usuario.
#     '''
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('O email deve ser fornecido')
#         email = self.normalize_email(email) #Padroniza o email

#         user = self.model(email=email, **extra_fields) #Cria o objeto usuário
#         user.set_password(password) #Pega a senha e cria o hash
#         user.save(using=self._db) #Salva o usuário no banco de dados

#         return user
    
    # def create_superuser(self, email, password=None, **extra_fields):
    #     '''
    #     Cria e salva um Superusuário (admin) para o comando
    #     'createsuperuser' do Django.
    #     '''
    #     #Não vai usar no postman.
    #     extra_fields.setdefault('is_staff', True)
    #     extra_fields.setdefault('is_superuser', True)
    #     extra_fields.setdefault('is_active', True)

    #     if extra_fields.get('is_staff') is not True:
    #         raise ValueError('Superusuário deve ter is_staff=True.')
    #     if extra_fields.get('is_superuser') is not True:
    #         raise ValueError('Superusuário deve ter is_superuser=True.')    

    #     return self.create_user(email, password, **extra_fields)


# --- Molde para criar usuários ---

class Usuario(AbstractUser):
    username = models.CharField(
        max_length=150, 
        unique=False,
        blank=True,
        null=True,
    ) #Remove o campo username
    email = models.EmailField(_('endereço de e-mail'), unique=True, null=False)
    data_cadastro = models.DateTimeField(auto_now_add=True)


    USERNAME_FIELD = 'email' #Utiliza o email como campo de login
    
    REQUIRED_FIELDS = []

    # objects = UsuarioManager()

    def __str__(self):
        return self.email
    
class Empresa(models.Model):
    nome_empresa = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18, unique=True)

    def __str__(self):
        return self.nome_empresa