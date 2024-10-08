from django.db import models
from django.contrib.auth.models import User

class Produto(models.Model):
    nome_produto = models.CharField(max_length=25)
    preco_produto = models.DecimalField(decimal_places=2,max_digits=3,default=0)
    def __str__(self) -> str:
        return str(self.nome_produto)

class Vendas(models.Model):
    produto_id = models.ForeignKey(Produto, on_delete=models.CASCADE)
    usuario_id = models.ForeignKey(User, on_delete=models.CASCADE)
    # podemos criar um campo que irá receber a qty de itens comprados.
    def __str__(self) -> str:
        return f'{self.produto_id} {self.usuario_id}'