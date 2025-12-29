from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from .models import (
    EBD, Devocional, Comentando, Podcast, Culto,
    Plataforma, Curso, PlaylistItem, Comentario, SugestaoPauta
)
from .forms import (
    EBDForm, DevocionalForm, ComentandoForm, PodcastForm, CultoForm,
    PlataformaForm, CursoForm, SugestaoPautaForm, ComentarioForm
)
from usuarios.models import Usuario


# ========== VIEWS PÚBLICAS ==========

def index_vdflix(request):
    """Página inicial do VDDFlix"""
    ebd_recentes = EBD.objects.filter(publicado=True)[:5]
    devocionais_recentes = Devocional.objects.filter(publicado=True)[:5]
    podcasts_recentes = Podcast.objects.filter(publicado=True)[:5]
    
    return render(request, 'vdflix/index.html', {
        'ebd_recentes': ebd_recentes,
        'devocionais_recentes': devocionais_recentes,
        'podcasts_recentes': podcasts_recentes,
    })


def listar_ebd(request):
    ebd_list = EBD.objects.filter(publicado=True)
    linha_teologica = request.GET.get('linha_teologica')
    if linha_teologica:
        ebd_list = ebd_list.filter(linhas_teologicas__id=linha_teologica)
    return render(request, 'vdflix/listar_ebd.html', {'ebd_list': ebd_list})


def detalhar_ebd(request, pk):
    ebd = get_object_or_404(EBD, pk=pk, publicado=True)
    comentarios = Comentario.objects.filter(tipo='ebd', objeto_id=pk) if ebd.permite_comentarios else []
    return render(request, 'vdflix/detalhar_ebd.html', {
        'ebd': ebd,
        'comentarios': comentarios,
    })


def listar_devocionais(request):
    devocionais = Devocional.objects.filter(publicado=True)
    linha_teologica = request.GET.get('linha_teologica')
    if linha_teologica:
        devocionais = devocionais.filter(linhas_teologicas__id=linha_teologica)
    return render(request, 'vdflix/listar_devocionais.html', {'devocionais': devocionais})


def detalhar_devocional(request, pk):
    devocional = get_object_or_404(Devocional, pk=pk, publicado=True)
    comentarios = Comentario.objects.filter(tipo='devocional', objeto_id=pk) if devocional.permite_comentarios else []
    return render(request, 'vdflix/detalhar_devocional.html', {
        'devocional': devocional,
        'comentarios': comentarios,
    })


def listar_comentando(request, tipo):
    comentando_list = Comentando.objects.filter(publicado=True, tipo=tipo)
    linha_teologica = request.GET.get('linha_teologica')
    if linha_teologica:
        comentando_list = comentando_list.filter(linhas_teologicas__id=linha_teologica)
    return render(request, 'vdflix/listar_comentando.html', {
        'comentando_list': comentando_list,
        'tipo': tipo,
    })


def detalhar_comentando(request, pk):
    comentando = get_object_or_404(Comentando, pk=pk, publicado=True)
    comentarios = Comentario.objects.filter(tipo='comentando', objeto_id=pk) if comentando.permite_comentarios else []
    return render(request, 'vdflix/detalhar_comentando.html', {
        'comentando': comentando,
        'comentarios': comentarios,
    })


def listar_podcasts(request):
    podcasts = Podcast.objects.filter(publicado=True)
    linha_teologica = request.GET.get('linha_teologica')
    if linha_teologica:
        podcasts = podcasts.filter(linhas_teologicas__id=linha_teologica)
    return render(request, 'vdflix/listar_podcasts.html', {'podcasts': podcasts})


def listar_cultos(request):
    cultos = Culto.objects.filter(publicado=True)
    linha_teologica = request.GET.get('linha_teologica')
    if linha_teologica:
        cultos = cultos.filter(linhas_teologicas__id=linha_teologica)
    return render(request, 'vdflix/listar_cultos.html', {'cultos': cultos})


def listar_plataformas(request):
    plataformas = Plataforma.objects.all()
    linha_teologica = request.GET.get('linha_teologica')
    if linha_teologica:
        plataformas = plataformas.filter(linhas_teologicas__id=linha_teologica)
    return render(request, 'vdflix/listar_plataformas.html', {'plataformas': plataformas})


def listar_cursos(request):
    cursos = Curso.objects.all()
    linha_teologica = request.GET.get('linha_teologica')
    if linha_teologica:
        cursos = cursos.filter(linhas_teologicas__id=linha_teologica)
    return render(request, 'vdflix/listar_cursos.html', {'cursos': cursos})


# ========== COMENTÁRIOS ==========

@login_required
def adicionar_comentario(request, tipo, objeto_id):
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.tipo = tipo
            comentario.objeto_id = objeto_id
            comentario.autor = request.user
            comentario.save()
            messages.success(request, 'Comentário adicionado com sucesso!')
            
            # Redirecionar de volta ao conteúdo
            if tipo == 'ebd':
                return redirect('detalhar_ebd', pk=objeto_id)
            elif tipo == 'devocional':
                return redirect('detalhar_devocional', pk=objeto_id)
            elif tipo == 'comentando':
                return redirect('detalhar_comentando', pk=objeto_id)
    
    return redirect('index_vdflix')


# ========== FAVORITOS/PLAYLIST ==========

