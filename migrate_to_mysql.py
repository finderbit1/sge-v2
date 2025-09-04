#!/usr/bin/env python3
"""
Script para migrar dados do SQLite para MySQL
"""

import os
import sys
import django
import json
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sge_sistema.settings')
django.setup()

from django.db import connections
from django.core.management import execute_from_command_line
from estoque.models import Categoria, Fornecedor, Produto, MovimentacaoEstoque, Venda, ItemVenda
from django.contrib.auth.models import User

def print_header():
    print("=" * 60)
    print("🔄 MIGRAÇÃO DE DADOS: SQLITE → MYSQL")
    print("=" * 60)
    print()

def backup_sqlite_data():
    """Fazer backup dos dados do SQLite"""
    print("💾 Fazendo backup dos dados do SQLite...")
    
    # Verificar se existe db.sqlite3
    if not os.path.exists('db.sqlite3'):
        print("❌ Arquivo db.sqlite3 não encontrado")
        return False
    
    # Fazer backup
    backup_file = f"backup_sqlite_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sqlite3"
    try:
        import shutil
        shutil.copy2('db.sqlite3', backup_file)
        print(f"✅ Backup criado: {backup_file}")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar backup: {e}")
        return False

def export_data_to_json():
    """Exportar dados para JSON"""
    print("📤 Exportando dados para JSON...")
    
    try:
        data = {
            'categorias': [],
            'fornecedores': [],
            'produtos': [],
            'movimentacoes': [],
            'vendas': [],
            'itens_venda': [],
            'usuarios': []
        }
        
        # Exportar categorias
        for categoria in Categoria.objects.all():
            data['categorias'].append({
                'nome': categoria.nome,
                'descricao': categoria.descricao,
                'ativa': categoria.ativa
            })
        
        # Exportar fornecedores
        for fornecedor in Fornecedor.objects.all():
            data['fornecedores'].append({
                'nome': fornecedor.nome,
                'cnpj': fornecedor.cnpj,
                'endereco': fornecedor.endereco,
                'telefone': fornecedor.telefone,
                'email': fornecedor.email,
                'contato': fornecedor.contato,
                'ativo': fornecedor.ativo
            })
        
        # Exportar produtos
        for produto in Produto.objects.all():
            data['produtos'].append({
                'codigo': produto.codigo,
                'nome': produto.nome,
                'descricao': produto.descricao,
                'categoria_nome': produto.categoria.nome,
                'fornecedor_nome': produto.fornecedor.nome,
                'preco_custo': float(produto.preco_custo),
                'preco_venda': float(produto.preco_venda),
                'estoque_minimo': produto.estoque_minimo,
                'estoque_atual': produto.estoque_atual,
                'unidade': produto.unidade,
                'ativo': produto.ativo
            })
        
        # Exportar movimentações
        for movimentacao in MovimentacaoEstoque.objects.all():
            data['movimentacoes'].append({
                'produto_codigo': movimentacao.produto.codigo,
                'tipo': movimentacao.tipo,
                'quantidade': float(movimentacao.quantidade),
                'usuario_username': movimentacao.usuario.username,
                'observacoes': movimentacao.observacoes,
                'destino': movimentacao.destino,
                'data_movimentacao': movimentacao.data_movimentacao.isoformat()
            })
        
        # Exportar vendas
        for venda in Venda.objects.all():
            data['vendas'].append({
                'numero_venda': venda.numero_venda,
                'cliente': venda.cliente,
                'vendedor_username': venda.vendedor.username,
                'total': float(venda.total),
                'desconto': float(venda.desconto),
                'status': venda.status,
                'observacoes': venda.observacoes,
                'data_venda': venda.data_venda.isoformat()
            })
        
        # Exportar itens de venda
        for item in ItemVenda.objects.all():
            data['itens_venda'].append({
                'venda_numero': item.venda.numero_venda,
                'produto_codigo': item.produto.codigo,
                'quantidade': item.quantidade,
                'preco_unitario': float(item.preco_unitario),
                'subtotal': float(item.subtotal)
            })
        
        # Exportar usuários
        for usuario in User.objects.all():
            data['usuarios'].append({
                'username': usuario.username,
                'email': usuario.email,
                'first_name': usuario.first_name,
                'last_name': usuario.last_name,
                'is_superuser': usuario.is_superuser,
                'is_staff': usuario.is_staff,
                'is_active': usuario.is_active,
                'date_joined': usuario.date_joined.isoformat()
            })
        
        # Salvar JSON
        json_file = f"dados_exportados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Dados exportados para: {json_file}")
        return json_file
        
    except Exception as e:
        print(f"❌ Erro ao exportar dados: {e}")
        return None

