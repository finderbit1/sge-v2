#!/usr/bin/env python3
"""
Script para configurar o sistema para usar MySQL
"""

import os
import sys
import subprocess
import getpass

def print_header():
    print("=" * 60)
    print("🔧 CONFIGURAÇÃO DO MYSQL - SISTEMA DE ESTOQUE")
    print("=" * 60)
    print()

def check_mysql_installed():
    """Verificar se o MySQL está instalado"""
    try:
        result = subprocess.run(['mysql', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ MySQL encontrado:", result.stdout.strip())
            return True
        else:
            print("❌ MySQL não encontrado")
            return False
    except FileNotFoundError:
        print("❌ MySQL não encontrado")
        return False

def install_mysql_client():
    """Instalar mysqlclient"""
    print("📦 Instalando mysqlclient...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'mysqlclient'], check=True)
        print("✅ mysqlclient instalado com sucesso")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar mysqlclient")
        print("💡 Tente instalar manualmente: pip install mysqlclient")
        return False

def get_mysql_credentials():
    """Obter credenciais do MySQL"""
    print("🔐 Configuração do MySQL")
    print("-" * 30)
    
    host = input("Host (padrão: localhost): ").strip() or "localhost"
    port = input("Porta (padrão: 3306): ").strip() or "3306"
    user = input("Usuário (padrão: root): ").strip() or "root"
    password = getpass.getpass("Senha do MySQL: ")
    database = input("Nome do banco (padrão: sge_estoque): ").strip() or "sge_estoque"
    
    return {
        'HOST': host,
        'PORT': port,
        'USER': user,
        'PASSWORD': password,
        'NAME': database
    }

def create_database(credentials):
    """Criar banco de dados"""
    print(f"🗄️ Criando banco de dados '{credentials['NAME']}'...")
    
    try:
        # Conectar ao MySQL e criar banco
        import pymysql
        
        connection = pymysql.connect(
            host=credentials['HOST'],
            port=int(credentials['PORT']),
            user=credentials['USER'],
            password=credentials['PASSWORD']
        )
        
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {credentials['NAME']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"✅ Banco de dados '{credentials['NAME']}' criado com sucesso")
        
        connection.close()
        return True
        
    except ImportError:
        print("❌ PyMySQL não encontrado. Instalando...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'pymysql'], check=True)
            return create_database(credentials)
        except subprocess.CalledProcessError:
            print("❌ Erro ao instalar PyMySQL")
            return False
    except Exception as e:
        print(f"❌ Erro ao criar banco de dados: {e}")
        return False

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

def run_migrations():
    """Executar migrações"""
    print("🔄 Executando migrações...")
    
    try:
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
        subprocess.run([sys.executable, 'manage.py', 'createsuperuser'], check=True)
        print("✅ Superusuário criado com sucesso")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao criar superusuário: {e}")
        return False

def main():
    print_header()
    
    # Verificar MySQL
    if not check_mysql_installed():
        print("💡 Instale o MySQL primeiro:")
        print("   Ubuntu/Debian: sudo apt install mysql-server")
        print("   CentOS/RHEL: sudo yum install mysql-server")
        print("   macOS: brew install mysql")
        return False
    
    # Instalar mysqlclient
    if not install_mysql_client():
        return False
    
    # Obter credenciais
    credentials = get_mysql_credentials()
    
    # Criar banco de dados
    if not create_database(credentials):
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
    print("🎉 CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!")
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

