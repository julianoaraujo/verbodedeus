from django.contrib import admin
from .models import TopicoForum, RespostaForum


class RespostaForumInline(admin.TabularInline):
    model = RespostaForum
    extra = 0
    readonly_fields = ['criado_em', 'atualizado_em']


@admin.register(TopicoForum)
class TopicoForumAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'fixado', 'fechado', 'visualizacoes', 'criado_em']
    list_filter = ['fixado', 'fechado', 'criado_em']
    search_fields = ['titulo', 'conteudo', 'autor__username']
    readonly_fields = ['criado_em', 'atualizado_em', 'visualizacoes']
    inlines = [RespostaForumInline]


@admin.register(RespostaForum)
class RespostaForumAdmin(admin.ModelAdmin):
    list_display = ['topico', 'autor', 'editado', 'criado_em']
    list_filter = ['editado', 'criado_em']
    search_fields = ['conteudo', 'autor__username', 'topico__titulo']
    readonly_fields = ['criado_em', 'atualizado_em']

