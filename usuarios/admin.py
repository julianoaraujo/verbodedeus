from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Usuario, LinhaTeologica


@admin.register(LinhaTeologica)
class LinhaTeologicaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'criado_em']
    search_fields = ['nome']
    readonly_fields = ['criado_em']


@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'tipo_perfil', 'perfil_membro', 'ativo', 'criado_em']
    list_filter = ['tipo_perfil', 'perfil_membro', 'ativo', 'is_staff', 'is_superuser']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    # Copiar fieldsets do BaseUserAdmin e adicionar campos customizados
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'telefone', 'data_nascimento', 'foto')}),
        (_('Permissions'), {
            'fields': ('is_active', 'ativo', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'criado_em', 'atualizado_em')}),
        (_('Perfil Verbo de Deus'), {
            'fields': ('tipo_perfil', 'perfil_membro', 'linhas_teologicas'),
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'tipo_perfil'),
        }),
    )
    
    readonly_fields = ['criado_em', 'atualizado_em', 'last_login', 'date_joined']
    
    filter_horizontal = ['linhas_teologicas', 'groups', 'user_permissions']

