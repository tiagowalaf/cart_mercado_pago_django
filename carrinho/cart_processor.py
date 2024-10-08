from .cart import Carrinho

def cart_processor_f(request):
    return {'carrinho_pro': Carrinho(request)}

#Cria um contexto pra que o carrinho esteja disponível em
 # todas as páginas do site.