#!/usr/bin/env python3
"""
Configurações para MySQL - Sistema de Estoque
"""

# Configurações do Banco de Dados MySQL
MYSQL_CONFIG = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'sge_estoque',
    'USER': 'root',
    'PASSWORD': 'sua_senha_mysql',  # Altere para sua senha do MySQL
    'HOST': 'localhost',
    'PORT': '3306',
    'OPTIONS': {
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        'charset': 'utf8mb4',
    },
}

# Configurações de Segurança
SECURITY_CONFIG = {
    'SECRET_KEY': 'sua_chave_secreta_aqui',  # Gere uma nova chave secreta
    'DEBUG': True,
    'ALLOWED_HOSTS': ['localhost', '127.0.0.1'],
}

# Configurações de Email (opcional)
EMAIL_CONFIG = {
    'EMAIL_HOST': 'smtp.gmail.com',
    'EMAIL_PORT': 587,
    'EMAIL_USE_TLS': True,
    'EMAIL_HOST_USER': 'seu_email@gmail.com',
    'EMAIL_HOST_PASSWORD': 'sua_senha_email',
}

# Instruções de uso:
"""
1. Instale o MySQL Server no seu sistema
2. Crie um banco de dados chamado 'sge_estoque'
3. Altere a senha do MySQL na configuração acima
4. Execute: pip install mysqlclient
5. Execute: python manage.py migrate
6. Execute: python manage.py createsuperuser
7. Execute: python manage.py runserver
"""

