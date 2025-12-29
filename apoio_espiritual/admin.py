from django.contrib import admin
from .models import AconselhamentoPastoral, MensagemAconselhamento, PedidoOracao, CompromissoOracao


class MensagemAconselhamentoInline(admin.TabularInline):
    model = MensagemAconselhamento
    extra = 0
    readonly_fields = ['criado_em']


@admin.register(AconselhamentoPastoral)
class AconselhamentoPastoralAdmin(admin.ModelAdmin):
    list_display = ['assunto', 'solicitante', 'lider_espiritual', 'status', 'criado_em']
    list_filter = ['status', 'criado_em']
    search_fields = ['assunto', 'solicitante__username', 'lider_espiritual__username']
    readonly_fields = ['criado_em', 'atualizado_em', 'finalizado_em']
    inlines = [MensagemAconselhamentoInline]


@admin.register(MensagemAconselhamento)
class MensagemAconselhamentoAdmin(admin.ModelAdmin):
    list_display = ['aconselhamento', 'autor', 'lida', 'criado_em']
    list_filter = ['lida', 'criado_em']
    readonly_fields = ['criado_em']


class CompromissoOracaoInline(admin.TabularInline):
    model = CompromissoOracao
    extra = 0
    readonly_fields = ['criado_em']


@admin.register(PedidoOracao)
class PedidoOracaoAdmin(admin.ModelAdmin):
    list_display = ['solicitante', 'status', 'anonimo', 'criado_em']
    list_filter = ['status', 'anonimo', 'criado_em']
    search_fields = ['motivo', 'solicitante__username']
    readonly_fields = ['criado_em', 'atualizado_em']
    inlines = [CompromissoOracaoInline]


@admin.register(CompromissoOracao)
class CompromissoOracaoAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'membro', 'criado_em']
    readonly_fields = ['criado_em']

