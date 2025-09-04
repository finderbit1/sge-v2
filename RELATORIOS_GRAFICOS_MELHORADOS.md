# 📊 Relatórios e Gráficos Melhorados - Sistema de Estoque

## ✨ **Sistema de Relatórios e Gráficos Avançado**

### 🎯 **Funcionalidades Implementadas**

#### **1. Dashboard de Relatórios Interativo**
- **4 Gráficos Principais**: Movimentações diárias, produtos por categoria, movimentações por tipo, vendas mensais
- **Cards de Resumo**: Total de produtos, sem estoque, estoque baixo, valor total
- **Tabelas Detalhadas**: Top produtos movimentados, produtos com estoque baixo
- **Atualização em Tempo Real**: Botão de atualização e refresh automático a cada 60 segundos

#### **2. Sistema de Exportação Excel com Filtro de Datas**
- **Formulário Intuitivo**: Seleção de data início, data fim e tipo de relatório
- **4 Tipos de Relatórios**:
  - **Movimentações**: Entradas e saídas com filtro de período
  - **Produtos**: Lista completa com status de estoque
  - **Vendas**: Vendas realizadas no período
  - **Resumo Geral**: Métricas e indicadores do período
- **Validação de Datas**: Intervalo máximo de 1 ano, validação de datas
- **Arquivos Nomeados**: Nomenclatura automática com período selecionado

#### **3. Gráficos Interativos com Chart.js**
- **Gráfico de Linha**: Movimentações diárias (entradas vs saídas)
- **Gráfico de Pizza**: Distribuição de produtos por categoria
- **Gráfico de Barras**: Movimentações por tipo (entrada/saída)
- **Gráfico de Linha**: Evolução das vendas mensais
- **Responsivos**: Adaptam-se a diferentes tamanhos de tela
- **Cores Temáticas**: Paleta consistente com o design do sistema

### 🎨 **Interface e Design**

#### **Cards de Resumo**
```html
<!-- Exemplo de card de resumo -->
<div class="card card-stat border-left-primary shadow h-100">
    <div class="card-body">
        <div class="row no-gutters align-items-center">
            <div class="col mr-2">
                <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">
                    Total de Produtos
                </div>
                <div class="h5 mb-0 font-weight-bold text-gray-800">{{ total_produtos }}</div>
            </div>
            <div class="col-auto">
                <i class="bi bi-boxes fa-2x text-primary"></i>
            </div>
        </div>
    </div>
</div>
```

#### **Gráficos Responsivos**
- **Canvas Otimizado**: Tamanho adaptável para diferentes dispositivos
- **Cores Consistentes**: Paleta de cores harmoniosa
- **Animações Suaves**: Transições elegantes nos gráficos
- **Tooltips Informativos**: Informações detalhadas ao passar o mouse

### 📊 **Tipos de Relatórios Excel**

#### **1. Movimentações de Estoque**
- **Colunas**: Data/Hora, Produto, Categoria, Tipo, Quantidade, Usuário, Observações
- **Filtro**: Por período de datas
- **Formatação**: Bordas, cores, alinhamento profissional
- **Nome do arquivo**: `movimentacoes_YYYYMMDD_YYYYMMDD.xlsx`

#### **2. Produtos**
- **Colunas**: Código, Nome, Categoria, Fornecedor, Estoque Atual, Estoque Mínimo, Preço Custo, Preço Venda, Status
- **Status**: Sem Estoque, Baixo, OK
- **Formatação**: Larguras de coluna otimizadas
- **Nome do arquivo**: `produtos_YYYYMMDD_YYYYMMDD.xlsx`

#### **3. Vendas**
- **Colunas**: Data, Número Venda, Cliente, Total, Status, Vendedor
- **Filtro**: Por período de datas
- **Formatação**: Valores monetários formatados
- **Nome do arquivo**: `vendas_YYYYMMDD_YYYYMMDD.xlsx`

#### **4. Resumo Geral**
- **Métricas**: Total de produtos, sem estoque, estoque baixo, valor total, movimentações
- **Formato**: Tabela simples com métricas e valores
- **Nome do arquivo**: `resumo_YYYYMMDD_YYYYMMDD.xlsx`

### 🔧 **Funcionalidades Técnicas**

#### **View de Relatórios Melhorada**
```python
@login_required
def relatorios(request):
    """Página de relatórios com gráficos e estatísticas detalhadas"""
    # Dados básicos de estoque
    produtos_estoque_baixo = Produto.objects.filter(
        ativo=True,
        estoque_atual__lte=F('estoque_minimo')
    ).count()
    
    # Valor total do estoque
    valor_total_estoque = sum(
        produto.estoque_atual * produto.preco_custo 
        for produto in Produto.objects.filter(ativo=True)
    )
    
    # Movimentações por dia (últimos 7 dias)
    movimentacoes_por_dia = []
    for i in range(7):
        data = timezone.now() - timedelta(days=i)
        entrada = MovimentacaoEstoque.objects.filter(
            tipo='ENTRADA',
            data_movimentacao__date=data.date()
        ).count()
        saida = MovimentacaoEstoque.objects.filter(
            tipo='SAIDA',
            data_movimentacao__date=data.date()
        ).count()
        
        movimentacoes_por_dia.append({
            'dia': data.strftime('%d/%m'),
            'entrada': entrada,
            'saida': saida
        })
```

