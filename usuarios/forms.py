from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario, LinhaTeologica


class UsuarioRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    telefone = forms.CharField(max_length=15, required=False)
    data_nascimento = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    tipo_perfil = forms.ChoiceField(choices=Usuario.TIPO_PERFIL_CHOICES, initial='visitante')
    linhas_teologicas = forms.ModelMultipleChoiceField(
        queryset=LinhaTeologica.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 
                 'password2', 'telefone', 'data_nascimento', 'tipo_perfil', 'linhas_teologicas')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Obrigatório. 150 caracteres ou menos.'
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None


class UsuarioUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'email', 'telefone', 'data_nascimento', 
                 'foto', 'tipo_perfil', 'perfil_membro', 'linhas_teologicas')

