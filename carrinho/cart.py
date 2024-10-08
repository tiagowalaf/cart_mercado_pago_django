from products.models import Produto

class Carrinho:
    def __init__(self, request) -> None:
        self.session = request.session
        carrinho = self.session.get('session_key')
        if 'session_key' not in request.session:
            carrinho = self.session['session_key'] = {}
        self.cart_available_all_pages = carrinho

    def add(self, produto_, quantidade_desejada):
        produto_id = str(produto_.id)
        quantidade_desejada = str(quantidade_desejada)
        if produto_id in self.cart_available_all_pages:
            pass
        else:
            self.cart_available_all_pages[produto_id] = int(quantidade_desejada)
        self.session.modified = True

    def total_custo(self):
        produto_id = self.cart_available_all_pages.keys()
        produtos_bd = Produto.objects.filter(id__in=produto_id)
        quantidade = self.cart_available_all_pages
        total = 0
        for chave, valor in quantidade.items():
            chave = int(chave)
            for produto in produtos_bd:
                if produto.id == chave:
                    total = total + (produto.preco_produto * valor)
        return total

    def __len__(self):
        return len(self.cart_available_all_pages)
    
    def get_products(self):
        produto_ids = self.cart_available_all_pages.keys()
        produto = Produto.objects.filter(id__in=produto_ids)
        return produto
    
    def obter_qty_selecionada(self):
        quantidade = self.cart_available_all_pages
        return quantidade
    
    def atualizar(self, produto, quantidade):
        produto_id = str(produto)
        produto_qty = int(quantidade)
        nosso_carrinho = self.cart_available_all_pages # somente obtemos o carrinho
        nosso_carrinho[produto_id] = produto_qty 
        # Acessa o id enviado pelo 'data-index="{{prod.id}}' e seta o valor enviado pelo 'let quantidade'.
        self.session.modified = True
        return nosso_carrinho
    
    def deletar(self, produto):
        produto_id = str(produto)
        if produto_id in self.cart_available_all_pages:
            del self.cart_available_all_pages[produto_id]
            self.session.modified = True
            return self.cart_available_all_pages

# Devemos usar "session.modified = True" para informar ao Django que a sessão foi modificada, 
    # e os dados precisam ser salvos, Django só salva a sessão se detectar alterações nela.
# # Lembrando que são objetos mutáveis, usar "session.modified = True" garante que os dados serão salvos.