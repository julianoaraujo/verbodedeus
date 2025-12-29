from django.db import models
from django.conf import settings


class AconselhamentoPastoral(models.Model):
    """Modelo para solicitações de aconselhamento pastoral"""
    STATUS_CHOICES = [
        ('solicitado', 'Solicitado'),
        ('aceito', 'Aceito'),
        ('em_andamento', 'Em Andamento'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    ]
    
    solicitante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='aconselhamentos_solicitados'
    )
    lider_espiritual = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='aconselhamentos_atendidos',
        limit_choices_to={'perfil_membro': 'lider_espiritual'}
    )
    assunto = models.CharField(max_length=200)
    mensagem_inicial = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='solicitado')
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    finalizado_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Aconselhamento Pastoral"
        verbose_name_plural = "Aconselhamentos Pastorais"
        ordering = ['-criado_em']

    def __str__(self):
        return f"{self.assunto} - {self.solicitante.username}"


class MensagemAconselhamento(models.Model):
    """Modelo para mensagens trocadas no aconselhamento"""
    aconselhamento = models.ForeignKey(AconselhamentoPastoral, on_delete=models.CASCADE, related_name='mensagens')
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mensagem = models.TextField()
    lida = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Mensagem de Aconselhamento"
        verbose_name_plural = "Mensagens de Aconselhamento"
        ordering = ['criado_em']

    def __str__(self):
        return f"Mensagem de {self.autor.username} em {self.aconselhamento.assunto}"


class PedidoOracao(models.Model):
    """Modelo para pedidos de oração no grupo de oração"""
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('atendido', 'Atendido'),
        ('encerrado', 'Encerrado'),
    ]
    
    solicitante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pedidos_oracao')
    motivo = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativo')
    anonimo = models.BooleanField(default=False)
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Pedido de Oração"
        verbose_name_plural = "Pedidos de Oração"
        ordering = ['-criado_em']

    def __str__(self):
        nome = "Anônimo" if self.anonimo else self.solicitante.username
        return f"Pedido de {nome} - {self.motivo[:50]}"


class CompromissoOracao(models.Model):
    """Modelo para registrar quem se comprometeu a orar"""
    pedido = models.ForeignKey(PedidoOracao, on_delete=models.CASCADE, related_name='compromissos')
    membro = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Compromisso de Oração"
        verbose_name_plural = "Compromissos de Oração"
        unique_together = ['pedido', 'membro']
        ordering = ['-criado_em']

    def __str__(self):
        return f"{self.membro.username} orando por {self.pedido}"

