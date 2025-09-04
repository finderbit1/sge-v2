#!/usr/bin/env python3
"""
Script para configurar MySQL remoto - Sistema de Estoque
"""

import os
import sys

def print_header():
    print("=" * 60)
    print("🌐 CONFIGURAÇÃO MYSQL REMOTO - SISTEMA DE ESTOQUE")
    print("=" * 60)
    print()

def get_remote_credentials():
    """Obter credenciais do MySQL remoto"""
    print("🔐 Configuração do MySQL Remoto")
    print("-" * 40)
    
    host = input("URL do servidor MySQL (ex: mysql.exemplo.com): ").strip()
    if not host:
        print("❌ URL do servidor é obrigatória")
        return None
    
    port = input("Porta (padrão: 3306): ").strip() or "3306"
    user = input("Usuário do MySQL: ").strip()
    if not user:
        print("❌ Usuário é obrigatório")
        return None
    
    password = input("Senha do MySQL: ").strip()
    if not password:
        print("❌ Senha é obrigatória")
        return None
    
    database = input("Nome do banco (padrão: sge_estoque): ").strip() or "sge_estoque"
    
    return {
        'HOST': host,
        'PORT': port,
        'USER': user,
        'PASSWORD': password,
        'NAME': database
    }

def update_settings(credentials):
    """Atualizar arquivo settings.py"""
    print("⚙️ Atualizando configurações...")
    
    settings_file = "sge_sistema/settings.py"
    
    try:
        with open(settings_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Substituir configuração do banco
        old_db_config = """DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sge_estoque',  # Nome do banco de dados
        'USER': 'seu_usuario',  # Usuário do MySQL
        'PASSWORD': 'sua_senha',  # Senha do MySQL
        'HOST': 'seu_host_remoto',  # URL do servidor remoto
        'PORT': '3306',  # Porta do MySQL (geralmente 3306)
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}"""
        
        new_db_config = f"""DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '{credentials['NAME']}',
        'USER': '{credentials['USER']}',
        'PASSWORD': '{credentials['PASSWORD']}',
        'HOST': '{credentials['HOST']}',
        'PORT': '{credentials['PORT']}',
        'OPTIONS': {{
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        }},
    }}
}}"""
        
        content = content.replace(old_db_config, new_db_config)
        
        with open(settings_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Configurações atualizadas com sucesso")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao atualizar configurações: {e}")
        return False

def test_connection(credentials):
    """Testar conexão com o banco remoto"""
    print("🔍 Testando conexão com o banco remoto...")
    
    try:
        import pymysql
        
        connection = pymysql.connect(
            host=credentials['HOST'],
            port=int(credentials['PORT']),
            user=credentials['USER'],
            password=credentials['PASSWORD'],
            database=credentials['NAME']
        )
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print("✅ Conexão com MySQL remoto funcionando!")
            print(f"Servidor: {credentials['HOST']}:{credentials['PORT']}")
            print(f"Banco: {credentials['NAME']}")
        
        connection.close()
        return True
        
    except ImportError:
        print("📦 Instalando PyMySQL...")
        try:
            import subprocess
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'pymysql'], check=True)
            return test_connection(credentials)
        except subprocess.CalledProcessError:
            print("❌ Erro ao instalar PyMySQL")
            return False
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        print("💡 Verifique se:")
        print("  - O servidor MySQL está acessível")
        print("  - As credenciais estão corretas")
        print("  - O banco de dados existe")
        print("  - O usuário tem permissões adequadas")
        return False

def run_migrations():
    """Executar migrações"""
    print("🔄 Executando migrações...")
    
    try:
        import subprocess
        subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
        print("✅ Migrações executadas com sucesso")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar migrações: {e}")
        return False

def create_superuser():
    """Criar superusuário"""
    print("👤 Criando superusuário...")
    
    try:
        import subprocess
        subprocess.run([sys.executable, 'manage.py', 'createsuperuser'], check=True)
        print("✅ Superusuário criado com sucesso")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao criar superusuário: {e}")
        return False

def main():
    print_header()
    
    # Obter credenciais
    credentials = get_remote_credentials()
    if not credentials:
        return False
    
    # Testar conexão
    if not test_connection(credentials):
        return False
    
    # Atualizar configurações
    if not update_settings(credentials):
        return False
    
    # Executar migrações
    if not run_migrations():
        return False
    
    # Criar superusuário
    create_superuser()
    
    print()
    print("🎉 CONFIGURAÇÃO REMOTA CONCLUÍDA COM SUCESSO!")
    print("=" * 60)
    print("📋 Próximos passos:")
    print("1. Execute: python manage.py runserver")
    print("2. Acesse: http://127.0.0.1:8000")
    print("3. Faça login com o superusuário criado")
    print("4. Importe os dados: python importar_dados_silkart.py")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    main()

