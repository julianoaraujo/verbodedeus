from django.urls import path
from . import views

urlpatterns = [
    # Página inicial
    path('', views.index_vdflix, name='index_vdflix'),
    
    # EBD
    path('ebd/', views.listar_ebd, name='listar_ebd'),
    path('ebd/<int:pk>/', views.detalhar_ebd, name='detalhar_ebd'),
    path('ebd/cadastrar/', views.cadastrar_ebd, name='cadastrar_ebd'),
    
    # Devocionais
    path('devocionais/', views.listar_devocionais, name='listar_devocionais'),
    path('devocionais/<int:pk>/', views.detalhar_devocional, name='detalhar_devocional'),
    path('devocionais/cadastrar/', views.cadastrar_devocional, name='cadastrar_devocional'),
    
    # Comentando
    path('comentando/<str:tipo>/', views.listar_comentando, name='listar_comentando'),
    path('comentando/<int:pk>/', views.detalhar_comentando, name='detalhar_comentando'),
    path('comentando/cadastrar/', views.cadastrar_comentando, name='cadastrar_comentando'),
    
    # Podcasts
    path('podcasts/', views.listar_podcasts, name='listar_podcasts'),
    path('podcasts/cadastrar/', views.cadastrar_podcast, name='cadastrar_podcast'),
    
    # Cultos
    path('cultos/', views.listar_cultos, name='listar_cultos'),
    path('cultos/cadastrar/', views.cadastrar_culto, name='cadastrar_culto'),
    
    # Plataformas
    path('plataformas/', views.listar_plataformas, name='listar_plataformas'),
    path('plataformas/cadastrar/', views.cadastrar_plataforma, name='cadastrar_plataforma'),
    
    # Cursos
    path('cursos/', views.listar_cursos, name='listar_cursos'),
    path('cursos/cadastrar/', views.cadastrar_curso, name='cadastrar_curso'),
    
    # Comentários
    path('comentario/<str:tipo>/<int:objeto_id>/', views.adicionar_comentario, name='adicionar_comentario'),
    
    # Playlist/Favoritos
    path('playlist/adicionar/<str:tipo>/<int:objeto_id>/', views.adicionar_playlist, name='adicionar_playlist'),
    path('playlist/', views.minha_playlist, name='minha_playlist'),
    
    # Sugestões de Pauta
    path('sugestao-pauta/', views.criar_sugestao_pauta, name='criar_sugestao_pauta'),
]

