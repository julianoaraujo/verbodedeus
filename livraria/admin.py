from django.contrib import admin
from .models import Livro, Venda


@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'preco', 'preco_promocional', 'disponivel', 'criado_em']
    list_filter = ['disponivel', 'criado_em', 'linhas_teologicas']
    search_fields = ['titulo', 'autor', 'isbn']
    filter_horizontal = ['linhas_teologicas']
    readonly_fields = ['criado_em', 'atualizado_em', 'cadastrado_por']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'autor', 'descricao', 'sinopse', 'capa', 'isbn')
        }),
        ('Arquivos Digitais', {
            'fields': ('arquivo_pdf', 'arquivo_epub', 'arquivo_mobi')
        }),
        ('Preços', {
            'fields': ('preco', 'preco_promocional', 'disponivel')
        }),
        ('Categorização', {
            'fields': ('linhas_teologicas',)
        }),
        ('Metadados', {
            'fields': ('cadastrado_por', 'criado_em', 'atualizado_em')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Se é um novo objeto
            obj.cadastrado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ['livro', 'comprador', 'preco_pago', 'status', 'criado_em']
    list_filter = ['status', 'criado_em']
    search_fields = ['livro__titulo', 'comprador__username', 'codigo_transacao']
    readonly_fields = ['criado_em', 'atualizado_em']

