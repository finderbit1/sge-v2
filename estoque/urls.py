from django.urls import path
from . import views

app_name = 'estoque'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Produtos
    path('produtos/', views.lista_produtos, name='lista_produtos'),
    path('produtos/adicionar/', views.adicionar_produto, name='adicionar_produto'),
    path('produtos/<int:produto_id>/', views.detalhes_produto, name='detalhes_produto'),
    path('produtos/<int:produto_id>/editar/', views.editar_produto, name='editar_produto'),
    
    # Movimentações
    path('movimentacao/', views.movimentacao_estoque, name='movimentacao_estoque'),
    
    # Vendas
    path('vendas/nova/', views.nova_venda, name='nova_venda'),
    path('vendas/<int:venda_id>/', views.detalhes_venda, name='detalhes_venda'),
    
    # Relatórios
    path('relatorios/', views.relatorios, name='relatorios'),
    path('relatorios/produtos-pdf/', views.relatorio_produtos_pdf, name='relatorio_produtos_pdf'),
    path('relatorios/movimentacoes-excel/', views.relatorio_movimentacoes_excel, name='relatorio_movimentacoes_excel'),
    path('relatorios/exportar/', views.exportar_relatorio_excel, name='exportar_relatorio_excel'),
    
    # AJAX
    path('ajax/buscar-produto/', views.buscar_produto_ajax, name='buscar_produto_ajax'),
    path('ajax/dashboard/', views.dashboard_ajax, name='dashboard_ajax'),
]
