from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_carrinho, name='home_carrinho'),
    path('add/', views.cart_adicionar, name='adicionar_cart'),
    path('delete/', views.cart_deletar, name='deletar_cart'),
    path('update/', views.cart_update, name='update_cart'),

    path('criar/pagamento/', views.criarpagamento, name='criar_pagamento'),
    path('concluida/', views.compraconcluida, name='compra_concluida'),
    path('falhou/', views.camprafalhou, name='compra_falhou'),
    path('pendente/', views.comprapendente, name='compra_pendente'),
]