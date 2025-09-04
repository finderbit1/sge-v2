#!/bin/bash

# Script para iniciar o sistema com MySQL remoto
echo "🚀 INICIANDO SISTEMA DE ESTOQUE COM MYSQL REMOTO"
echo "================================================"

# Ativar ambiente virtual
echo "📦 Ativando ambiente virtual..."
source .venv/bin/activate

# Configurar PyMySQL
echo "🔧 Configurando PyMySQL para MySQL 5.6..."
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Executar Django com MySQL
echo "🌐 Iniciando servidor Django..."
echo "📊 Banco de dados: MySQL remoto (estoquesilkart.mysql.uhserver.com)"
echo "👤 Usuário: mateusfinderbit"
echo "🔗 URL: http://127.0.0.1:8000"
echo ""

# Executar o servidor
python run_django_mysql.py runserver 0.0.0.0:8000

