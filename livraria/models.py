from django.db import models
from django.conf import settings
from usuarios.models import LinhaTeologica


class Livro(models.Model):
    """Modelo para livros digitais da livraria"""
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    descricao = models.TextField()
    sinopse = models.TextField(blank=True)
    capa = models.ImageField(upload_to='livraria/capas/', blank=True, null=True)
    
    # Arquivos digitais
    arquivo_pdf = models.FileField(upload_to='livraria/livros/pdf/', blank=True, null=True)
    arquivo_epub = models.FileField(upload_to='livraria/livros/epub/', blank=True, null=True)
    arquivo_mobi = models.FileField(upload_to='livraria/livros/mobi/', blank=True, null=True)
    
    # Preço e vendas
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    preco_promocional = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    disponivel = models.BooleanField(default=True)
    
    # Categorização
    linhas_teologicas = models.ManyToManyField(LinhaTeologica, blank=True)
    isbn = models.CharField(max_length=20, blank=True)
    
    # Metadados
    cadastrado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Livro"
        verbose_name_plural = "Livros"
        ordering = ['-criado_em']

    def __str__(self):
        return self.titulo

    def preco_atual(self):
        """Retorna o preço atual (promocional se disponível)"""
        return self.preco_promocional if self.preco_promocional else self.preco


class Venda(models.Model):
    """Modelo para registrar vendas de livros"""
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('paga', 'Paga'),
        ('cancelada', 'Cancelada'),
        ('reembolsada', 'Reembolsada'),
    ]
    
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    comprador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    preco_pago = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    
    # Dados do PagSeguro
    codigo_transacao = models.CharField(max_length=100, blank=True)
    referencia = models.CharField(max_length=100, blank=True)
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Venda"
        verbose_name_plural = "Vendas"
        ordering = ['-criado_em']

    def __str__(self):
        return f"{self.livro.titulo} - {self.comprador.username}"

