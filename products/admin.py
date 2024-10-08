from django.contrib import admin
from . import models

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome_produto']
admin.site.register(models.Produto)

class VendaAdmin(admin.ModelAdmin):
    list_display = ['produto_id']
admin.site.register(models.Vendas)