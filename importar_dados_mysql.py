#!/usr/bin/env python3
"""
Script para importar dados do estoquesilkart.json para MySQL
"""

import json
import pymysql
from datetime import datetime

# Configurações do banco
DB_CONFIG = {
    'host': 'estoquesilkart.mysql.uhserver.com',
    'port': 3306,
    'user': 'mateusfinderbit',
    'password': 'MJs119629@03770',
    'database': 'estoquesilkart',
    'charset': 'utf8mb4'
}

def importar_dados():
    """Importar dados do JSON para MySQL"""
    
    print("📥 IMPORTANDO DADOS DO ESTOQUESILKART.JSON")
    print("=" * 50)
    
    try:
        # Conectar ao MySQL
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("✅ Conectado ao MySQL remoto!")
        
        # Ler arquivo JSON
        print("\n📖 Lendo arquivo estoquesilkart.json...")
        with open('estoquesilkart.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ Arquivo lido com sucesso! {len(data)} registros encontrados")
        
        # Limpar dados existentes
        print("\n🗑️ Limpando dados existentes...")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        tabelas_para_limpar = [
            'estoque_itemvenda',
            'estoque_movimentacaoestoque', 
            'estoque_venda',
            'estoque_produto',
            'estoque_fornecedor',
            'estoque_categoria'
        ]
        
        for tabela in tabelas_para_limpar:
            cursor.execute(f"DELETE FROM {tabela}")
            print(f"  ✅ {tabela} limpa")
        
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        # 1. Importar categorias
        print("\n📂 Importando categorias...")
        categorias_map = {}
        
        # Categoria padrão
        cursor.execute("""
            INSERT INTO estoque_categoria (nome, descricao, ativa) 
            VALUES ('Geral', 'Categoria padrão', TRUE)
        """)
        categorias_map['Geral'] = cursor.lastrowid
        
        # Categorias do JSON
        categorias_unicas = set()
        for item in data:
            if 'categoria' in item and item['categoria']:
                categorias_unicas.add(item['categoria'])
        
        for categoria_nome in categorias_unicas:
            cursor.execute("""
                INSERT INTO estoque_categoria (nome, descricao, ativa) 
                VALUES (%s, %s, %s)
            """, (categoria_nome, f'Categoria: {categoria_nome}', True))
            categorias_map[categoria_nome] = cursor.lastrowid
        
        print(f"✅ {len(categorias_map)} categorias importadas")
        
        # 2. Importar fornecedores
        print("\n🏢 Importando fornecedores...")
        fornecedores_map = {}
        
        # Fornecedor padrão
        cursor.execute("""
            INSERT INTO estoque_fornecedor (nome, cnpj, ativo) 
            VALUES ('Fornecedor Padrão', '00.000.000/0001-00', TRUE)
        """)
        fornecedores_map['Fornecedor Padrão'] = cursor.lastrowid
        
        # Fornecedores do JSON
        fornecedores_unicos = set()
        for item in data:
            if 'fornecedor' in item and item['fornecedor']:
                fornecedores_unicos.add(item['fornecedor'])
        
        for fornecedor_nome in fornecedores_unicos:
            cursor.execute("""
                INSERT INTO estoque_fornecedor (nome, cnpj, ativo) 
                VALUES (%s, %s, %s)
            """, (fornecedor_nome, '', True))
            fornecedores_map[fornecedor_nome] = cursor.lastrowid
        
        print(f"✅ {len(fornecedores_map)} fornecedores importados")
        
        # 3. Importar produtos
        print("\n📦 Importando produtos...")
        produtos_map = {}
        
        for i, item in enumerate(data, 1):
            try:
                # Mapear categoria
                categoria_id = categorias_map.get(item.get('categoria', 'Geral'), categorias_map['Geral'])
                
                # Mapear fornecedor
                fornecedor_id = fornecedores_map.get(item.get('fornecedor', 'Fornecedor Padrão'), fornecedores_map['Fornecedor Padrão'])
                
                # Extrair dados do produto
                nome = item.get('nome', f'Produto {i}')
                codigo = item.get('codigo', f'PROD{i:04d}')
                descricao = item.get('descricao', '')
                preco_custo = float(item.get('preco_custo', 0))
                preco_venda = float(item.get('preco_venda', preco_custo * 1.5))
                estoque_atual = int(item.get('estoque_atual', 0))
                estoque_minimo = int(item.get('estoque_minimo', 0))
                unidade = item.get('unidade', 'UN')
                
                cursor.execute("""
                    INSERT INTO estoque_produto 
                    (codigo, nome, descricao, categoria_id, fornecedor_id, 
                     preco_custo, preco_venda, estoque_atual, estoque_minimo, 
                     unidade, ativo, data_cadastro)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    codigo, nome, descricao, categoria_id, fornecedor_id,
                    preco_custo, preco_venda, estoque_atual, estoque_minimo,
                    unidade, True, datetime.now()
                ))
                
                produtos_map[codigo] = cursor.lastrowid
                
                if i % 10 == 0:
                    print(f"  📦 {i} produtos processados...")
                    
            except Exception as e:
                print(f"  ⚠️  Erro no produto {i}: {e}")
                continue
        
        print(f"✅ {len(produtos_map)} produtos importados")
        
        # 4. Criar movimentações de estoque baseadas nos dados
        print("\n🔄 Criando movimentações de estoque...")
        
        # Buscar usuário admin
        cursor.execute("SELECT id FROM auth_user WHERE username = 'admin' LIMIT 1")
        admin_user = cursor.fetchone()
        usuario_id = admin_user[0] if admin_user else None
        
        movimentacoes_criadas = 0
        for codigo, produto_id in produtos_map.items():
            try:
                # Buscar dados do produto
                cursor.execute("""
                    SELECT estoque_atual, nome FROM estoque_produto WHERE id = %s
                """, (produto_id,))
                produto_data = cursor.fetchone()
                
                if produto_data and produto_data[0] > 0:
                    # Criar movimentação de entrada
                    cursor.execute("""
                        INSERT INTO estoque_movimentacaoestoque 
                        (produto_id, tipo, quantidade, observacoes, usuario_id, data_movimentacao)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        produto_id, 'ENTRADA', produto_data[0], 
                        f'Importação inicial - {produto_data[1]}', 
                        usuario_id, datetime.now()
                    ))
                    movimentacoes_criadas += 1
                    
            except Exception as e:
                print(f"  ⚠️  Erro na movimentação do produto {codigo}: {e}")
                continue
        
        print(f"✅ {movimentacoes_criadas} movimentações criadas")
        
        connection.commit()
        
        # Estatísticas finais
        print("\n📊 ESTATÍSTICAS FINAIS")
        print("=" * 30)
        
        cursor.execute("SELECT COUNT(*) FROM estoque_categoria")
        cat_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM estoque_fornecedor")
        forn_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM estoque_produto")
        prod_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM estoque_movimentacaoestoque")
        mov_count = cursor.fetchone()[0]
        
        print(f"📂 Categorias: {cat_count}")
        print(f"🏢 Fornecedores: {forn_count}")
        print(f"📦 Produtos: {prod_count}")
        print(f"🔄 Movimentações: {mov_count}")
        
        cursor.close()
        connection.close()
        
        print("\n🎉 IMPORTAÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 50)
        print("📋 Próximos passos:")
        print("1. Execute: python manage.py runserver")
        print("2. Acesse: http://127.0.0.1:8000")
        print("3. Faça login com: admin / admin")
        print("4. Todos os dados estão no sistema!")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na importação: {e}")
        return False

if __name__ == "__main__":
    importar_dados()
