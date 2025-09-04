#!/usr/bin/env python3
"""
Script para sincronizar dados entre SQLite e MySQL
"""

import os
import sys
import django
import pymysql
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sge_sistema.settings')
django.setup()

# Importar modelos
from estoque.models import Categoria, Fornecedor, Produto, MovimentacaoEstoque, Venda, ItemVenda

# Configurações do MySQL
MYSQL_CONFIG = {
    'host': 'estoquesilkart.mysql.uhserver.com',
    'port': 3306,
    'user': 'mateusfinderbit',
    'password': 'MJs119629@03770',
    'database': 'estoquesilkart',
    'charset': 'utf8mb4'
}

def sincronizar_categorias():
    """Sincronizar categorias do SQLite para MySQL"""
    print("📂 Sincronizando categorias...")
    
    try:
        mysql_conn = pymysql.connect(**MYSQL_CONFIG)
        mysql_cursor = mysql_conn.cursor()
        
        # Limpar tabela MySQL
        mysql_cursor.execute("DELETE FROM estoque_categoria")
        
        # Inserir categorias do SQLite
        categorias = Categoria.objects.all()
        for categoria in categorias:
            mysql_cursor.execute("""
                INSERT INTO estoque_categoria (id, nome, descricao, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                categoria.id,
                categoria.nome,
                categoria.descricao,
                categoria.data_criacao,
                categoria.data_criacao  # Usar data_criacao como updated_at
            ))
        
        mysql_conn.commit()
        print(f"✅ {categorias.count()} categorias sincronizadas")
        
        mysql_cursor.close()
        mysql_conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro ao sincronizar categorias: {e}")
        return False

def sincronizar_fornecedores():
    """Sincronizar fornecedores do SQLite para MySQL"""
    print("🏢 Sincronizando fornecedores...")
    
    try:
        mysql_conn = pymysql.connect(**MYSQL_CONFIG)
        mysql_cursor = mysql_conn.cursor()
        
        # Limpar tabela MySQL
        mysql_cursor.execute("DELETE FROM estoque_fornecedor")
        
        # Inserir fornecedores do SQLite
        fornecedores = Fornecedor.objects.all()
        for fornecedor in fornecedores:
            mysql_cursor.execute("""
                INSERT INTO estoque_fornecedor (id, nome, cnpj, endereco, telefone, email, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                fornecedor.id,
                fornecedor.nome,
                fornecedor.cnpj,
                fornecedor.endereco,
                fornecedor.telefone,
                fornecedor.email,
                fornecedor.data_cadastro,
                fornecedor.data_cadastro  # Usar data_cadastro como updated_at
            ))
        
        mysql_conn.commit()
        print(f"✅ {fornecedores.count()} fornecedores sincronizados")
        
        mysql_cursor.close()
        mysql_conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro ao sincronizar fornecedores: {e}")
        return False

