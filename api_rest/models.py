from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

# (Definido ANTES para que o 'Usuario' possa encontrá-lo)

class UsuarioManager(BaseUserManager):  
    '''
    Esta classe é o "Manual De Instruções" para criar usuários 
    do modelo Usuario.
    '''
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email deve ser fornecido')
        email = self.normalize_email(email) #Padroniza o email

        user = self.model(email=email, **extra_fields) #Cria o objeto usuário
        user.set_password(password) #Pega a senha e cria o hash
        user.save(using=self._db) #Salva o usuário no banco de dados
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        '''
        Cria e salva um Superusuário (admin) para o comando
        'createsuperuser' do Django.
        '''
        #Não vai usar no postman.
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuário deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuário deve ter is_superuser=True.')    

        return self.create_user(email, password, **extra_fields)


# --- PARTE 2: O MODELO (O MOLDE) ---

class Usuario(AbstractUser):
    # Campos
    username = None #Remove o campo username
    email = models.EmailField(_('endereço de e-mail'), unique=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email' #Utiliza o email como campo de login
    
    REQUIRED_FIELDS = []

    objects = UsuarioManager()

    def __str__(self):
        return self.email