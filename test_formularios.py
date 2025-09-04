#!/usr/bin/env python3
"""
Script para testar todos os formulários e relatórios do sistema
"""

import os
import sys
import django
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from estoque.models import Categoria, Fornecedor, Produto, MovimentacaoEstoque, Venda, ItemVenda
from estoque.forms import ProdutoForm, MovimentacaoForm, VendaForm, ItemVendaForm, BuscaProdutoForm

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sge_sistema.settings')
django.setup()

def test_formularios():
    """Testar todos os formulários do sistema"""
    print("🔍 Testando Formulários do Sistema...")
    
    # Criar dados de teste
    categoria = Categoria.objects.create(
        nome="Teste Categoria",
        descricao="Categoria para teste",
        ativa=True
    )
    
    fornecedor = Fornecedor.objects.create(
        nome="Fornecedor Teste",
        cnpj="12.345.678/0001-90",
        endereco="Endereço Teste",
        telefone="(11) 99999-9999",
        email="teste@fornecedor.com",
        contato="João Silva",
        ativo=True
    )
    
    produto = Produto.objects.create(
        codigo="TEST001",
        nome="Produto Teste",
        descricao="Produto para teste",
        categoria=categoria,
        fornecedor=fornecedor,
        preco_custo=10.00,
        preco_venda=15.00,
        estoque_minimo=5,
        estoque_atual=20,
        unidade="UN",
        ativo=True
    )
    
    print("✅ Dados de teste criados com sucesso!")
    
    # Testar Formulário de Produto
    print("\n📝 Testando Formulário de Produto...")
    produto_data = {
        'codigo': 'TEST002',
        'nome': 'Produto Teste 2',
        'descricao': 'Segundo produto para teste',
        'categoria': categoria.id,
        'fornecedor': fornecedor.id,
        'preco_custo': 20.00,
        'preco_venda': 30.00,
        'estoque_minimo': 3,
        'estoque_atual': 15,
        'unidade': 'UN',
        'ativo': True
    }
    
    form = ProdutoForm(data=produto_data)
    if form.is_valid():
        print("✅ Formulário de Produto: VÁLIDO")
        produto2 = form.save()
        print(f"✅ Produto criado: {produto2.nome}")
    else:
        print("❌ Formulário de Produto: INVÁLIDO")
        print(f"Erros: {form.errors}")
    
    # Testar Formulário de Movimentação
    print("\n📝 Testando Formulário de Movimentação...")
    movimentacao_data = {
        'produto': produto.id,
        'tipo': 'ENTRADA',
        'quantidade': 10,
        'observacoes': 'Movimentação de teste',
        'destino': 'Estoque Principal'
    }
    
    form = MovimentacaoForm(data=movimentacao_data)
    if form.is_valid():
        print("✅ Formulário de Movimentação: VÁLIDO")
        movimentacao = form.save()
        print(f"✅ Movimentação criada: {movimentacao.tipo} - {movimentacao.quantidade} unidades")
    else:
        print("❌ Formulário de Movimentação: INVÁLIDO")
        print(f"Erros: {form.errors}")
    
    # Testar Formulário de Venda
    print("\n📝 Testando Formulário de Venda...")
    venda_data = {
        'cliente': 'Cliente Teste',
        'desconto': 0.00,
        'observacoes': 'Venda de teste'
    }
    
    form = VendaForm(data=venda_data)
    if form.is_valid():
        print("✅ Formulário de Venda: VÁLIDO")
        venda = form.save()
        print(f"✅ Venda criada: {venda.cliente}")
    else:
        print("❌ Formulário de Venda: INVÁLIDO")
        print(f"Erros: {form.errors}")
    
    # Testar Formulário de Item de Venda
    print("\n📝 Testando Formulário de Item de Venda...")
    item_data = {
        'produto': produto.id,
        'quantidade': 2,
        'preco_unitario': 15.00
    }
    
    form = ItemVendaForm(data=item_data)
    if form.is_valid():
        print("✅ Formulário de Item de Venda: VÁLIDO")
        item = form.save()
        print(f"✅ Item criado: {item.produto.nome} - {item.quantidade} unidades")
    else:
        print("❌ Formulário de Item de Venda: INVÁLIDO")
        print(f"Erros: {form.errors}")
    
    # Testar Formulário de Busca
    print("\n📝 Testando Formulário de Busca...")
    busca_data = {
        'busca': 'Produto Teste',
        'categoria': categoria.id,
        'status_estoque': ''
    }
    
    form = BuscaProdutoForm(data=busca_data)
    if form.is_valid():
        print("✅ Formulário de Busca: VÁLIDO")
        print(f"✅ Busca: {form.cleaned_data['busca']}")
    else:
        print("❌ Formulário de Busca: INVÁLIDO")
        print(f"Erros: {form.errors}")
    
    print("\n🎉 Teste de Formulários Concluído!")

def test_relatorios():
    """Testar geração de relatórios"""
    print("\n📊 Testando Geração de Relatórios...")
    
    # Verificar produtos com estoque baixo
    produtos_estoque_baixo = Produto.objects.filter(
        ativo=True,
        estoque_atual__lte=models.F('estoque_minimo')
    ).count()
    
    print(f"✅ Produtos com estoque baixo: {produtos_estoque_baixo}")
    
    # Verificar produtos sem estoque
    produtos_sem_estoque = Produto.objects.filter(
        ativo=True,
        estoque_atual=0
    ).count()
    
    print(f"✅ Produtos sem estoque: {produtos_sem_estoque}")
    
    # Verificar total de produtos
    total_produtos = Produto.objects.filter(ativo=True).count()
    print(f"✅ Total de produtos: {total_produtos}")
    
    # Verificar total de vendas
    total_vendas = Venda.objects.count()
    print(f"✅ Total de vendas: {total_vendas}")
    
    # Verificar movimentações
    total_movimentacoes = MovimentacaoEstoque.objects.count()
    print(f"✅ Total de movimentações: {total_movimentacoes}")
    
    print("\n🎉 Teste de Relatórios Concluído!")

def test_views():
    """Testar views do sistema"""
    print("\n🌐 Testando Views do Sistema...")
    
    client = Client()
    
    # Testar login
    print("🔐 Testando página de login...")
    response = client.get('/accounts/login/')
    if response.status_code == 200:
        print("✅ Página de login: OK")
    else:
        print(f"❌ Página de login: ERRO {response.status_code}")
    
    # Testar dashboard (deve redirecionar para login)
    print("🏠 Testando dashboard...")
    response = client.get('/estoque/')
    if response.status_code == 302:
        print("✅ Dashboard redireciona para login: OK")
    else:
        print(f"❌ Dashboard: ERRO {response.status_code}")
    
    print("\n🎉 Teste de Views Concluído!")

if __name__ == "__main__":
    try:
        test_formularios()
        test_relatorios()
        test_views()
        print("\n🎉 TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
    except Exception as e:
        print(f"\n❌ ERRO DURANTE OS TESTES: {e}")
        import traceback
        traceback.print_exc()
