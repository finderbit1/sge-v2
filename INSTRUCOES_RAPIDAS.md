# 🚀 Instruções Rápidas - Sistema de Estoque

## ✅ Sistema Funcionando!

O sistema está rodando em: **http://127.0.0.1:8000**

### 🔑 **Credenciais de Acesso:**
- **Usuário:** admin
- **Senha:** (a que você criou)

## 📋 **Primeiros Passos:**

### 1. **Acesse o Sistema**
- Abra: http://127.0.0.1:8000
- Faça login com as credenciais acima

### 2. **Configure Dados Básicos (Admin)**
- Acesse: http://127.0.0.1:8000/admin
- **Crie Categorias:**
  - Clique em "Categorias" → "Adicionar"
  - Exemplo: Eletrônicos, Roupas, Alimentos, etc.

- **Cadastre Fornecedores:**
  - Clique em "Fornecedores" → "Adicionar"
  - Preencha: Nome, CNPJ, Endereço, Telefone, Email

### 3. **Adicione Produtos**
- Volte para o sistema principal
- Clique em "Produtos" → "Adicionar Produto"
- Preencha todas as informações necessárias

### 4. **Teste as Funcionalidades**
- **Movimentações:** Adicione/remova estoque
- **Vendas:** Crie uma venda de teste
- **Dashboard:** Veja as estatísticas

## 🎯 **Funcionalidades Principais:**

### 📦 **Gestão de Produtos**
- ✅ Cadastro completo
- ✅ Categorização
- ✅ Controle de preços
- ✅ Gestão de estoque

### 📊 **Movimentações**
- ✅ Entrada de produtos
- ✅ Saída de produtos
- ✅ Ajustes de inventário
- ✅ Histórico completo

### 💰 **Vendas**
- ✅ Criação de vendas
- ✅ Múltiplos itens
- ✅ Cálculo automático
- ✅ Integração com estoque

### 📈 **Dashboard**
- ✅ Estatísticas em tempo real
- ✅ Alertas de estoque
- ✅ Gráficos e relatórios

## 🔧 **Comandos Úteis:**

```bash
# Parar o servidor
Ctrl + C

# Reiniciar o servidor
uv run python manage.py runserver

# Criar novo superusuário
uv run python manage.py createsuperuser

# Aplicar migrações
uv run python manage.py migrate
```

## 🆘 **Solução de Problemas:**

### Se não conseguir acessar:
1. Verifique se o servidor está rodando
2. Confirme as credenciais
3. Acesse o admin primeiro: http://127.0.0.1:8000/admin

### Se houver erro de banco:
```bash
uv run python manage.py migrate
```

### Para resetar tudo:
```bash
rm db.sqlite3
uv run python manage.py migrate
uv run python manage.py createsuperuser
```

## 🎉 **Pronto para Usar!**

O sistema está completamente funcional com:
- ✅ Interface moderna e responsiva
- ✅ Autenticação segura
- ✅ Todas as funcionalidades de estoque
- ✅ Dashboard com estatísticas
- ✅ Sistema de vendas integrado

**Divirta-se gerenciando seu estoque!** 🚀
