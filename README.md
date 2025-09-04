# Sistema de Gerenciamento de Estoque (SGE)

Um sistema completo de gerenciamento de estoque desenvolvido em Django com interface moderna e funcionalidades avançadas.

## 🚀 Funcionalidades

### 📦 Gestão de Produtos
- Cadastro completo de produtos com códigos únicos
- Categorização e organização por fornecedores
- Controle de preços (custo e venda)
- Gestão de unidades de medida
- Controle de estoque mínimo e atual
- Cálculo automático de margem de lucro

### 🏢 Gestão de Fornecedores
- Cadastro de fornecedores com dados completos
- Controle de CNPJ e informações de contato
- Histórico de relacionamento

### 📊 Controle de Estoque
- Movimentações de entrada e saída
- Ajustes de estoque
- Transferências entre locais
- Histórico completo de movimentações
- Alertas de estoque baixo

### 💰 Sistema de Vendas
- Criação de vendas com múltiplos itens
- Cálculo automático de totais e descontos
- Integração com movimentações de estoque
- Numeração automática de vendas

### 📈 Dashboard e Relatórios
- Visão geral do sistema
- Estatísticas em tempo real
- Gráficos de performance
- Alertas de estoque
- Relatórios detalhados

## 🛠️ Tecnologias Utilizadas

- **Backend**: Django 5.2.6
- **Frontend**: Bootstrap 5.3, HTML5, CSS3, JavaScript
- **Banco de Dados**: SQLite (desenvolvimento)
- **Gerenciamento de Dependências**: UV
- **Gráficos**: Chart.js

## 📋 Pré-requisitos

- Python 3.11+
- UV (gerenciador de pacotes Python)
- Navegador web moderno

## 🚀 Instalação e Configuração

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd sge-v2
```

### 2. Ative o ambiente virtual e instale dependências
```bash
# O ambiente virtual já deve estar criado
uv sync
```

### 3. Execute as migrações
```bash
uv run python manage.py migrate
```

### 4. Crie um superusuário
```bash
uv run python manage.py createsuperuser
```

### 5. Execute o servidor de desenvolvimento
```bash
uv run python manage.py runserver
```

### 6. Acesse o sistema
Abra seu navegador e acesse: `http://127.0.0.1:8000`

## 👤 Acesso ao Sistema

### Interface Web
- URL: `http://127.0.0.1:8000`
- Use as credenciais do superusuário criado

### Painel Administrativo
- URL: `http://127.0.0.1:8000/admin`
- Acesso completo ao banco de dados

## 📱 Como Usar

### 1. Primeiro Acesso
1. Acesse o painel administrativo (`/admin`)
2. Crie categorias de produtos
3. Cadastre fornecedores
4. Adicione seus primeiros produtos

### 2. Gestão Diária
1. **Dashboard**: Visão geral do sistema
2. **Produtos**: Gerenciar catálogo de produtos
3. **Movimentações**: Registrar entradas e saídas
4. **Vendas**: Processar vendas
5. **Relatórios**: Acompanhar performance

### 3. Funcionalidades Principais

#### Cadastro de Produtos
- Código único obrigatório
- Informações completas (nome, descrição, categoria)
- Preços de custo e venda
- Controle de estoque mínimo
- Unidade de medida

#### Movimentações de Estoque
- **Entrada**: Recebimento de mercadorias
- **Saída**: Vendas ou consumo interno
- **Ajuste**: Correção de inventário
- **Transferência**: Movimentação entre locais

#### Sistema de Vendas
- Seleção de produtos
- Cálculo automático de totais
- Aplicação de descontos
- Geração de movimentação automática

## 🔧 Configurações Avançadas

### Personalização de Unidades
O sistema suporta as seguintes unidades de medida:
- Unidade (UN)
- Quilograma (KG)
- Grama (G)
- Litro (L)
- Mililitro (ML)
- Metro (M)
- Centímetro (CM)
- Caixa (CX)
- Peça (PC)

### Alertas de Estoque
- Produtos sem estoque (vermelho)
- Produtos com estoque baixo (amarelo)
- Produtos com estoque normal (verde)

## 📊 Estrutura do Banco de Dados

### Modelos Principais
- **Categoria**: Organização de produtos
- **Fornecedor**: Dados dos fornecedores
- **Produto**: Catálogo de produtos
- **MovimentacaoEstoque**: Histórico de movimentações
- **Venda**: Registro de vendas
- **ItemVenda**: Itens de cada venda

## 🚨 Solução de Problemas

### Erro de Migração
```bash
uv run python manage.py makemigrations
uv run python manage.py migrate
```

### Problemas de Permissão
```bash
uv run python manage.py createsuperuser
```

### Reset do Banco de Dados
```bash
rm db.sqlite3
uv run python manage.py migrate
uv run python manage.py createsuperuser
```

## 📝 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir melhorias
- Enviar pull requests

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique a documentação
2. Consulte os logs do sistema
3. Abra uma issue no repositório

---

**Desenvolvido com ❤️ usando Django**
