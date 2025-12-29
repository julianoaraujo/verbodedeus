from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import Livro, Venda
from .forms import LivroForm
import requests


def listar_livros(request):
    livros = Livro.objects.filter(disponivel=True)
    
    # Filtros
    linha_teologica = request.GET.get('linha_teologica')
    if linha_teologica:
        livros = livros.filter(linhas_teologicas__id=linha_teologica)
    
    busca = request.GET.get('busca')
    if busca:
        livros = livros.filter(titulo__icontains=busca) | livros.filter(autor__icontains=busca)
    
    return render(request, 'livraria/listar_livros.html', {
        'livros': livros,
        'linha_teologica': linha_teologica,
        'busca': busca,
    })


def detalhar_livro(request, pk):
    livro = get_object_or_404(Livro, pk=pk, disponivel=True)
    return render(request, 'livraria/detalhar_livro.html', {'livro': livro})


@login_required
def comprar_livro(request, pk):
    livro = get_object_or_404(Livro, pk=pk, disponivel=True)
    
    if request.method == 'POST':
        # Criar venda
        venda = Venda.objects.create(
            livro=livro,
            comprador=request.user,
            preco_pago=livro.preco_atual(),
            status='pendente'
        )
        
        # Integração com PagSeguro (simplificada - precisa implementar completamente)
        try:
            response = criar_pagamento_pagseguro(venda)
            if response and response.get('code'):
                venda.codigo_transacao = response['code']
                venda.referencia = str(venda.id)
                venda.save()
                return redirect(response.get('paymentLink', '#'))
            else:
                messages.error(request, 'Erro ao processar pagamento. Tente novamente.')
        except Exception as e:
            messages.error(request, f'Erro ao processar pagamento: {str(e)}')
    
    return render(request, 'livraria/comprar_livro.html', {'livro': livro})


def criar_pagamento_pagseguro(venda):
    """Cria pagamento no PagSeguro"""
    # Esta é uma implementação simplificada
    # Em produção, usar a biblioteca oficial do PagSeguro ou SDK
    
    url = 'https://ws.sandbox.pagseguro.uol.com.br/v2/checkout' if settings.PAGSEGURO_SANDBOX else 'https://ws.pagseguro.uol.com.br/v2/checkout'
    
    data = {
        'email': settings.PAGSEGURO_EMAIL,
        'token': settings.PAGSEGURO_TOKEN,
        'currency': 'BRL',
        'itemId1': str(venda.livro.id),
        'itemDescription1': venda.livro.titulo,
        'itemAmount1': f"{venda.preco_pago:.2f}",
        'itemQuantity1': '1',
        'reference': str(venda.id),
    }
    
    try:
        response = requests.post(url, data=data)
        # Processar resposta XML do PagSeguro
        # Retornar código de checkout e link de pagamento
        # Implementação completa requer parsing XML
        return {'code': 'checkout_code', 'paymentLink': '#'}
    except Exception as e:
        return None


@login_required
def minhas_compras(request):
    compras = Venda.objects.filter(comprador=request.user, status='paga')
    return render(request, 'livraria/minhas_compras.html', {'compras': compras})

