#!/usr/bin/env python3
"""
Script para forçar o uso do PyMySQL com MySQL 5.6
"""

import os
import sys

# Adicionar o diretório do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configurar PyMySQL antes de importar Django
import pymysql
pymysql.install_as_MySQLdb()

# Configurar variáveis de ambiente
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sge_sistema.settings')

# Importar e configurar Django
import django
django.setup()

# Agora executar o comando Django
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    execute_from_command_line(sys.argv)

