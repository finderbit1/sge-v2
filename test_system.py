#!/usr/bin/env python
"""
Script de teste para verificar se o sistema de estoque está funcionando corretamente
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sge_sistema.settings')
django.setup()

from django.contrib.auth.models import User
from estoque.models import Categoria, Fornecedor, Produto

def test_system():
    print("🧪 Testando Sistema de Estoque...")
    print("=" * 50)
    
    # Teste 1: Verificar se o superusuário existe
    print("1. Verificando superusuário...")
    try:
        admin_user = User.objects.filter(is_superuser=True).first()
        if admin_user:
            print(f"   ✅ Superusuário encontrado: {admin_user.username}")
        else:
            print("   ❌ Nenhum superusuário encontrado")
            return False
    except Exception as e:
        print(f"   ❌ Erro ao verificar superusuário: {e}")
        return False
    
    # Teste 2: Verificar se os modelos estão funcionando
    print("\n2. Testando modelos...")
    try:
        # Testar Categoria
        categoria_count = Categoria.objects.count()
        print(f"   ✅ Categorias: {categoria_count} registros")
        
        # Testar Fornecedor
        fornecedor_count = Fornecedor.objects.count()
        print(f"   ✅ Fornecedores: {fornecedor_count} registros")
        
        # Testar Produto
        produto_count = Produto.objects.count()
        print(f"   ✅ Produtos: {produto_count} registros")
        
    except Exception as e:
        print(f"   ❌ Erro ao testar modelos: {e}")
        return False
    
    # Teste 3: Criar dados de teste
    print("\n3. Criando dados de teste...")
    try:
        # Criar categoria de teste
        categoria, created = Categoria.objects.get_or_create(
            nome="Teste",
            defaults={'descricao': 'Categoria para testes', 'ativa': True}
        )
        if created:
            print("   ✅ Categoria de teste criada")
        else:
            print("   ✅ Categoria de teste já existe")
        
        # Criar fornecedor de teste
        fornecedor, created = Fornecedor.objects.get_or_create(
            nome="Fornecedor Teste",
            defaults={
                'cnpj': '00.000.000/0001-00',
                'endereco': 'Endereço de teste',
                'telefone': '(00) 00000-0000',
                'email': 'teste@teste.com',
                'contato': 'Contato Teste',
                'ativo': True
            }
        )
        if created:
            print("   ✅ Fornecedor de teste criado")
        else:
            print("   ✅ Fornecedor de teste já existe")
        
        # Criar produto de teste
        produto, created = Produto.objects.get_or_create(
            codigo="TESTE001",
            defaults={
                'nome': 'Produto de Teste',
                'descricao': 'Produto criado para testes',
                'categoria': categoria,
                'fornecedor': fornecedor,
                'preco_custo': 10.00,
                'preco_venda': 15.00,
                'estoque_minimo': 5,
                'estoque_atual': 10,
                'unidade': 'UN',
                'ativo': True
            }
        )
        if created:
            print("   ✅ Produto de teste criado")
        else:
            print("   ✅ Produto de teste já existe")
        
    except Exception as e:
        print(f"   ❌ Erro ao criar dados de teste: {e}")
        return False
    
    # Teste 4: Verificar propriedades calculadas
    print("\n4. Testando propriedades calculadas...")
    try:
        produto = Produto.objects.first()
        if produto:
            print(f"   ✅ Margem de lucro: {produto.margem_lucro:.2f}%")
            print(f"   ✅ Valor total do estoque: R$ {produto.valor_total_estoque:.2f}")
            print(f"   ✅ Status do estoque: {produto.status_estoque}")
        else:
            print("   ⚠️  Nenhum produto encontrado para testar propriedades")
    except Exception as e:
        print(f"   ❌ Erro ao testar propriedades: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Todos os testes passaram! Sistema funcionando corretamente.")
    print("\n📋 Próximos passos:")
    print("   1. Acesse: http://127.0.0.1:8000")
    print("   2. Faça login com as credenciais do admin")
    print("   3. Comece a usar o sistema!")
    
    return True

if __name__ == "__main__":
    success = test_system()
    sys.exit(0 if success else 1)