#### **Sistema de Exportação Excel**
```python
@login_required
def exportar_relatorio_excel(request):
    """Exportar relatórios em Excel com filtro de datas"""
    if request.method == 'POST':
        form = RelatorioDataForm(request.POST)
        if form.is_valid():
            data_inicio = form.cleaned_data['data_inicio']
            data_fim = form.cleaned_data['data_fim']
            tipo_relatorio = form.cleaned_data['tipo_relatorio']
            
            # Criar workbook com estilos profissionais
            wb = openpyxl.Workbook()
            ws = wb.active
            
            # Aplicar estilos e formatação
            # ... código de formatação ...
```

#### **Formulário de Seleção de Datas**
```python
class RelatorioDataForm(forms.Form):
    """Formulário para seleção de intervalo de datas para relatórios"""
    data_inicio = forms.DateField(
        label='Data Início',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'id': 'data-inicio'
        })
    )
    
    data_fim = forms.DateField(
        label='Data Fim',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'id': 'data-fim'
        })
    )
    
    tipo_relatorio = forms.ChoiceField(
        label='Tipo de Relatório',
        choices=[
            ('movimentacoes', 'Movimentações de Estoque'),
            ('produtos', 'Produtos'),
            ('vendas', 'Vendas'),
            ('resumo', 'Resumo Geral')
        ]
    )
```

### 📱 **Responsividade e UX**

#### **Interface Responsiva**
- **Desktop**: Gráficos lado a lado, tabelas completas
- **Tablet**: Gráficos empilhados, tabelas com scroll
- **Mobile**: Gráficos otimizados, cards empilhados

#### **Experiência do Usuário**
- **Loading States**: Indicadores de carregamento
- **Validação em Tempo Real**: Feedback imediato
- **Mensagens de Sucesso**: Confirmações de ações
- **Atalhos de Teclado**: Ctrl+Enter para exportar, Escape para limpar

#### **JavaScript Interativo**
```javascript
// Atualização automática de dados
function atualizarDados() {
    fetch('{% url "estoque:dashboard_ajax" %}')
        .then(response => response.json())
        .then(data => {
            // Atualizar cards de resumo
            document.querySelector('.card-stat:nth-child(1) .h5').textContent = data.total_produtos;
            
            // Atualizar gráfico de movimentações
            movimentacoesChart.data.labels = data.movimentacoes_por_dia.map(item => item.dia);
            movimentacoesChart.update();
        });
}

// Atualização automática a cada 60 segundos
setInterval(atualizarDados, 60000);
```

### 🎯 **Benefícios das Melhorias**

#### **1. Análise Visual**
- **Gráficos Intuitivos**: Fácil compreensão dos dados
- **Múltiplas Perspectivas**: Diferentes visualizações dos mesmos dados
- **Tendências**: Identificação de padrões e tendências

#### **2. Exportação Profissional**
- **Relatórios Personalizados**: Filtros por período
- **Formatação Profissional**: Estilos e cores consistentes
- **Dados Completos**: Informações detalhadas para análise

#### **3. Performance**
- **Atualização Automática**: Dados sempre atualizados
- **Carregamento Rápido**: Otimização de consultas
- **Interface Responsiva**: Funciona em todos os dispositivos

#### **4. Usabilidade**
- **Interface Intuitiva**: Fácil navegação e uso
- **Validação Inteligente**: Prevenção de erros
- **Feedback Visual**: Confirmações e mensagens claras

### 🚀 **Como Usar**

#### **1. Acessar Relatórios**
- Navegue para "Relatórios" no menu lateral
- Visualize gráficos e estatísticas em tempo real
- Use o botão "Atualizar" para dados mais recentes

#### **2. Exportar para Excel**
- Clique em "Exportar Excel" no cabeçalho
- Selecione o período desejado (máximo 1 ano)
- Escolha o tipo de relatório
- Clique em "Exportar para Excel"

#### **3. Tipos de Relatórios**
- **Movimentações**: Para análise de entradas e saídas
- **Produtos**: Para inventário e status de estoque
- **Vendas**: Para análise comercial
- **Resumo**: Para visão geral e métricas

### 📋 **URLs e Rotas**

#### **Relatórios**
- `/estoque/relatorios/` - Dashboard de relatórios
- `/estoque/relatorios/exportar/` - Formulário de exportação
- `/estoque/relatorios/produtos-pdf/` - Relatório PDF de produtos
- `/estoque/relatorios/movimentacoes-excel/` - Relatório Excel de movimentações

#### **AJAX**
- `/estoque/ajax/dashboard/` - Atualização de dados do dashboard

### 🎉 **Resultado Final**

**O sistema agora possui um sistema completo de relatórios e gráficos!**

- ✅ **4 Gráficos Interativos**: Movimentações, categorias, tipos, vendas
- ✅ **Exportação Excel**: Com filtro de datas e 4 tipos de relatórios
- ✅ **Interface Responsiva**: Funciona em todos os dispositivos
- ✅ **Atualização Automática**: Dados sempre atualizados
- ✅ **Validação Inteligente**: Prevenção de erros
- ✅ **Formatação Profissional**: Relatórios com qualidade empresarial

**Agora você pode analisar seus dados de forma visual e exportar relatórios personalizados para Excel!** 📊✨

