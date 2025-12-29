from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import TopicoForum, RespostaForum


class TopicoForumForm(forms.ModelForm):
    class Meta:
        model = TopicoForum
        fields = ['titulo', 'conteudo']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'conteudo': CKEditorWidget(),
        }


class RespostaForumForm(forms.ModelForm):
    class Meta:
        model = RespostaForum
        fields = ['conteudo']
        widgets = {
            'conteudo': CKEditorWidget(),
        }

