from django.shortcuts import render
from . models import Produto
# from django.http import HttpResponse
# import mercadopago
# from django.contrib.auth.models import User
# from payament.settings import MERCADOPAGO

def home(request):
    lista_produtos = Produto.objects.all()
    return render(request, 'home.html', context={'produtos':lista_produtos})

def detalhes(request, id_produto):
    produto = Produto.objects.get(id=id_produto)
    return render(request, 'detail/detail.html', context={'produto_detalhe':produto})