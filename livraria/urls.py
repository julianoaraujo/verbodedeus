from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_livros, name='listar_livros'),
    path('<int:pk>/', views.detalhar_livro, name='detalhar_livro'),
    path('<int:pk>/comprar/', views.comprar_livro, name='comprar_livro'),
    path('minhas-compras/', views.minhas_compras, name='minhas_compras'),
]

