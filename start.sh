#!/bin/bash

echo "🚀 Iniciando Sistema de Gerenciamento de Estoque (SGE)"
echo "=================================================="

# Verificar se o ambiente virtual está ativo
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Ambiente virtual ativo: $VIRTUAL_ENV"
else
    echo "⚠️  Ambiente virtual não detectado. Execute: uv sync"
fi

# Verificar se as migrações estão aplicadas
echo "📊 Verificando migrações..."
uv run python manage.py showmigrations --plan | grep -q "\[ \]"
if [ $? -eq 0 ]; then
    echo "🔄 Aplicando migrações pendentes..."
    uv run python manage.py migrate
else
    echo "✅ Migrações já aplicadas"
fi

# Verificar se existe superusuário
echo "👤 Verificando superusuário..."
uv run python manage.py shell -c "
from django.contrib.auth.models import User
if User.objects.filter(is_superuser=True).exists():
    print('✅ Superusuário encontrado')
else:
    print('⚠️  Nenhum superusuário encontrado')
    print('Execute: uv run python manage.py createsuperuser')
"

echo ""
echo "🌐 Iniciando servidor de desenvolvimento..."
echo "📍 Acesse: http://127.0.0.1:8000"
echo "🔧 Admin: http://127.0.0.1:8000/admin"
echo ""
echo "Pressione Ctrl+C para parar o servidor"
echo "=================================================="

# Iniciar o servidor
uv run python manage.py runserver
