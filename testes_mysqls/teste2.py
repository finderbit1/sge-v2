import pymysql

# Conectar ao MySQL
connection = pymysql.connect(
    host='estoquesilkart.mysql.uhserver.com',
    port=3306,
    user='mateusfinderbit',
    password='MJs119629@03770',
    database='estoquesilkart',
    charset='utf8mb4'
)

cursor = connection.cursor()

print('🔧 Recriando tabela estoque_produto com estrutura correta...')

# Dropar e recriar a tabela estoque_produto
cursor.execute('DROP TABLE IF EXISTS estoque_produto')

cursor.execute('''
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
''')

print('✅ Tabela estoque_produto recriada com sucesso!')

# Adicionar colunas que faltam nas outras tabelas
print('🔧 Adicionando colunas que faltam...')

try:
    cursor.execute('ALTER TABLE estoque_categoria ADD COLUMN ativa BOOLEAN DEFAULT TRUE')
    print('✅ Coluna ativa adicionada em estoque_categoria')
except:
    print('⚠️  Coluna ativa já existe em estoque_categoria')

try:
    cursor.execute('ALTER TABLE estoque_fornecedor ADD COLUMN ativo BOOLEAN DEFAULT TRUE')
    print('✅ Coluna ativo adicionada em estoque_fornecedor')
except:
    print('⚠️  Coluna ativo já existe em estoque_fornecedor')

connection.commit()
print('🎉 Estrutura das tabelas corrigida!')

cursor.close()
connection.close()
