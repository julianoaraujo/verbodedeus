from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import AconselhamentoPastoral, MensagemAconselhamento, PedidoOracao, CompromissoOracao
from .forms import AconselhamentoForm, MensagemAconselhamentoForm, PedidoOracaoForm
from usuarios.models import Usuario


@login_required
def listar_aconselhamentos(request):
    """Lista aconselhamentos do usuário (como solicitante ou líder)"""
    if request.user.is_lider_espiritual():
        aconselhamentos = AconselhamentoPastoral.objects.filter(lider_espiritual=request.user)
    else:
        aconselhamentos = AconselhamentoPastoral.objects.filter(solicitante=request.user)
    
    status = request.GET.get('status')
    if status:
        aconselhamentos = aconselhamentos.filter(status=status)
    
    return render(request, 'apoio_espiritual/listar_aconselhamentos.html', {
        'aconselhamentos': aconselhamentos,
        'status': status,
    })


@login_required
def solicitar_aconselhamento(request):
    """Permite que membros (exceto líderes) solicitem aconselhamento"""
    if request.user.is_lider_espiritual():
        messages.error(request, 'Líderes espirituais não podem solicitar aconselhamento.')
        return redirect('listar_aconselhamentos')
    
    if request.method == 'POST':
        form = AconselhamentoForm(request.POST)
        if form.is_valid():
            aconselhamento = form.save(commit=False)
            aconselhamento.solicitante = request.user
            aconselhamento.save()
            messages.success(request, 'Solicitação de aconselhamento enviada com sucesso!')
            return redirect('detalhar_aconselhamento', pk=aconselhamento.pk)
    else:
        form = AconselhamentoForm()
    
    return render(request, 'apoio_espiritual/solicitar_aconselhamento.html', {'form': form})


@login_required
def detalhar_aconselhamento(request, pk):
    """Detalha um aconselhamento e permite troca de mensagens"""
    aconselhamento = get_object_or_404(AconselhamentoPastoral, pk=pk)
    
    # Verificar se o usuário tem permissão para ver este aconselhamento
    if aconselhamento.solicitante != request.user and aconselhamento.lider_espiritual != request.user:
        messages.error(request, 'Você não tem permissão para acessar este aconselhamento.')
        return redirect('listar_aconselhamentos')
    
    mensagens = aconselhamento.mensagens.all()
    
    if request.method == 'POST':
        form = MensagemAconselhamentoForm(request.POST)
        if form.is_valid():
            mensagem = form.save(commit=False)
            mensagem.aconselhamento = aconselhamento
            mensagem.autor = request.user
            mensagem.save()
            
            # Atualizar status se necessário
            if aconselhamento.status == 'solicitado':
                aconselhamento.status = 'aceito'
                aconselhamento.save()
            elif aconselhamento.status == 'aceito':
                aconselhamento.status = 'em_andamento'
                aconselhamento.save()
            
            messages.success(request, 'Mensagem enviada com sucesso!')
            return redirect('detalhar_aconselhamento', pk=aconselhamento.pk)
    else:
        form = MensagemAconselhamentoForm()
    
    # Marcar mensagens como lidas
    mensagens.filter(~Q(autor=request.user)).update(lida=True)
    
    return render(request, 'apoio_espiritual/detalhar_aconselhamento.html', {
        'aconselhamento': aconselhamento,
        'mensagens': mensagens,
        'form': form,
    })


@login_required
def listar_pedidos_oracao(request):
    """Lista todos os pedidos de oração"""
    pedidos = PedidoOracao.objects.filter(status='ativo')
    return render(request, 'apoio_espiritual/listar_pedidos_oracao.html', {'pedidos': pedidos})


@login_required
def criar_pedido_oracao(request):
    """Permite criar um pedido de oração"""
    if request.method == 'POST':
        form = PedidoOracaoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.solicitante = request.user
            pedido.save()
            messages.success(request, 'Pedido de oração criado com sucesso!')
            return redirect('listar_pedidos_oracao')
    else:
        form = PedidoOracaoForm()
    
    return render(request, 'apoio_espiritual/criar_pedido_oracao.html', {'form': form})


@login_required
def comprometer_oracao(request, pk):
    """Permite que um membro se comprometa a orar por um pedido"""
    pedido = get_object_or_404(PedidoOracao, pk=pk)
    
    if request.method == 'POST':
        compromisso, created = CompromissoOracao.objects.get_or_create(
            pedido=pedido,
            membro=request.user
        )
        if created:
            messages.success(request, 'Você se comprometeu a orar por este pedido!')
        else:
            messages.info(request, 'Você já está orando por este pedido.')
    
    return redirect('listar_pedidos_oracao')

