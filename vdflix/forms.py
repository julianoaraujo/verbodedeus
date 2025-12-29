from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import (
    EBD, Devocional, Comentando, Podcast, Culto,
    Plataforma, Curso, SugestaoPauta, Comentario
)
from usuarios.models import LinhaTeologica


class ConteudoBaseForm(forms.ModelForm):
    """Form base para conteúdos"""
    linhas_teologicas = forms.ModelMultipleChoiceField(
        queryset=LinhaTeologica.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    
    class Meta:
        fields = ['titulo', 'descricao', 'url_externa', 'permite_comentarios',
                 'conteudo', 'arquivo_pdf', 'links_externos', 'linhas_teologicas', 'publicado']
        widgets = {
            'conteudo': CKEditorWidget(),
            'descricao': forms.Textarea(attrs={'rows': 3}),
            'links_externos': forms.Textarea(attrs={'rows': 2}),
        }


class EBDForm(ConteudoBaseForm):
    class Meta(ConteudoBaseForm.Meta):
        model = EBD


class DevocionalForm(ConteudoBaseForm):
    class Meta(ConteudoBaseForm.Meta):
        model = Devocional


class ComentandoForm(ConteudoBaseForm):
    class Meta(ConteudoBaseForm.Meta):
        model = Comentando
        fields = ConteudoBaseForm.Meta.fields + ['tipo']


class PodcastForm(ConteudoBaseForm):
    class Meta(ConteudoBaseForm.Meta):
        model = Podcast
        fields = ConteudoBaseForm.Meta.fields + ['plataforma']


class CultoForm(ConteudoBaseForm):
    class Meta(ConteudoBaseForm.Meta):
        model = Culto


class PlataformaForm(forms.ModelForm):
    linhas_teologicas = forms.ModelMultipleChoiceField(
        queryset=LinhaTeologica.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    
    class Meta:
        model = Plataforma
        fields = ['nome', 'url', 'descricao', 'linhas_teologicas']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }


class CursoForm(forms.ModelForm):
    linhas_teologicas = forms.ModelMultipleChoiceField(
        queryset=LinhaTeologica.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    
    class Meta:
        model = Curso
        fields = ['titulo', 'descricao', 'url', 'plataforma', 'imagem', 'linhas_teologicas']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }


class SugestaoPautaForm(forms.ModelForm):
    class Meta:
        model = SugestaoPauta
        fields = ['tipo', 'titulo', 'descricao']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 5}),
        }


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['comentario']
        widgets = {
            'comentario': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

