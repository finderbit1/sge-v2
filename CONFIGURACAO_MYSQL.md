# 🗄️ Configuração MySQL - Sistema de Estoque

## ✨ **Sistema Preparado para MySQL**

### 🎯 **Funcionalidades Implementadas**

#### **1. Configuração Automática**
- **Script de Instalação**: `install_mysql.sh` - Instalação completa automatizada
- **Configuração Interativa**: `setup_mysql.py` - Configuração passo a passo
- **Migração de Dados**: `migrate_to_mysql.py` - Migração do SQLite para MySQL

#### **2. Configurações do Banco**
- **Engine**: `django.db.backends.mysql`
- **Charset**: `utf8mb4` (suporte completo a Unicode)
- **SQL Mode**: `STRICT_TRANS_TABLES` (validação rigorosa)
- **Configurações Otimizadas**: Para performance e compatibilidade

#### **3. Dependências Instaladas**
- **mysqlclient**: Driver oficial do MySQL para Python
- **PyMySQL**: Driver alternativo (fallback)
- **openpyxl**: Para exportação Excel
- **reportlab**: Para geração de PDFs

### 🚀 **Instalação Rápida**

#### **Método 1: Script Automático (Recomendado)**
```bash
# Tornar executável e executar
chmod +x install_mysql.sh
./install_mysql.sh
```

#### **Método 2: Manual**
```bash
# 1. Instalar dependências do sistema
sudo apt update
sudo apt install python3-dev default-libmysqlclient-dev build-essential pkg-config

# 2. Instalar dependências Python
pip install -r requirements_mysql.txt

# 3. Configurar MySQL
python setup_mysql.py

# 4. Migrar dados (se necessário)
python migrate_to_mysql.py
```

### 🔧 **Configuração Manual**

#### **1. Instalar MySQL Server**
```bash
# Ubuntu/Debian
sudo apt install mysql-server

# CentOS/RHEL
sudo yum install mysql-server

# macOS
brew install mysql
```

#### **2. Configurar MySQL**
```bash
# Iniciar MySQL
sudo systemctl start mysql
sudo systemctl enable mysql

# Configurar segurança
sudo mysql_secure_installation

# Criar banco de dados
mysql -u root -p
CREATE DATABASE sge_estoque CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
GRANT ALL PRIVILEGES ON sge_estoque.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

#### **3. Configurar Django**
```python
# sge_sistema/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sge_estoque',
        'USER': 'root',
        'PASSWORD': 'sua_senha_mysql',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}
```

### 📊 **Migração de Dados**

#### **Do SQLite para MySQL**
```bash
# 1. Fazer backup do SQLite
cp db.sqlite3 backup_sqlite_$(date +%Y%m%d_%H%M%S).sqlite3

# 2. Executar migração
python migrate_to_mysql.py
```

#### **Processo de Migração**
1. **Backup Automático**: Cria backup do SQLite
2. **Exportação JSON**: Exporta todos os dados para JSON
3. **Importação MySQL**: Importa dados para MySQL
4. **Validação**: Verifica integridade dos dados

### 🎨 **Configurações Avançadas**

#### **1. Configuração de Performance**
```python
# settings.py - Otimizações para MySQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sge_estoque',
        'USER': 'root',
        'PASSWORD': 'sua_senha_mysql',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
            'autocommit': True,
            'sql_mode': 'traditional',
        },
        'CONN_MAX_AGE': 60,
        'CONN_HEALTH_CHECKS': True,
    }
}
```

#### **2. Configuração de Ambiente**
```python
# config_mysql.py
MYSQL_CONFIG = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'sge_estoque',
    'USER': 'root',
    'PASSWORD': 'sua_senha_mysql',
    'HOST': 'localhost',
    'PORT': '3306',
    'OPTIONS': {
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        'charset': 'utf8mb4',
    },
}
```

### 🔍 **Verificação e Testes**

#### **1. Testar Conexão**
```python
# test_mysql_connection.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sge_sistema.settings')
django.setup()

from django.db import connection

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print("✅ Conexão MySQL funcionando!")
        print(f"Resultado: {result}")
except Exception as e:
    print(f"❌ Erro na conexão: {e}")
```

#### **2. Verificar Dados**
```bash
# Executar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Verificar dados
python manage.py shell
>>> from estoque.models import Produto
>>> print(f"Produtos: {Produto.objects.count()}")
```

### 📋 **Scripts Disponíveis**

#### **1. install_mysql.sh**
- Instalação completa automatizada
- Verifica dependências
- Configura MySQL
- Executa migrações

#### **2. setup_mysql.py**
- Configuração interativa
- Criação do banco de dados
- Atualização das configurações
- Criação do superusuário

#### **3. migrate_to_mysql.py**
- Migração de dados do SQLite
- Backup automático
- Exportação/importação JSON
- Validação de integridade

### 🚨 **Solução de Problemas**

#### **1. Erro de Conexão**
```bash
# Verificar se MySQL está rodando
sudo systemctl status mysql

# Verificar porta
netstat -tlnp | grep 3306

# Testar conexão
mysql -u root -p -h localhost
```

#### **2. Erro de Permissões**
```sql
-- Conceder permissões
GRANT ALL PRIVILEGES ON sge_estoque.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
```

#### **3. Erro de Charset**
```sql
-- Verificar charset do banco
SHOW CREATE DATABASE sge_estoque;

-- Alterar se necessário
ALTER DATABASE sge_estoque CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 🎯 **Vantagens do MySQL**

#### **1. Performance**
- **Índices Otimizados**: Consultas mais rápidas
- **Cache de Consultas**: Melhor performance
- **Concorrência**: Múltiplos usuários simultâneos

#### **2. Escalabilidade**
- **Replicação**: Backup automático
- **Clustering**: Alta disponibilidade
- **Particionamento**: Dados grandes

#### **3. Recursos Avançados**
- **Triggers**: Automação de tarefas
- **Stored Procedures**: Lógica no banco
- **Views**: Consultas complexas

### 📊 **Monitoramento**

#### **1. Status do Banco**
```sql
-- Verificar status
SHOW STATUS;

-- Verificar processos
SHOW PROCESSLIST;

-- Verificar tabelas
SHOW TABLES;
```

#### **2. Performance**
```sql
-- Verificar consultas lentas
SHOW VARIABLES LIKE 'slow_query_log';

-- Verificar cache
SHOW STATUS LIKE 'Qcache%';
```

### 🎉 **Resultado Final**

**O sistema agora está preparado para MySQL!**

- ✅ **Configuração Automática**: Scripts de instalação e configuração
- ✅ **Migração de Dados**: Transferência segura do SQLite
- ✅ **Performance Otimizada**: Configurações para melhor performance
- ✅ **Backup Automático**: Proteção dos dados
- ✅ **Validação de Integridade**: Verificação de dados migrados
- ✅ **Documentação Completa**: Guias e soluções de problemas

**Agora você pode usar MySQL com todas as funcionalidades do sistema!** 🗄️✨

### 🚀 **Próximos Passos**

1. **Execute**: `./install_mysql.sh`
2. **Configure**: Siga as instruções do script
3. **Migre**: Execute `python migrate_to_mysql.py` se necessário
4. **Teste**: Acesse o sistema e verifique os dados
5. **Produção**: Configure para ambiente de produção

