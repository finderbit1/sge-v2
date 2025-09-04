
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

# Verificar estrutura da tabela estoque_produto
print('📋 Estrutura atual da tabela estoque_produto:')
cursor.execute('DESCRIBE estoque_produto')
for row in cursor.fetchall():
    print(f'  {row[0]} - {row[1]}')

print()

# Adicionar coluna ativo no final da tabela
print('🔧 Adicionando coluna ativo na tabela estoque_produto...')
cursor.execute('ALTER TABLE estoque_produto ADD COLUMN ativo BOOLEAN DEFAULT TRUE')

# Adicionar coluna ativa na tabela estoque_categoria
print('🔧 Adicionando coluna ativa na tabela estoque_categoria...')
cursor.execute('ALTER TABLE estoque_categoria ADD COLUMN ativa BOOLEAN DEFAULT TRUE')

# Adicionar coluna ativo na tabela estoque_fornecedor
print('🔧 Adicionando coluna ativo na tabela estoque_fornecedor...')
cursor.execute('ALTER TABLE estoque_fornecedor ADD COLUMN ativo BOOLEAN DEFAULT TRUE')

connection.commit()
print('✅ Colunas adicionadas com sucesso!')

cursor.close()
connection.close()
