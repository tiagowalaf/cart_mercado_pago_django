from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('produto/<int:id_produto>/', views.detalhes, name='detalhes'),
]