def sincronizar_produtos():
    """Sincronizar produtos do SQLite para MySQL"""
    print("📦 Sincronizando produtos...")
    
    try:
        mysql_conn = pymysql.connect(**MYSQL_CONFIG)
        mysql_cursor = mysql_conn.cursor()
        
        # Limpar tabela MySQL
        mysql_cursor.execute("DELETE FROM estoque_produto")
        
        # Inserir produtos do SQLite
        produtos = Produto.objects.all()
        for produto in produtos:
            mysql_cursor.execute("""
                INSERT INTO estoque_produto (id, nome, descricao, preco_custo, preco_venda, 
                estoque_atual, estoque_minimo, categoria_id, fornecedor_id, codigo_barras, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                produto.id,
                produto.nome,
                produto.descricao,
                float(produto.preco_custo),
                float(produto.preco_venda),
                produto.estoque_atual,
                produto.estoque_minimo,
                produto.categoria_id,
                produto.fornecedor_id,
                produto.codigo,  # Usar codigo em vez de codigo_barras
                produto.data_cadastro,
                produto.data_atualizacao
            ))
        
        mysql_conn.commit()
        print(f"✅ {produtos.count()} produtos sincronizados")
        
        mysql_cursor.close()
        mysql_conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro ao sincronizar produtos: {e}")
        return False

def sincronizar_movimentacoes():
    """Sincronizar movimentações do SQLite para MySQL"""
    print("🔄 Sincronizando movimentações...")
    
    try:
        mysql_conn = pymysql.connect(**MYSQL_CONFIG)
        mysql_cursor = mysql_conn.cursor()
        
        # Limpar tabela MySQL
        mysql_cursor.execute("DELETE FROM estoque_movimentacaoestoque")
        
        # Inserir movimentações do SQLite
        movimentacoes = MovimentacaoEstoque.objects.all()
        for mov in movimentacoes:
            mysql_cursor.execute("""
                INSERT INTO estoque_movimentacaoestoque (id, produto_id, tipo, quantidade, destino, observacoes, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                mov.id,
                mov.produto_id,
                mov.tipo,
                mov.quantidade,
                mov.destino,
                mov.observacoes,
                mov.data_movimentacao
            ))
        
        mysql_conn.commit()
        print(f"✅ {movimentacoes.count()} movimentações sincronizadas")
        
        mysql_cursor.close()
        mysql_conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro ao sincronizar movimentações: {e}")
        return False

def sincronizar_vendas():
    """Sincronizar vendas do SQLite para MySQL"""
    print("💰 Sincronizando vendas...")
    
    try:
        mysql_conn = pymysql.connect(**MYSQL_CONFIG)
        mysql_cursor = mysql_conn.cursor()
        
        # Limpar tabelas MySQL
        mysql_cursor.execute("DELETE FROM estoque_itemvenda")
        mysql_cursor.execute("DELETE FROM estoque_venda")
        
        # Inserir vendas do SQLite
        vendas = Venda.objects.all()
        for venda in vendas:
            mysql_cursor.execute("""
                INSERT INTO estoque_venda (id, cliente_nome, cliente_cpf, valor_total, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                venda.id,
                venda.cliente,
                '',  # Não temos cliente_cpf no modelo
                float(venda.total),
                venda.data_venda,
                venda.data_venda  # Usar data_venda como updated_at
            ))
            
            # Inserir itens da venda
            for item in venda.itemvenda_set.all():
                mysql_cursor.execute("""
                    INSERT INTO estoque_itemvenda (id, venda_id, produto_id, quantidade, preco_unitario, subtotal)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    item.id,
                    item.venda_id,
                    item.produto_id,
                    item.quantidade,
                    float(item.preco_unitario),
                    float(item.subtotal)
                ))
        
        mysql_conn.commit()
        print(f"✅ {vendas.count()} vendas sincronizadas")
        
        mysql_cursor.close()
        mysql_conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro ao sincronizar vendas: {e}")
        return False

def sincronizar_tudo():
    """Sincronizar todos os dados"""
    print("🚀 INICIANDO SINCRONIZAÇÃO SQLITE → MYSQL")
    print("=" * 50)
    
    sucesso = True
    
    # Sincronizar em ordem (respeitando foreign keys)
    if not sincronizar_categorias():
        sucesso = False
    
    if not sincronizar_fornecedores():
        sucesso = False
    
    if not sincronizar_produtos():
        sucesso = False
    
    if not sincronizar_movimentacoes():
        sucesso = False
    
    if not sincronizar_vendas():
        sucesso = False
    
    print("=" * 50)
    if sucesso:
        print("🎉 SINCRONIZAÇÃO CONCLUÍDA COM SUCESSO!")
        print("📊 Todos os dados foram transferidos para o MySQL remoto")
    else:
        print("⚠️  SINCRONIZAÇÃO CONCLUÍDA COM ALGUNS ERROS")
        print("📊 Verifique os logs acima para detalhes")
    
    return sucesso

if __name__ == "__main__":
    sincronizar_tudo()
