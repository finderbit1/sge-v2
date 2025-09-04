#!/usr/bin/env python3
"""
Configuração rápida para MySQL remoto
"""

def configurar_mysql_remoto():
    print("🌐 CONFIGURAÇÃO MYSQL REMOTO")
    print("=" * 40)
    print()
    
    # Obter informações do usuário
    host = input("URL do servidor MySQL: ").strip()
    port = input("Porta (padrão 3306): ").strip() or "3306"
    user = input("Usuário: ").strip()
    password = input("Senha: ").strip()
    database = input("Nome do banco (padrão sge_estoque): ").strip() or "sge_estoque"
    
    # Criar configuração
    config = f"""DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '{database}',
        'USER': '{user}',
        'PASSWORD': '{password}',
        'HOST': '{host}',
        'PORT': '{port}',
        'OPTIONS': {{
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        }},
    }}
}}"""
    
    print()
    print("📋 CONFIGURAÇÃO GERADA:")
    print("-" * 40)
    print(config)
    print()
    
    # Salvar em arquivo
    with open('config_mysql_gerada.py', 'w') as f:
        f.write(config)
    
    print("✅ Configuração salva em: config_mysql_gerada.py")
    print()
    print("📝 PRÓXIMOS PASSOS:")
    print("1. Copie a configuração acima")
    print("2. Cole no arquivo sge_sistema/settings.py")
    print("3. Substitua a seção DATABASES")
    print("4. Execute: python manage.py migrate")
    print("5. Execute: python manage.py createsuperuser")
    print("6. Execute: python manage.py runserver")

if __name__ == "__main__":
    configurar_mysql_remoto()

