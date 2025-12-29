from django.db import models
from django.conf import settings
from django.utils import timezone
from ckeditor.fields import RichTextField
from usuarios.models import LinhaTeologica


class ConteudoBase(models.Model):
    """Classe base para conteúdos do VDDFlix"""
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    url_externa = models.URLField(blank=True, null=True, help_text="URL para plataformas como Youtube, Spotify, etc")
    permite_comentarios = models.BooleanField(default=True)
    
    # Conteúdo em texto (alternativa à URL)
    conteudo = RichTextField(blank=True, null=True)
    arquivo_pdf = models.FileField(upload_to='vdflix/pdf/', blank=True, null=True)
    links_externos = models.TextField(blank=True, help_text="Links externos separados por vírgula")
    
    # Metadados
    data_publicacao = models.DateTimeField(auto_now_add=True)
    data_revisao = models.DateTimeField(null=True, blank=True)
    linhas_teologicas = models.ManyToManyField(LinhaTeologica, blank=True)
    
    # Controle
    publicado = models.BooleanField(default=False)
    revisado = models.BooleanField(default=False)
    cadastrado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        abstract = True
        ordering = ['-data_publicacao']

    def __str__(self):
        return self.titulo
    
    def save(self, *args, **kwargs):
        # Atualizar data_revisao se o objeto já existe e está sendo editado
        if self.pk:
            self.data_revisao = timezone.now()
        super().save(*args, **kwargs)


# ========== SUBMÓDULO ORIGINAIS ==========

class EBD(ConteudoBase):
    """Escola Bíblica Dominical"""
    class Meta:
        verbose_name = "EBD"
        verbose_name_plural = "EBDs"
        ordering = ['-data_publicacao']


class Devocional(ConteudoBase):
    """Devocionais"""
    class Meta:
        verbose_name = "Devocional"
        verbose_name_plural = "Devocionais"
        ordering = ['-data_publicacao']


class TipoComentando(models.TextChoices):
    NOTICIAS = 'noticias', 'Notícias'
    LIVROS = 'livros', 'Livros'
    ARTIGOS = 'artigos', 'Artigos'
    BIBLIA = 'biblia', 'Bíblia'


class Comentando(ConteudoBase):
    """Comentários de Notícias, Livros, Artigos ou Bíblia"""
    tipo = models.CharField(max_length=20, choices=TipoComentando.choices)
    
    class Meta:
        verbose_name = "Comentando"
        verbose_name_plural = "Comentando"
        ordering = ['-data_publicacao']


class Podcast(ConteudoBase):
    """Podcasts"""
    plataforma = models.CharField(max_length=100, blank=True, help_text="Ex: Spotify, Youtube, etc")
    
    class Meta:
        verbose_name = "Podcast"
        verbose_name_plural = "Podcasts"
        ordering = ['-data_publicacao']


class Culto(ConteudoBase):
    """Cultos"""
    class Meta:
        verbose_name = "Culto"
        verbose_name_plural = "Cultos"
        ordering = ['-data_publicacao']


# ========== SUBMÓDULO PLATAFORMAS ==========

class Plataforma(models.Model):
    """URLs de outras plataformas embedadas"""
    nome = models.CharField(max_length=100)
    url = models.URLField()
    descricao = models.TextField(blank=True)
    linhas_teologicas = models.ManyToManyField(LinhaTeologica, blank=True)
    cadastrado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Plataforma"
        verbose_name_plural = "Plataformas"
        ordering = ['nome']

    def __str__(self):
        return self.nome


# ========== SUBMÓDULO CURSOS ==========

class Curso(models.Model):
    """Cursos de outras plataformas"""
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    url = models.URLField()
    plataforma = models.CharField(max_length=100, blank=True, help_text="Ex: Udemy, Coursera, etc")
    imagem = models.ImageField(upload_to='vdflix/cursos/', blank=True, null=True)
    linhas_teologicas = models.ManyToManyField(LinhaTeologica, blank=True)
    cadastrado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ['-criado_em']

    def __str__(self):
        return self.titulo


# ========== FAVORITOS/PLAYLIST ==========

class PlaylistItem(models.Model):
    """Itens salvos em playlist (favoritos) pelos visitantes"""
    TIPO_CHOICES = [
        ('ebd', 'EBD'),
        ('devocional', 'Devocional'),
        ('comentando', 'Comentando'),
        ('podcast', 'Podcast'),
        ('culto', 'Culto'),
        ('plataforma', 'Plataforma'),
        ('curso', 'Curso'),
    ]
    
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='playlist')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    objeto_id = models.PositiveIntegerField()
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Item de Playlist"
        verbose_name_plural = "Itens de Playlist"
        unique_together = ['usuario', 'tipo', 'objeto_id']
        ordering = ['-criado_em']

    def __str__(self):
        return f"{self.usuario.username} - {self.get_tipo_display()}"


# ========== COMENTÁRIOS ==========

class Comentario(models.Model):
    """Comentários em conteúdos do VDDFlix"""
    TIPO_CHOICES = [
        ('ebd', 'EBD'),
        ('devocional', 'Devocional'),
        ('comentando', 'Comentando'),
    ]
    
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    objeto_id = models.PositiveIntegerField()
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comentario = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"
        ordering = ['-criado_em']

    def __str__(self):
        return f"Comentário de {self.autor.username}"


# ========== SUGESTÕES DE PAUTA ==========

class SugestaoPauta(models.Model):
    """Sugestões de pautas feitas por visitantes"""
    TIPO_CHOICES = [
        ('artigo', 'Artigo'),
        ('devocional', 'Devocional'),
        ('podcast', 'Podcast'),
    ]
    
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aceita', 'Aceita'),
        ('rejeitada', 'Rejeitada'),
    ]
    
    solicitante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Sugestão de Pauta"
        verbose_name_plural = "Sugestões de Pauta"
        ordering = ['-criado_em']

    def __str__(self):
        return f"{self.titulo} - {self.solicitante.username}"

