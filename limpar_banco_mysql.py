#!/usr/bin/env python3
"""
Script para limpar todos os dados do banco MySQL
"""

import pymysql

# Configurações do banco
DB_CONFIG = {
    'host': 'estoquesilkart.mysql.uhserver.com',
    'port': 3306,
    'user': 'mateusfinderbit',
    'password': 'MJs119629@03770',
    'database': 'estoquesilkart',
    'charset': 'utf8mb4'
}

def limpar_banco():
    """Limpar todos os dados do banco"""
    
    print("🗑️ LIMPANDO BANCO DE DADOS MYSQL")
    print("=" * 40)
    
    try:
        # Conectar ao MySQL
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("✅ Conectado ao MySQL remoto!")
        
        # Desabilitar verificações de chave estrangeira
        print("\n🔓 Desabilitando verificações de chave estrangeira...")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        # Limpar todas as tabelas do sistema
        print("\n🧹 Limpando tabelas do sistema...")
        
        tabelas_para_limpar = [
            'estoque_itemvenda',
            'estoque_movimentacaoestoque', 
            'estoque_venda',
            'estoque_produto',
            'estoque_fornecedor',
            'estoque_categoria'
        ]
        
        for tabela in tabelas_para_limpar:
            try:
                cursor.execute(f"DELETE FROM {tabela}")
                print(f"  ✅ {tabela} limpa")
            except Exception as e:
                print(f"  ⚠️  {tabela}: {e}")
        
        # Reabilitar verificações de chave estrangeira
        print("\n🔒 Reabilitando verificações de chave estrangeira...")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        # Inserir dados iniciais básicos
        print("\n🌱 Inserindo dados iniciais básicos...")
        
        # Categoria padrão
        cursor.execute("""
            INSERT INTO estoque_categoria (nome, descricao, ativa) 
            VALUES ('Geral', 'Categoria padrão para produtos sem categoria específica', TRUE)
        """)
        print("  ✅ Categoria padrão inserida")
        
        # Fornecedor padrão
        cursor.execute("""
            INSERT INTO estoque_fornecedor (nome, cnpj, ativo) 
            VALUES ('Fornecedor Padrão', '00.000.000/0001-00', TRUE)
        """)
        print("  ✅ Fornecedor padrão inserido")
        
        connection.commit()
        
        # Verificar estado final
        print("\n📊 ESTADO FINAL DO BANCO")
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
        
        print("\n🎉 BANCO LIMPO COM SUCESSO!")
        print("=" * 40)
        print("📋 Próximos passos:")
        print("1. Execute: python manage.py runserver")
        print("2. Acesse: http://127.0.0.1:8000")
        print("3. Faça login com: admin / admin")
        print("4. Insira os dados manualmente pelo sistema!")
        print("=" * 40)
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao limpar banco: {e}")
        return False

if __name__ == "__main__":
    limpar_banco()