def import_data_to_mysql(json_file):
    """Importar dados para MySQL"""
    print("📥 Importando dados para MySQL...")
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Importar categorias
        print("  📁 Importando categorias...")
        for cat_data in data['categorias']:
            Categoria.objects.get_or_create(
                nome=cat_data['nome'],
                defaults={
                    'descricao': cat_data['descricao'],
                    'ativa': cat_data['ativa']
                }
            )
        
        # Importar fornecedores
        print("  🏢 Importando fornecedores...")
        for forn_data in data['fornecedores']:
            Fornecedor.objects.get_or_create(
                nome=forn_data['nome'],
                defaults={
                    'cnpj': forn_data['cnpj'],
                    'endereco': forn_data['endereco'],
                    'telefone': forn_data['telefone'],
                    'email': forn_data['email'],
                    'contato': forn_data['contato'],
                    'ativo': forn_data['ativo']
                }
            )
        
        # Importar usuários
        print("  👤 Importando usuários...")
        for user_data in data['usuarios']:
            User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'is_superuser': user_data['is_superuser'],
                    'is_staff': user_data['is_staff'],
                    'is_active': user_data['is_active']
                }
            )
        
        # Importar produtos
        print("  📦 Importando produtos...")
        for prod_data in data['produtos']:
            categoria = Categoria.objects.get(nome=prod_data['categoria_nome'])
            fornecedor = Fornecedor.objects.get(nome=prod_data['fornecedor_nome'])
            
            Produto.objects.get_or_create(
                codigo=prod_data['codigo'],
                defaults={
                    'nome': prod_data['nome'],
                    'descricao': prod_data['descricao'],
                    'categoria': categoria,
                    'fornecedor': fornecedor,
                    'preco_custo': prod_data['preco_custo'],
                    'preco_venda': prod_data['preco_venda'],
                    'estoque_minimo': prod_data['estoque_minimo'],
                    'estoque_atual': prod_data['estoque_atual'],
                    'unidade': prod_data['unidade'],
                    'ativo': prod_data['ativo']
                }
            )
        
        # Importar vendas
        print("  🛒 Importando vendas...")
        for venda_data in data['vendas']:
            vendedor = User.objects.get(username=venda_data['vendedor_username'])
            
            Venda.objects.get_or_create(
                numero_venda=venda_data['numero_venda'],
                defaults={
                    'cliente': venda_data['cliente'],
                    'vendedor': vendedor,
                    'total': venda_data['total'],
                    'desconto': venda_data['desconto'],
                    'status': venda_data['status'],
                    'observacoes': venda_data['observacoes']
                }
            )
        
        # Importar movimentações
        print("  🔄 Importando movimentações...")
        for mov_data in data['movimentacoes']:
            produto = Produto.objects.get(codigo=mov_data['produto_codigo'])
            usuario = User.objects.get(username=mov_data['usuario_username'])
            
            MovimentacaoEstoque.objects.create(
                produto=produto,
                tipo=mov_data['tipo'],
                quantidade=mov_data['quantidade'],
                usuario=usuario,
                observacoes=mov_data['observacoes'],
                destino=mov_data['destino']
            )
        
        # Importar itens de venda
        print("  📋 Importando itens de venda...")
        for item_data in data['itens_venda']:
            venda = Venda.objects.get(numero_venda=item_data['venda_numero'])
            produto = Produto.objects.get(codigo=item_data['produto_codigo'])
            
            ItemVenda.objects.create(
                venda=venda,
                produto=produto,
                quantidade=item_data['quantidade'],
                preco_unitario=item_data['preco_unitario'],
                subtotal=item_data['subtotal']
            )
        
        print("✅ Dados importados com sucesso para MySQL")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao importar dados: {e}")
        return False

def main():
    print_header()
    
    # Verificar se estamos usando MySQL
    from django.conf import settings
    if 'mysql' not in settings.DATABASES['default']['ENGINE']:
        print("❌ Sistema não está configurado para MySQL")
        print("💡 Execute primeiro: python setup_mysql.py")
        return False
    
    # Fazer backup do SQLite
    if not backup_sqlite_data():
        return False
    
    # Exportar dados para JSON
    json_file = export_data_to_json()
    if not json_file:
        return False
    
    # Importar dados para MySQL
    if not import_data_to_mysql(json_file):
        return False
    
    print()
    print("🎉 MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 60)
    print("📋 Resumo:")
    print(f"  - Backup SQLite: backup_sqlite_*.sqlite3")
    print(f"  - Dados exportados: {json_file}")
    print("  - Dados importados para MySQL")
    print()
    print("🚀 Próximos passos:")
    print("1. Execute: python manage.py runserver")
    print("2. Acesse: http://127.0.0.1:8000")
    print("3. Verifique se todos os dados estão corretos")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    main()

