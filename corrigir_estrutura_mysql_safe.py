#!/usr/bin/env python3
"""
Script para corrigir a estrutura das tabelas MySQL de forma segura
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

def corrigir_estrutura_safe():
    """Corrigir estrutura de todas as tabelas de forma segura"""
    
    print("🔧 CORRIGINDO ESTRUTURA DAS TABELAS MYSQL (MODO SEGURO)")
    print("=" * 60)
    
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("✅ Conectado ao MySQL remoto!")
        
        # Desabilitar verificações de chave estrangeira
        print("\n🔓 Desabilitando verificações de chave estrangeira...")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        # 1. Limpar e recriar tabelas em ordem inversa (filhas primeiro)
        print("\n🗑️ Removendo tabelas existentes...")
        
        tabelas_para_remover = [
            'estoque_itemvenda',
            'estoque_movimentacaoestoque', 
            'estoque_venda',
            'estoque_produto',
            'estoque_fornecedor',
            'estoque_categoria'
        ]
        
        for tabela in tabelas_para_remover:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {tabela}")
                print(f"  ✅ {tabela} removida")
            except Exception as e:
                print(f"  ⚠️  {tabela}: {e}")
        
        # 2. Recriar tabelas na ordem correta (pais primeiro)
        print("\n🏗️ Criando tabelas com estrutura correta...")
        
        # Categoria (sem dependências)
        print("📂 Criando estoque_categoria...")
        cursor.execute("""
            CREATE TABLE estoque_categoria (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL UNIQUE,
                descricao TEXT,
                ativa BOOLEAN NOT NULL DEFAULT TRUE,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        print("  ✅ estoque_categoria criada")
        
        # Fornecedor (sem dependências)
        print("🏢 Criando estoque_fornecedor...")
        cursor.execute("""
            CREATE TABLE estoque_fornecedor (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(200) NOT NULL,
                cnpj VARCHAR(18) UNIQUE,
                endereco TEXT,
                telefone VARCHAR(20),
                email VARCHAR(100),
                contato VARCHAR(100),
                ativo BOOLEAN NOT NULL DEFAULT TRUE,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        print("  ✅ estoque_fornecedor criada")
        
        # Produto (depende de categoria e fornecedor)
        print("📦 Criando estoque_produto...")
        cursor.execute("""
            CREATE TABLE estoque_produto (
                id INT AUTO_INCREMENT PRIMARY KEY,
                codigo VARCHAR(50) NOT NULL UNIQUE,
                nome VARCHAR(200) NOT NULL,
                descricao TEXT,
                categoria_id INT,
                fornecedor_id INT,
                preco_custo DECIMAL(10,2) NOT NULL,
                preco_venda DECIMAL(10,2) NOT NULL,
                estoque_minimo INT NOT NULL DEFAULT 0,
                estoque_atual INT NOT NULL DEFAULT 0,
                unidade VARCHAR(2) NOT NULL DEFAULT 'UN',
                ativo BOOLEAN NOT NULL DEFAULT TRUE,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (categoria_id) REFERENCES estoque_categoria(id) ON DELETE SET NULL,
                FOREIGN KEY (fornecedor_id) REFERENCES estoque_fornecedor(id) ON DELETE SET NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        print("  ✅ estoque_produto criada")
        
        # Movimentação (depende de produto e usuário)
        print("🔄 Criando estoque_movimentacaoestoque...")
        cursor.execute("""
            CREATE TABLE estoque_movimentacaoestoque (
                id INT AUTO_INCREMENT PRIMARY KEY,
                produto_id INT NOT NULL,
                tipo VARCHAR(15) NOT NULL,
                quantidade INT NOT NULL,
                observacoes TEXT,
                usuario_id INT,
                data_movimentacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                destino VARCHAR(200),
                FOREIGN KEY (produto_id) REFERENCES estoque_produto(id) ON DELETE CASCADE,
                FOREIGN KEY (usuario_id) REFERENCES auth_user(id) ON DELETE SET NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        print("  ✅ estoque_movimentacaoestoque criada")
        
        # Venda (depende de usuário)
        print("💰 Criando estoque_venda...")
        cursor.execute("""
            CREATE TABLE estoque_venda (
                id INT AUTO_INCREMENT PRIMARY KEY,
                numero_venda VARCHAR(20) NOT NULL UNIQUE,
                cliente VARCHAR(200) NOT NULL,
                data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(15) NOT NULL DEFAULT 'PENDENTE',
                total DECIMAL(10,2) NOT NULL DEFAULT 0,
                desconto DECIMAL(10,2) NOT NULL DEFAULT 0,
                vendedor_id INT,
                observacoes TEXT,
                FOREIGN KEY (vendedor_id) REFERENCES auth_user(id) ON DELETE SET NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        print("  ✅ estoque_venda criada")
        
        # Item Venda (depende de venda e produto)
        print("🛒 Criando estoque_itemvenda...")
        cursor.execute("""
            CREATE TABLE estoque_itemvenda (
                id INT AUTO_INCREMENT PRIMARY KEY,
                venda_id INT NOT NULL,
                produto_id INT NOT NULL,
                quantidade INT NOT NULL,
                preco_unitario DECIMAL(10,2) NOT NULL,
                subtotal DECIMAL(10,2) NOT NULL,
                FOREIGN KEY (venda_id) REFERENCES estoque_venda(id) ON DELETE CASCADE,
                FOREIGN KEY (produto_id) REFERENCES estoque_produto(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        print("  ✅ estoque_itemvenda criada")
        
        # Reabilitar verificações de chave estrangeira
        print("\n🔒 Reabilitando verificações de chave estrangeira...")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        # Inserir dados iniciais
        print("\n🌱 Inserindo dados iniciais...")
        
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
        print("✅ Dados iniciais inseridos")
        
        # Verificar tabelas criadas
        cursor.execute("SHOW TABLES LIKE 'estoque_%'")
        tabelas = cursor.fetchall()
        
        print(f"\n📊 Tabelas do sistema criadas: {len(tabelas)}")
        for tabela in tabelas:
            print(f"  - {tabela[0]}")
        
        cursor.close()
        connection.close()
        
        print("\n🎉 ESTRUTURA CORRIGIDA COM SUCESSO!")
        print("=" * 60)
        print("📋 Próximos passos:")
        print("1. Execute: python manage.py runserver")
        print("2. Acesse: http://127.0.0.1:8000")
        print("3. Faça login com: admin / admin")
        print("4. Importe os dados: python importar_dados_silkart.py")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao corrigir estrutura: {e}")
        return False

if __name__ == "__main__":
    corrigir_estrutura_safe()
