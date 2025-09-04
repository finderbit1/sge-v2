#!/usr/bin/env python3
"""
Script para criar tabelas diretamente no MySQL 5.6 usando PyMySQL
"""

import pymysql
import os
import sys

# Configurações do banco
DB_CONFIG = {
    'host': 'estoquesilkart.mysql.uhserver.com',
    'port': 3306,
    'user': 'mateusfinderbit',
    'password': 'MJs119629@03770',
    'database': 'estoquesilkart',
    'charset': 'utf8mb4'
}

def criar_tabelas():
    """Criar todas as tabelas do sistema de estoque"""
    
    print("🔧 Conectando ao MySQL remoto...")
    
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print("✅ Conectado ao MySQL remoto!")
        
        # SQL para criar as tabelas
        tabelas_sql = [
            # Tabela de categorias
            """
            CREATE TABLE IF NOT EXISTS estoque_categoria (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                descricao TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            
            # Tabela de fornecedores
            """
            CREATE TABLE IF NOT EXISTS estoque_fornecedor (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(200) NOT NULL,
                cnpj VARCHAR(18) UNIQUE,
                endereco TEXT,
                telefone VARCHAR(20),
                email VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            
            # Tabela de produtos
            """
            CREATE TABLE IF NOT EXISTS estoque_produto (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(200) NOT NULL,
                descricao TEXT,
                preco_custo DECIMAL(10,2) NOT NULL,
                preco_venda DECIMAL(10,2) NOT NULL,
                estoque_atual INT NOT NULL DEFAULT 0,
                estoque_minimo INT NOT NULL DEFAULT 0,
                categoria_id INT,
                fornecedor_id INT,
                codigo_barras VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (categoria_id) REFERENCES estoque_categoria(id) ON DELETE SET NULL,
                FOREIGN KEY (fornecedor_id) REFERENCES estoque_fornecedor(id) ON DELETE SET NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            
            # Tabela de movimentações de estoque
            """
            CREATE TABLE IF NOT EXISTS estoque_movimentacaoestoque (
                id INT AUTO_INCREMENT PRIMARY KEY,
                produto_id INT NOT NULL,
                tipo VARCHAR(10) NOT NULL,
                quantidade INT NOT NULL,
                destino VARCHAR(200),
                observacoes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (produto_id) REFERENCES estoque_produto(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            
            # Tabela de vendas
            """
            CREATE TABLE IF NOT EXISTS estoque_venda (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cliente_nome VARCHAR(200),
                cliente_cpf VARCHAR(14),
                valor_total DECIMAL(10,2) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            
            # Tabela de itens de venda
            """
            CREATE TABLE IF NOT EXISTS estoque_itemvenda (
                id INT AUTO_INCREMENT PRIMARY KEY,
                venda_id INT NOT NULL,
                produto_id INT NOT NULL,
                quantidade INT NOT NULL,
                preco_unitario DECIMAL(10,2) NOT NULL,
                subtotal DECIMAL(10,2) NOT NULL,
                FOREIGN KEY (venda_id) REFERENCES estoque_venda(id) ON DELETE CASCADE,
                FOREIGN KEY (produto_id) REFERENCES estoque_produto(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            
            # Tabela de usuários (Django auth)
            """
            CREATE TABLE IF NOT EXISTS auth_user (
                id INT AUTO_INCREMENT PRIMARY KEY,
                password VARCHAR(128) NOT NULL,
                last_login TIMESTAMP NULL,
                is_superuser BOOLEAN NOT NULL,
                username VARCHAR(150) NOT NULL UNIQUE,
                first_name VARCHAR(150) NOT NULL,
                last_name VARCHAR(150) NOT NULL,
                email VARCHAR(254) NOT NULL,
                is_staff BOOLEAN NOT NULL,
                is_active BOOLEAN NOT NULL,
                date_joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            
            # Tabela de sessões (Django sessions)
            """
            CREATE TABLE IF NOT EXISTS django_session (
                session_key VARCHAR(40) NOT NULL PRIMARY KEY,
                session_data LONGTEXT NOT NULL,
                expire_date TIMESTAMP NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            
            # Tabela de migrações (Django migrations)
            """
            CREATE TABLE IF NOT EXISTS django_migrations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                app VARCHAR(255) NOT NULL,
                name VARCHAR(255) NOT NULL,
                applied TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
        ]
        
        print("📋 Criando tabelas...")
        
        for i, sql in enumerate(tabelas_sql, 1):
            try:
                cursor.execute(sql)
                print(f"✅ Tabela {i}/{len(tabelas_sql)} criada com sucesso")
            except Exception as e:
                print(f"⚠️  Erro na tabela {i}: {e}")
        
        # Inserir dados iniciais
        print("🌱 Inserindo dados iniciais...")
        
        # Criar superusuário
        cursor.execute("""
            INSERT IGNORE INTO auth_user 
            (password, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
            VALUES 
            ('pbkdf2_sha256$600000$dummy$dummy', 1, 'admin', 'Admin', 'Sistema', 'admin@estoque.com', 1, 1, NOW())
        """)
        
        # Inserir categoria padrão
        cursor.execute("""
            INSERT IGNORE INTO estoque_categoria (nome, descricao) 
            VALUES ('Geral', 'Categoria padrão para produtos sem categoria específica')
        """)
        
        # Inserir fornecedor padrão
        cursor.execute("""
            INSERT IGNORE INTO estoque_fornecedor (nome, cnpj) 
            VALUES ('Fornecedor Padrão', '00.000.000/0001-00')
        """)
        
        connection.commit()
        print("✅ Dados iniciais inseridos com sucesso!")
        
        # Verificar tabelas criadas
        cursor.execute("SHOW TABLES")
        tabelas = cursor.fetchall()
        
        print(f"\n📊 Total de tabelas criadas: {len(tabelas)}")
        for tabela in tabelas:
            print(f"  - {tabela[0]}")
        
        cursor.close()
        connection.close()
        
        print("\n🎉 CONFIGURAÇÃO MYSQL CONCLUÍDA COM SUCESSO!")
        print("=" * 60)
        print("📋 Próximos passos:")
        print("1. Execute: python manage.py runserver")
        print("2. Acesse: http://127.0.0.1:8000")
        print("3. Faça login com: admin / admin")
        print("4. Importe os dados: python importar_dados_silkart.py")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False

if __name__ == "__main__":
    criar_tabelas()

