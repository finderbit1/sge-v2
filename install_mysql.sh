#!/bin/bash

# Script de instalação para MySQL - Sistema de Estoque
# Execute: chmod +x install_mysql.sh && ./install_mysql.sh

echo "============================================================"
echo "🔧 INSTALAÇÃO MYSQL - SISTEMA DE ESTOQUE"
echo "============================================================"
echo

# Verificar se está no diretório correto
if [ ! -f "manage.py" ]; then
    echo "❌ Execute este script no diretório do projeto Django"
    exit 1
fi

# Verificar se o MySQL está instalado
echo "🔍 Verificando MySQL..."
if ! command -v mysql &> /dev/null; then
    echo "❌ MySQL não encontrado"
    echo "💡 Instale o MySQL primeiro:"
    echo "   Ubuntu/Debian: sudo apt install mysql-server"
    echo "   CentOS/RHEL: sudo yum install mysql-server"
    echo "   macOS: brew install mysql"
    exit 1
else
    echo "✅ MySQL encontrado"
fi

# Verificar se o Python está instalado
echo "🔍 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado"
    exit 1
else
    echo "✅ Python3 encontrado"
fi

# Verificar se o pip está instalado
echo "🔍 Verificando pip..."
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 não encontrado"
    exit 1
else
    echo "✅ pip3 encontrado"
fi

# Instalar dependências do sistema (Ubuntu/Debian)
echo "📦 Instalando dependências do sistema..."
if command -v apt &> /dev/null; then
    sudo apt update
    sudo apt install -y python3-dev default-libmysqlclient-dev build-essential pkg-config
    echo "✅ Dependências do sistema instaladas"
fi

# Instalar dependências Python
echo "📦 Instalando dependências Python..."
pip3 install -r requirements_mysql.txt

# Verificar se a instalação foi bem-sucedida
if [ $? -eq 0 ]; then
    echo "✅ Dependências Python instaladas com sucesso"
else
    echo "❌ Erro ao instalar dependências Python"
    exit 1
fi

# Executar script de configuração
echo "⚙️ Executando configuração do MySQL..."
python3 setup_mysql.py

# Verificar se a configuração foi bem-sucedida
if [ $? -eq 0 ]; then
    echo "✅ Configuração concluída com sucesso"
else
    echo "❌ Erro na configuração"
    exit 1
fi

echo
echo "🎉 INSTALAÇÃO CONCLUÍDA COM SUCESSO!"
echo "============================================================"
echo "📋 Próximos passos:"
echo "1. Execute: python3 manage.py runserver"
echo "2. Acesse: http://127.0.0.1:8000"
echo "3. Faça login com o superusuário criado"
echo "4. Importe os dados: python3 importar_dados_silkart.py"
echo "============================================================"

