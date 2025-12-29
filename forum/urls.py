from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_topicos, name='listar_topicos'),
    path('criar/', views.criar_topico, name='criar_topico'),
    path('<int:pk>/', views.detalhar_topico, name='detalhar_topico'),
    path('<int:pk>/editar/', views.editar_topico, name='editar_topico'),
    path('<int:pk>/excluir/', views.excluir_topico, name='excluir_topico'),
    path('resposta/<int:pk>/editar/', views.editar_resposta, name='editar_resposta'),
    path('resposta/<int:pk>/excluir/', views.excluir_resposta, name='excluir_resposta'),
]

