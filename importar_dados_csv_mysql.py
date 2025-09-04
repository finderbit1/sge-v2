#!/usr/bin/env python3
"""
Script para importar dados do estoquesilkart.csv para MySQL
"""

import csv
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

def importar_dados_csv():
    """Importar dados do CSV para MySQL"""
    
    print("📥 IMPORTANDO DADOS DO ESTOQUESILKART.CSV")
    print("=" * 50)
    
    try:
        # Conectar ao MySQL
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("✅ Conectado ao MySQL remoto!")
        
        # Ler arquivo CSV
        print("\n📖 Lendo arquivo estoquesilkart.csv...")
        
        with open('estoquesilkart.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        
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
        
        # Categorias do CSV
        categorias_unicas = set()
        for item in data:
            if 'categoria' in item and item['categoria'] and item['categoria'].strip():
                categorias_unicas.add(item['categoria'].strip())
        
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
        
        # Fornecedores do CSV
        fornecedores_unicos = set()
        for item in data:
            if 'fornecedor' in item and item['fornecedor'] and item['fornecedor'].strip():
                fornecedores_unicos.add(item['fornecedor'].strip())
        
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
                categoria_nome = item.get('categoria', '').strip() or 'Geral'
                categoria_id = categorias_map.get(categoria_nome, categorias_map['Geral'])
                
                # Mapear fornecedor
                fornecedor_nome = item.get('fornecedor', '').strip() or 'Fornecedor Padrão'
                fornecedor_id = fornecedores_map.get(fornecedor_nome, fornecedores_map['Fornecedor Padrão'])
                
                # Extrair dados do produto
                nome = item.get('nome', f'Produto {i}').strip()
                codigo = item.get('codigo', f'PROD{i:04d}').strip()
                descricao = item.get('descricao', '').strip()
                
                # Converter preços
                try:
                    preco_custo = float(item.get('preco_custo', 0).replace(',', '.'))
                except:
                    preco_custo = 0.0
                
                try:
                    preco_venda = float(item.get('preco_venda', preco_custo * 1.5).replace(',', '.'))
                except:
                    preco_venda = preco_custo * 1.5 if preco_custo > 0 else 0.0
                
                # Converter estoque
                try:
                    estoque_atual = int(float(item.get('estoque_atual', 0)))
                except:
                    estoque_atual = 0
                
                try:
                    estoque_minimo = int(float(item.get('estoque_minimo', 0)))
                except:
                    estoque_minimo = 0
                
                unidade = item.get('unidade', 'UN').strip() or 'UN'
                
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
                
                if i % 50 == 0:
                    print(f"  📦 {i} produtos processados...")
                    
            except Exception as e:
                print(f"  ⚠️  Erro no produto {i} ({item.get('nome', 'N/A')}): {e}")
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
    importar_dados_csv()
