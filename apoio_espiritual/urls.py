from django.urls import path
from . import views

urlpatterns = [
    # Aconselhamento Pastoral
    path('aconselhamento/', views.listar_aconselhamentos, name='listar_aconselhamentos'),
    path('aconselhamento/solicitar/', views.solicitar_aconselhamento, name='solicitar_aconselhamento'),
    path('aconselhamento/<int:pk>/', views.detalhar_aconselhamento, name='detalhar_aconselhamento'),
    
    # Grupo de Oração
    path('oracao/', views.listar_pedidos_oracao, name='listar_pedidos_oracao'),
    path('oracao/criar/', views.criar_pedido_oracao, name='criar_pedido_oracao'),
    path('oracao/<int:pk>/comprometer/', views.comprometer_oracao, name='comprometer_oracao'),
]

