from django.contrib import admin
from .models import (
    EBD, Devocional, Comentando, Podcast, Culto,
    Plataforma, Curso, PlaylistItem, Comentario, SugestaoPauta
)


@admin.register(EBD)
class EBDAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'cadastrado_por', 'publicado', 'revisado', 'data_publicacao']
    list_filter = ['publicado', 'revisado', 'data_publicacao', 'linhas_teologicas']
    search_fields = ['titulo', 'descricao']
    filter_horizontal = ['linhas_teologicas']
    readonly_fields = ['data_publicacao', 'data_revisao', 'cadastrado_por']
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.cadastrado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(Devocional)
class DevocionalAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'cadastrado_por', 'publicado', 'revisado', 'data_publicacao']
    list_filter = ['publicado', 'revisado', 'data_publicacao', 'linhas_teologicas']
    search_fields = ['titulo', 'descricao']
    filter_horizontal = ['linhas_teologicas']
    readonly_fields = ['data_publicacao', 'data_revisao', 'cadastrado_por']
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.cadastrado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comentando)
class ComentandoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'cadastrado_por', 'publicado', 'revisado', 'data_publicacao']
    list_filter = ['tipo', 'publicado', 'revisado', 'data_publicacao', 'linhas_teologicas']
    search_fields = ['titulo', 'descricao']
    filter_horizontal = ['linhas_teologicas']
    readonly_fields = ['data_publicacao', 'data_revisao', 'cadastrado_por']
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.cadastrado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'plataforma', 'cadastrado_por', 'publicado', 'revisado', 'data_publicacao']
    list_filter = ['plataforma', 'publicado', 'revisado', 'data_publicacao', 'linhas_teologicas']
    search_fields = ['titulo', 'descricao']
    filter_horizontal = ['linhas_teologicas']
    readonly_fields = ['data_publicacao', 'data_revisao', 'cadastrado_por']
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.cadastrado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(Culto)
class CultoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'cadastrado_por', 'publicado', 'revisado', 'data_publicacao']
    list_filter = ['publicado', 'revisado', 'data_publicacao', 'linhas_teologicas']
    search_fields = ['titulo', 'descricao']
    filter_horizontal = ['linhas_teologicas']
    readonly_fields = ['data_publicacao', 'data_revisao', 'cadastrado_por']
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.cadastrado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(Plataforma)
class PlataformaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'url', 'cadastrado_por', 'criado_em']
    search_fields = ['nome', 'url']
    filter_horizontal = ['linhas_teologicas']
    readonly_fields = ['criado_em', 'cadastrado_por']
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.cadastrado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'plataforma', 'cadastrado_por', 'criado_em']
    list_filter = ['plataforma', 'criado_em', 'linhas_teologicas']
    search_fields = ['titulo', 'descricao']
    filter_horizontal = ['linhas_teologicas']
    readonly_fields = ['criado_em', 'cadastrado_por']
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.cadastrado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(PlaylistItem)
class PlaylistItemAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'tipo', 'criado_em']
    list_filter = ['tipo', 'criado_em']
    readonly_fields = ['criado_em']


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['autor', 'tipo', 'criado_em']
    list_filter = ['tipo', 'criado_em']
    readonly_fields = ['criado_em', 'atualizado_em']


@admin.register(SugestaoPauta)
class SugestaoPautaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'solicitante', 'status', 'criado_em']
    list_filter = ['tipo', 'status', 'criado_em']
    search_fields = ['titulo', 'descricao']
    readonly_fields = ['criado_em']

