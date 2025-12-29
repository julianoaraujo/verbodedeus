from django import forms
from .models import AconselhamentoPastoral, MensagemAconselhamento, PedidoOracao
from usuarios.models import Usuario


class AconselhamentoForm(forms.ModelForm):
    class Meta:
        model = AconselhamentoPastoral
        fields = ['lider_espiritual', 'assunto', 'mensagem_inicial']
        widgets = {
            'lider_espiritual': forms.Select(attrs={'class': 'form-control'}),
            'assunto': forms.TextInput(attrs={'class': 'form-control'}),
            'mensagem_inicial': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lider_espiritual'].queryset = Usuario.objects.filter(perfil_membro='lider_espiritual', ativo=True)


class MensagemAconselhamentoForm(forms.ModelForm):
    class Meta:
        model = MensagemAconselhamento
        fields = ['mensagem']
        widgets = {
            'mensagem': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class PedidoOracaoForm(forms.ModelForm):
    class Meta:
        model = PedidoOracao
        fields = ['motivo', 'anonimo']
        widgets = {
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'anonimo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

