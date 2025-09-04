from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Categoria, Fornecedor, Produto, MovimentacaoEstoque, Venda, ItemVenda


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao', 'ativa', 'data_criacao']
    list_filter = ['ativa', 'data_criacao']
    search_fields = ['nome', 'descricao']
    list_editable = ['ativa']


@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cnpj', 'telefone', 'email', 'ativo', 'data_cadastro']
    list_filter = ['ativo', 'data_cadastro']
    search_fields = ['nome', 'cnpj', 'email']
    list_editable = ['ativo']


class ItemVendaInline(admin.TabularInline):
    model = ItemVenda
    extra = 1
    readonly_fields = ['subtotal']


@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ['numero_venda', 'cliente', 'data_venda', 'status', 'total', 'vendedor']
    list_filter = ['status', 'data_venda', 'vendedor']
    search_fields = ['numero_venda', 'cliente']
    inlines = [ItemVendaInline]
    readonly_fields = ['total', 'data_venda']


@admin.register(ItemVenda)
class ItemVendaAdmin(admin.ModelAdmin):
    list_display = ['venda', 'produto', 'quantidade', 'preco_unitario', 'subtotal']
    list_filter = ['venda__data_venda']


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = [
        'codigo', 'nome', 'categoria', 'fornecedor', 'estoque_atual', 
        'estoque_minimo', 'preco_custo', 'preco_venda', 'status_estoque_display', 'ativo'
    ]
    list_filter = ['categoria', 'fornecedor', 'ativo', 'unidade', 'data_cadastro']
    search_fields = ['codigo', 'nome', 'descricao']
    list_editable = ['ativo']
    readonly_fields = ['data_cadastro', 'data_atualizacao', 'margem_lucro', 'valor_total_estoque']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('codigo', 'nome', 'descricao', 'categoria', 'fornecedor')
        }),
        ('Preços', {
            'fields': ('preco_custo', 'preco_venda', 'margem_lucro')
        }),
        ('Estoque', {
            'fields': ('estoque_atual', 'estoque_minimo', 'unidade', 'valor_total_estoque')
        }),
        ('Status', {
            'fields': ('ativo', 'data_cadastro', 'data_atualizacao')
        }),
    )

    def status_estoque_display(self, obj):
        """Exibe o status do estoque com cores"""
        status = obj.status_estoque
        if status == "Sem Estoque":
            color = "red"
        elif status == "Estoque Baixo":
            color = "orange"
        else:
            color = "green"
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            status
        )
    status_estoque_display.short_description = "Status do Estoque"

    def margem_lucro(self, obj):
        """Exibe a margem de lucro formatada"""
        return f"{obj.margem_lucro:.2f}%"
    margem_lucro.short_description = "Margem de Lucro (%)"

    def valor_total_estoque(self, obj):
        """Exibe o valor total do estoque formatado"""
        return f"R$ {obj.valor_total_estoque:,.2f}"
    valor_total_estoque.short_description = "Valor Total do Estoque"


@admin.register(MovimentacaoEstoque)
class MovimentacaoEstoqueAdmin(admin.ModelAdmin):
    list_display = [
        'produto', 'tipo', 'quantidade', 'usuario', 'data_movimentacao', 'observacoes'
    ]
    list_filter = ['tipo', 'data_movimentacao', 'usuario', 'produto__categoria']
    search_fields = ['produto__nome', 'produto__codigo', 'observacoes']
    readonly_fields = ['data_movimentacao']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('produto', 'usuario')


# Personalizações do Admin
admin.site.site_header = "Sistema de Gerenciamento de Estoque"
admin.site.site_title = "SGE Admin"
admin.site.index_title = "Painel Administrativo"