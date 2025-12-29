from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField


class TopicoForum(models.Model):
    """Tópicos/posts do fórum interno"""
    titulo = models.CharField(max_length=200)
    conteudo = RichTextField()
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='topicos_forum')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    fixado = models.BooleanField(default=False)
    fechado = models.BooleanField(default=False)
    
    # Controle de visualizações
    visualizacoes = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Tópico do Fórum"
        verbose_name_plural = "Tópicos do Fórum"
        ordering = ['-fixado', '-criado_em']

    def __str__(self):
        return self.titulo

    def incrementar_visualizacao(self):
        self.visualizacoes += 1
        self.save(update_fields=['visualizacoes'])


class RespostaForum(models.Model):
    """Respostas aos tópicos do fórum"""
    topico = models.ForeignKey(TopicoForum, on_delete=models.CASCADE, related_name='respostas')
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    conteudo = RichTextField()
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    editado = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Resposta do Fórum"
        verbose_name_plural = "Respostas do Fórum"
        ordering = ['criado_em']

    def __str__(self):
        return f"Resposta de {self.autor.username} em {self.topico.titulo}"

