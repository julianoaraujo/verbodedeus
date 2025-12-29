from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from .models import TopicoForum, RespostaForum
from .forms import TopicoForumForm, RespostaForumForm
from usuarios.models import Usuario


def listar_topicos(request):
    """Lista todos os tópicos do fórum"""
    topicos = TopicoForum.objects.annotate(
        num_respostas=Count('respostas')
    ).all()
    
    busca = request.GET.get('busca')
    if busca:
        topicos = topicos.filter(
            Q(titulo__icontains=busca) | Q(conteudo__icontains=busca)
        )
    
    return render(request, 'forum/listar_topicos.html', {
        'topicos': topicos,
        'busca': busca,
    })


@login_required
def criar_topico(request):
    """Cria um novo tópico no fórum"""
    if not request.user.pode_cadastrar_forum():
        messages.error(request, 'Você não tem permissão para criar tópicos no fórum.')
        return redirect('listar_topicos')
    
    if request.method == 'POST':
        form = TopicoForumForm(request.POST)
        if form.is_valid():
            topico = form.save(commit=False)
            topico.autor = request.user
            topico.save()
            messages.success(request, 'Tópico criado com sucesso!')
            return redirect('detalhar_topico', pk=topico.pk)
    else:
        form = TopicoForumForm()
    
    return render(request, 'forum/criar_topico.html', {'form': form})


def detalhar_topico(request, pk):
    """Detalha um tópico e suas respostas"""
    topico = get_object_or_404(TopicoForum, pk=pk)
    
    # Incrementar visualizações
    topico.incrementar_visualizacao()
    
    respostas = topico.respostas.all()
    
    if request.method == 'POST' and request.user.is_authenticated:
        if topico.fechado:
            messages.error(request, 'Este tópico está fechado para novas respostas.')
        else:
            form = RespostaForumForm(request.POST)
            if form.is_valid():
                resposta = form.save(commit=False)
                resposta.topico = topico
                resposta.autor = request.user
                resposta.save()
                messages.success(request, 'Resposta adicionada com sucesso!')
                return redirect('detalhar_topico', pk=topico.pk)
        form = RespostaForumForm()
    else:
        form = RespostaForumForm() if request.user.is_authenticated else None
    
    return render(request, 'forum/detalhar_topico.html', {
        'topico': topico,
        'respostas': respostas,
        'form': form,
    })


@login_required
def editar_topico(request, pk):
    """Edita um tópico (apenas o autor)"""
    topico = get_object_or_404(TopicoForum, pk=pk)
    
    if topico.autor != request.user:
        messages.error(request, 'Você só pode editar seus próprios tópicos.')
        return redirect('detalhar_topico', pk=topico.pk)
    
    if request.method == 'POST':
        form = TopicoForumForm(request.POST, instance=topico)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tópico atualizado com sucesso!')
            return redirect('detalhar_topico', pk=topico.pk)
    else:
        form = TopicoForumForm(instance=topico)
    
    return render(request, 'forum/editar_topico.html', {'form': form, 'topico': topico})


@login_required
def editar_resposta(request, pk):
    """Edita uma resposta (apenas o autor)"""
    resposta = get_object_or_404(RespostaForum, pk=pk)
    
    if resposta.autor != request.user:
        messages.error(request, 'Você só pode editar suas próprias respostas.')
        return redirect('detalhar_topico', pk=resposta.topico.pk)
    
    if request.method == 'POST':
        form = RespostaForumForm(request.POST, instance=resposta)
        if form.is_valid():
            resposta.editado = True
            resposta.save()
            form.save()
            messages.success(request, 'Resposta atualizada com sucesso!')
            return redirect('detalhar_topico', pk=resposta.topico.pk)
    else:
        form = RespostaForumForm(instance=resposta)
    
    return render(request, 'forum/editar_resposta.html', {'form': form, 'resposta': resposta})


@login_required
def excluir_topico(request, pk):
    """Exclui um tópico (apenas o autor)"""
    topico = get_object_or_404(TopicoForum, pk=pk)
    
    if topico.autor != request.user:
        messages.error(request, 'Você só pode excluir seus próprios tópicos.')
        return redirect('detalhar_topico', pk=topico.pk)
    
    if request.method == 'POST':
        topico.delete()
        messages.success(request, 'Tópico excluído com sucesso!')
        return redirect('listar_topicos')
    
    return render(request, 'forum/excluir_topico.html', {'topico': topico})


@login_required
def excluir_resposta(request, pk):
    """Exclui uma resposta (apenas o autor)"""
    resposta = get_object_or_404(RespostaForum, pk=pk)
    topico_pk = resposta.topico.pk
    
    if resposta.autor != request.user:
        messages.error(request, 'Você só pode excluir suas próprias respostas.')
        return redirect('detalhar_topico', pk=topico_pk)
    
    if request.method == 'POST':
        resposta.delete()
        messages.success(request, 'Resposta excluída com sucesso!')
        return redirect('detalhar_topico', pk=topico_pk)
    
    return render(request, 'forum/excluir_resposta.html', {'resposta': resposta})

