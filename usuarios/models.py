from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class LinhaTeologica(models.Model):
    """Modelo para linhas teológicas (ex: Reformada, Pentecostal, etc)"""
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Linha Teológica"
        verbose_name_plural = "Linhas Teológicas"
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Usuario(AbstractUser):
    """Modelo de usuário customizado com perfis"""
    
    TIPO_PERFIL_CHOICES = [
        ('visitante', 'Visitante'),
        ('membro', 'Membro'),
        ('produtor', 'Produtor'),
    ]
    
    PERFIL_MEMBRO_CHOICES = [
        ('curador', 'Curador'),
        ('redator', 'Redator'),
        ('lider_espiritual', 'Líder Espiritual'),
        ('revisor', 'Revisor'),
        ('social_media', 'Social Media'),
        ('programador', 'Programador'),
    ]
    
    # Campos básicos
    telefone = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Formato de telefone inválido")],
        blank=True
    )
    data_nascimento = models.DateField(null=True, blank=True)
    foto = models.ImageField(upload_to='usuarios/fotos/', blank=True, null=True)
    
    # Tipo de perfil
    tipo_perfil = models.CharField(
        max_length=20,
        choices=TIPO_PERFIL_CHOICES,
        default='visitante'
    )
    
    # Perfil de membro (pode ter múltiplos)
    perfil_membro = models.CharField(
        max_length=20,
        choices=PERFIL_MEMBRO_CHOICES,
        blank=True,
        null=True
    )
    
    # Linhas teológicas que o usuário segue
    linhas_teologicas = models.ManyToManyField(LinhaTeologica, blank=True)
    
    # Campos de controle
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ['username']

    def __str__(self):
        return self.username

    def is_curador(self):
        return self.perfil_membro == 'curador'
    
    def is_produtor(self):
        return self.tipo_perfil == 'produtor' or self.perfil_membro == 'produtor'
    
    def is_redator(self):
        return self.perfil_membro == 'redator'
    
    def is_lider_espiritual(self):
        return self.perfil_membro == 'lider_espiritual'
    
    def is_revisor(self):
        return self.perfil_membro == 'revisor'
    
    def is_social_media(self):
        return self.perfil_membro == 'social_media'
    
    def is_programador(self):
        return self.perfil_membro == 'programador'
    
    def is_visitante(self):
        return self.tipo_perfil == 'visitante'
    
    def pode_cadastrar_forum(self):
        """Verifica se o usuário pode cadastrar posts no fórum"""
        perfis_permitidos = ['curador', 'produtor', 'redator', 'lider_espiritual', 
                           'revisor', 'social_media', 'programador']
        return self.perfil_membro in perfis_permitidos or self.tipo_perfil == 'produtor'
    
    def pode_cadastrar_vdflix(self):
        """Verifica se o usuário pode cadastrar conteúdo no VDDFlix"""
        return self.is_curador() or self.is_produtor() or self.is_redator() or self.is_lider_espiritual()
    
    def pode_revisar_vdflix(self):
        """Verifica se o usuário pode revisar conteúdo do VDDFlix"""
        return self.is_revisor() or self.is_curador()