@login_required
def adicionar_playlist(request, tipo, objeto_id):
    if request.user.is_visitante():
        item, created = PlaylistItem.objects.get_or_create(
            usuario=request.user,
            tipo=tipo,
            objeto_id=objeto_id
        )
        if created:
            messages.success(request, 'Adicionado à sua playlist!')
        else:
            messages.info(request, 'Já está na sua playlist.')
    else:
        messages.error(request, 'Apenas visitantes podem criar playlists.')
    
    return redirect(request.META.get('HTTP_REFERER', 'index_vdflix'))


@login_required
def minha_playlist(request):
    if not request.user.is_visitante():
        messages.error(request, 'Apenas visitantes podem ter playlists.')
        return redirect('index_vdflix')
    
    playlist = PlaylistItem.objects.filter(usuario=request.user)
    return render(request, 'vdflix/minha_playlist.html', {'playlist': playlist})


# ========== SUGESTÕES DE PAUTA ==========

@login_required
def criar_sugestao_pauta(request):
    if not request.user.is_visitante():
        messages.error(request, 'Apenas visitantes podem sugerir pautas.')
        return redirect('index_vdflix')
    
    if request.method == 'POST':
        form = SugestaoPautaForm(request.POST)
        if form.is_valid():
            sugestao = form.save(commit=False)
            sugestao.solicitante = request.user
            sugestao.save()
            messages.success(request, 'Sugestão de pauta enviada com sucesso!')
            return redirect('index_vdflix')
    else:
        form = SugestaoPautaForm()
    
    return render(request, 'vdflix/criar_sugestao_pauta.html', {'form': form})


# ========== VIEWS DE CADASTRO (COM PERMISSÕES) ==========

def pode_cadastrar_vdflix(user):
    return user.is_authenticated and (
        user.is_curador() or user.is_produtor() or 
        user.is_redator() or user.is_lider_espiritual()
    )


@login_required
@user_passes_test(pode_cadastrar_vdflix)
def cadastrar_ebd(request):
    if request.method == 'POST':
        form = EBDForm(request.POST, request.FILES)
        if form.is_valid():
            ebd = form.save(commit=False)
            ebd.cadastrado_por = request.user
            ebd.save()
            form.save_m2m()
            messages.success(request, 'EBD cadastrada com sucesso!')
            return redirect('detalhar_ebd', pk=ebd.pk)
    else:
        form = EBDForm()
    return render(request, 'vdflix/cadastrar_ebd.html', {'form': form})


@login_required
@user_passes_test(pode_cadastrar_vdflix)
def cadastrar_devocional(request):
    if request.method == 'POST':
        form = DevocionalForm(request.POST, request.FILES)
        if form.is_valid():
            devocional = form.save(commit=False)
            devocional.cadastrado_por = request.user
            devocional.save()
            form.save_m2m()
            messages.success(request, 'Devocional cadastrado com sucesso!')
            return redirect('detalhar_devocional', pk=devocional.pk)
    else:
        form = DevocionalForm()
    return render(request, 'vdflix/cadastrar_devocional.html', {'form': form})


@login_required
def cadastrar_comentando(request):
    if not (request.user.is_redator() or request.user.is_produtor()):
        messages.error(request, 'Você não tem permissão para cadastrar comentários.')
        return redirect('index_vdflix')
    
    if request.method == 'POST':
        form = ComentandoForm(request.POST, request.FILES)
        if form.is_valid():
            comentando = form.save(commit=False)
            comentando.cadastrado_por = request.user
            comentando.save()
            form.save_m2m()
            messages.success(request, 'Comentário cadastrado com sucesso!')
            return redirect('detalhar_comentando', pk=comentando.pk)
    else:
        form = ComentandoForm()
    return render(request, 'vdflix/cadastrar_comentando.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_lider_espiritual() or u.is_produtor())
def cadastrar_podcast(request):
    if request.method == 'POST':
        form = PodcastForm(request.POST, request.FILES)
        if form.is_valid():
            podcast = form.save(commit=False)
            podcast.cadastrado_por = request.user
            podcast.save()
            form.save_m2m()
            messages.success(request, 'Podcast cadastrado com sucesso!')
            return redirect('listar_podcasts')
    else:
        form = PodcastForm()
    return render(request, 'vdflix/cadastrar_podcast.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_lider_espiritual() or u.is_produtor())
def cadastrar_culto(request):
    if request.method == 'POST':
        form = CultoForm(request.POST, request.FILES)
        if form.is_valid():
            culto = form.save(commit=False)
            culto.cadastrado_por = request.user
            culto.save()
            form.save_m2m()
            messages.success(request, 'Culto cadastrado com sucesso!')
            return redirect('listar_cultos')
    else:
        form = CultoForm()
    return render(request, 'vdflix/cadastrar_culto.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_curador() or u.is_produtor())
def cadastrar_plataforma(request):
    if request.method == 'POST':
        form = PlataformaForm(request.POST)
        if form.is_valid():
            plataforma = form.save(commit=False)
            plataforma.cadastrado_por = request.user
            plataforma.save()
            form.save_m2m()
            messages.success(request, 'Plataforma cadastrada com sucesso!')
            return redirect('listar_plataformas')
    else:
        form = PlataformaForm()
    return render(request, 'vdflix/cadastrar_plataforma.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.is_curador() or u.is_produtor())
def cadastrar_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST, request.FILES)
        if form.is_valid():
            curso = form.save(commit=False)
            curso.cadastrado_por = request.user
            curso.save()
            form.save_m2m()
            messages.success(request, 'Curso cadastrado com sucesso!')
            return redirect('listar_cursos')
    else:
        form = CursoForm()
    return render(request, 'vdflix/cadastrar_curso.html', {'form': form})

