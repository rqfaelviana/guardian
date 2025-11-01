from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Usuario, Empresa, Cliente

#painel de controle customizado para o 'Usuario'
class UsuarioAdmin(BaseUserAdmin):
    #formulário de criação
    fieldsets = (
        #seção de login
        (None, {'fields': ('email', 'password')}),

        #seção de informações pessoais
        ('Info pessoal', {'fields': ('first_name', 'last_name', 'empresa')}),

        #seção de permissões onde controle quem é adm
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser')})        
    )

    #colunas que serão mostrada na lista de usuários
    list_display = ('email', 'first_name', 'last_name', 'is_staff')

    ordering = ('email',)
    filter_horizontal = ()
    search_fields = ('email', 'first_name', 'last_name')

#registra o usuário
admin.site.register(Usuario, UsuarioAdmin)
#registra a empresa
admin.site.register(Empresa)
#Registra o cliente
admin.site.register(Cliente)
