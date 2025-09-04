#!/usr/bin/env python3
"""
Script para executar Django com MySQL 5.6 usando PyMySQL
"""

import os
import sys
import pymysql

# Configurar PyMySQL antes de importar Django
pymysql.install_as_MySQLdb()

# Configurar variáveis de ambiente
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sge_sistema.settings')

# Importar e configurar Django
import django
django.setup()

# Executar o servidor Django
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    execute_from_command_line(sys.argv)

