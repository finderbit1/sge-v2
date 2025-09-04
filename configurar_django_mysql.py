#!/usr/bin/env python3
"""
Script para configurar Django para usar MySQL remoto diretamente
"""

import os
import sys
import pymysql

# Configurar PyMySQL antes de importar Django
pymysql.install_as_MySQLdb()

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sge_sistema.settings')

def testar_conexao_mysql():
    """Testar conexão direta com MySQL"""
    print("🔍 Testando conexão direta com MySQL...")
    
    try:
        connection = pymysql.connect(
            host='estoquesilkart.mysql.uhserver.com',
            port=3306,
            user='mateusfinderbit',
            password='MJs119629@03770',
            database='estoquesilkart',
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM estoque_produto")
            count = cursor.fetchone()[0]
            print(f"✅ Conexão MySQL funcionando! Produtos no banco: {count}")
        
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro na conexão MySQL: {e}")
        return False

def configurar_django_mysql():
    """Configurar Django para usar MySQL"""
    print("⚙️ Configurando Django para MySQL...")
    
    # Atualizar settings.py
    settings_file = "sge_sistema/settings.py"
    
    try:
        with open(settings_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Substituir configuração do banco
        old_db_config = """DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}"""
        
        new_db_config = """DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'estoquesilkart',
        'USER': 'mateusfinderbit',
        'PASSWORD': 'MJs119629@03770',
        'HOST': 'estoquesilkart.mysql.uhserver.com',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
            'use_unicode': True,
        },
    }
}"""
        
        content = content.replace(old_db_config, new_db_config)
        
        with open(settings_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Configuração do Django atualizada para MySQL")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao atualizar configurações: {e}")
        return False

def testar_django_mysql():
    """Testar Django com MySQL"""
    print("🧪 Testando Django com MySQL...")
    
    try:
        import django
        django.setup()
        
        from django.db import connection
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM estoque_produto")
            count = cursor.fetchone()[0]
            print(f"✅ Django conectado ao MySQL! Produtos: {count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no Django com MySQL: {e}")
        return False

def main():
    print("🚀 CONFIGURAÇÃO DJANGO + MYSQL REMOTO")
    print("=" * 50)
    
    # Testar conexão direta
    if not testar_conexao_mysql():
        return False
    
    # Configurar Django
    if not configurar_django_mysql():
        return False
    
    # Testar Django
    if not testar_django_mysql():
        return False
    
    print("=" * 50)
    print("🎉 CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!")
    print("📋 Próximos passos:")
    print("1. Execute: python manage.py runserver")
    print("2. Acesse: http://127.0.0.1:8000")
    print("3. Faça login com: admin / admin")
    print("4. Todos os dados já estão no MySQL remoto!")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    main()

