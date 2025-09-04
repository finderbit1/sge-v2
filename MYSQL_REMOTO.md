# 🌐 Configuração MySQL Remoto - Sistema de Estoque

## ✨ **Configuração para Banco Remoto**

### 🎯 **Opções de Configuração**

#### **Opção 1: Script Automático (Recomendado)**
```bash
python config_remote_mysql.py
```

#### **Opção 2: Configuração Manual Rápida**
```bash
python configurar_mysql_remoto.py
```

#### **Opção 3: Editar Diretamente o settings.py**

### 🔧 **Configuração Manual**

#### **1. Editar settings.py**
```python
# sge_sistema/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sge_estoque',
        'USER': 'seu_usuario',
        'PASSWORD': 'sua_senha',
        'HOST': 'seu_servidor.com',  # URL do servidor remoto
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}
```

#### **2. Exemplos de Serviços de Banco Remoto**

##### **PlanetScale**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sge_estoque',
        'USER': 'abc123def456',
        'PASSWORD': 'pscale_pw_xyz789',
        'HOST': 'aws.connect.psdb.cloud',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
            'ssl': {'ca': '/path/to/ca-cert.pem'}
        },
    }
}
```

##### **AWS RDS**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sge_estoque',
        'USER': 'admin',
        'PASSWORD': 'sua_senha_aws',
        'HOST': 'sge-database.abc123.us-east-1.rds.amazonaws.com',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}
```

##### **Google Cloud SQL**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sge_estoque',
        'USER': 'root',
        'PASSWORD': 'sua_senha_gcp',
        'HOST': '35.123.456.789',  # IP público
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}
```

### 🚀 **Passos para Configuração**

#### **1. Obter Credenciais do Servidor**
- **Host**: URL ou IP do servidor MySQL
- **Porta**: Geralmente 3306
- **Usuário**: Nome do usuário do banco
- **Senha**: Senha do usuário
- **Banco**: Nome do banco de dados

#### **2. Configurar o Sistema**
```bash
# Opção 1: Script automático
python config_remote_mysql.py

# Opção 2: Configuração rápida
python configurar_mysql_remoto.py
```

#### **3. Executar Migrações**
```bash
# Criar tabelas no banco remoto
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver
```

### 🔍 **Teste de Conexão**

#### **Script de Teste**
```python
# test_connection.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sge_sistema.settings')
django.setup()

from django.db import connection

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print("✅ Conexão MySQL remota funcionando!")
        print(f"Resultado: {result}")
except Exception as e:
    print(f"❌ Erro na conexão: {e}")
```

### 🛠️ **Solução de Problemas**

#### **1. Erro de Conexão**
```
django.db.utils.OperationalError: (2003, "Can't connect to MySQL server")
```
**Soluções:**
- Verificar se o servidor está acessível
- Verificar firewall e portas
- Verificar credenciais

#### **2. Erro de SSL**
```
django.db.utils.OperationalError: (2026, 'SSL connection error')
```
**Solução:**
```python
'OPTIONS': {
    'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
    'charset': 'utf8mb4',
    'ssl_disabled': True,  # Desabilitar SSL se necessário
}
```

#### **3. Erro de Timeout**
```
django.db.utils.OperationalError: (2006, 'MySQL server has gone away')
```
**Solução:**
```python
'OPTIONS': {
    'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
    'charset': 'utf8mb4',
    'connect_timeout': 60,
    'read_timeout': 60,
    'write_timeout': 60,
}
```

### 📊 **Configurações Avançadas**

#### **1. Pool de Conexões**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sge_estoque',
        'USER': 'seu_usuario',
        'PASSWORD': 'sua_senha',
        'HOST': 'seu_servidor.com',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
        'CONN_MAX_AGE': 60,
        'CONN_HEALTH_CHECKS': True,
    }
}
```

#### **2. Configuração de Ambiente**
```python
# Usando variáveis de ambiente
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'sge_estoque'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}
```

### 🎯 **Serviços Recomendados**

#### **1. PlanetScale (Gratuito)**
- **URL**: https://planetscale.com
- **Gratuito**: 1GB de armazenamento
- **Vantagens**: Escalável, sem configuração de servidor

#### **2. AWS RDS (Pago)**
- **URL**: https://aws.amazon.com/rds
- **Vantagens**: Gerenciado pela AWS, alta disponibilidade

#### **3. Google Cloud SQL (Pago)**
- **URL**: https://cloud.google.com/sql
- **Vantagens**: Integração com Google Cloud

#### **4. Railway (Gratuito)**
- **URL**: https://railway.app
- **Gratuito**: 1GB de armazenamento
- **Vantagens**: Deploy fácil

### 🎉 **Resultado Final**

**O sistema está pronto para usar MySQL remoto!**

- ✅ **Configuração Automática**: Scripts para facilitar a configuração
- ✅ **Múltiplas Opções**: Scripts automáticos e configuração manual
- ✅ **Teste de Conexão**: Validação automática da conexão
- ✅ **Solução de Problemas**: Guias para resolver erros comuns
- ✅ **Documentação Completa**: Instruções detalhadas

**Agora você pode usar qualquer servidor MySQL remoto!** 🌐✨

### 🚀 **Próximos Passos**

1. **Configure**: Execute `python config_remote_mysql.py`
2. **Teste**: Verifique se a conexão está funcionando
3. **Migre**: Execute `python manage.py migrate`
4. **Crie usuário**: Execute `python manage.py createsuperuser`
5. **Inicie**: Execute `python manage.py runserver`
6. **Importe dados**: Execute `python importar_dados_silkart.py`

