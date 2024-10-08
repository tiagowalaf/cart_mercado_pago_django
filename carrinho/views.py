from django.shortcuts import render, get_object_or_404
from products.models import Produto, Vendas
from django.http import JsonResponse, HttpResponse
from carrinho.cart import Carrinho
from django.http import HttpResponse
import mercadopago
from django.contrib.auth.models import User
from payament.settings import MERCADOPAGO

def home_carrinho(request):
    carrinho = Carrinho(request)
    carrinho_get_qty = carrinho.obter_qty_selecionada
    carrinho_produtos = carrinho.get_products
    total = carrinho.total_custo()
    return render(request, 'cart/cart_home.html', {
        'obter_produtos': carrinho_produtos, 'qty_desejada':carrinho_get_qty, 'total':total})

def cart_adicionar(request):
    carrinho = Carrinho(request)
    if request.POST.get('action') == 'post':
        _id = int(request.POST.get('produto_id')) # Pega a variável produto_id passada em DATA.
        qty_desejada = int(request.POST.get('quantidade_desejada'))
        produto = get_object_or_404(Produto, id=_id) # O id que vem pelo post e captado e selecionado.
        carrinho.add(produto_=produto, quantidade_desejada=qty_desejada)
        quantidade_de_itens = carrinho.__len__()
        resposta = JsonResponse({'qty': quantidade_de_itens})
        return resposta
    return HttpResponse('None') # A view deve retornar algo caso uma condição não seja atendida.

def cart_deletar(request):
    carrinho = Carrinho(request)
    if request.method == 'POST' and request.POST.get('action') == 'post':
        _id = int(request.POST.get('produto_id'))
        carrinho.deletar(produto=_id)
        resposta = JsonResponse({'deletado': _id})
        return resposta
    else:
        return HttpResponse('Quantidade inválida', status=400)
    return HttpResponse('None', status=400)

def cart_update(request):
    carrinho = Carrinho(request)
    if request.method == 'POST' and request.POST.get('action') == 'post':
        _id = int(request.POST.get('produto_id'))
        qty_desejada = request.POST.get('quantidade_desejada')
        if qty_desejada and qty_desejada.isdigit():
            qty_desejada = int(qty_desejada)
            carrinho.atualizar(produto=_id, quantidade=qty_desejada)
            resposta = JsonResponse({'qty': qty_desejada})
            return resposta
        else:
            return HttpResponse('Quantidade inválida', status=400)
    return HttpResponse('None', status=400)



sdk = mercadopago.SDK(MERCADOPAGO)
# Vamos criar uma preferência de pagamento, acesse o link abaixo. Iremos criar um pagamento personalizado.
# https://www.mercadopago.com.br/developers/pt/reference/preferences/_checkout_preferences/post

# Você pode seguir a doc abaixo para criar uma requisição ao mercadopago.
# https://pypi.org/project/mercadopago/
def criarpagamento(request):
    usuario = User.objects.get(id=request.user.id)
    carrinho = Carrinho(request).cart_available_all_pages
    lista = []
    for prd_id, qty_prd in carrinho.items():
        try:
            produto = Produto.objects.get(id=prd_id)
            item = {
                "id": str(produto.id),
                "title": produto.nome_produto,
                "description": "Descição do produto",
                "quantity": qty_prd,
                "currency_id": "BRL",
                "unit_price": float(produto.preco_produto),
            }
            lista.append(item) # vamos ter uma lista de dicionários.
        except Produto.DoesNotExist:
            print('Aqui informamos o usuário de algum erro')
            continue
    if not lista:
        return HttpResponse("O carrinho está vazio ou os produtos não foram encontrados", status=400)

    pagamento = { 
        'items': lista,
        "back_urls": {
            "success": "http://127.0.0.1:8000/carrinho/concluida/",
            "failure": "http://127.0.0.1:8000/carrinho/falhou/",
            "pending": "http://127.0.0.1:8000/carrinho/pendente/",
        },
        "payer": {"email": usuario.email},
        "auto_return": "all",
        "metadata": {
            "user_email": usuario.email,
            "product_id": lista[0]['id'] if lista else None,
            # Usado para garantir que a lista não esteja vazia.
        }
    }
    preference_response = sdk.preference().create(pagamento)
    preference = preference_response["response"]
    return HttpResponse(preference['init_point'])

# A função abaixo foi criada apenas para teste, caso o pagamento for aceito em um srvidor real,
# deve-se criar um WEBHOOK pelo mercadopago, para informar ao nosso server caso ocorra um pagamento.
def compraconcluida(request):
    id_pagamento = request.GET.get('collection_id')
    status = request.GET.get('status')
    if status == 'approved':
        payment_info = sdk.payment().get(id_pagamento)
        email_usuario = payment_info['response']['metadata']['user_email']
        usuario = User.objects.get(email=email_usuario)

        for item in payment_info['response']['additional_info']['items']:
            id_produto = item['id']
            produto = Produto.objects.get(id=id_produto)
            quantidade = item['quantity']
            
            for _ in range(int(quantidade)):
                venda = Vendas(produto_id=produto, usuario_id=usuario)
                venda.save()
    else:
        print('Pagamento não concluído')
    return HttpResponse('OK')


def camprafalhou(request):
    return HttpResponse('Não deu certo')

def comprapendente(request):
    return HttpResponse('Compra pendente')

# A função compraconcluida simula um webhook, precisamos de um domínio para conf o webhook no mercado pago.
# Como vamos renderizar um qr code em nosso site, teremos de criar um webhook para que todo pagamento feito,
# nosso site seja notificado através da rota que passarmos para o mercado pago.