from django import forms
from .models import Livro
from usuarios.models import LinhaTeologica


class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'descricao', 'sinopse', 'capa', 
                 'arquivo_pdf', 'arquivo_epub', 'arquivo_mobi', 
                 'preco', 'preco_promocional', 'disponivel', 
                 'linhas_teologicas', 'isbn']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 5}),
            'sinopse': forms.Textarea(attrs={'rows': 3}),
            'linhas_teologicas': forms.CheckboxSelectMultiple(),
        }

