# 🌙 Tema Escuro - Sistema de Estoque

## ✨ Funcionalidades do Tema Escuro

### 🎨 **Alternância de Tema**
- **Botão de Toggle**: Clique no ícone de lua/sol no canto superior direito
- **Persistência**: O tema escolhido é salvo no localStorage
- **Transições Suaves**: Animações de 0.3s para mudanças de tema
- **Ícones Dinâmicos**: 
  - 🌙 Lua = Ativar tema escuro
  - ☀️ Sol = Ativar tema claro

### 🎯 **Elementos com Suporte ao Tema Escuro**

#### **Interface Principal**
- ✅ Sidebar com cores escuras
- ✅ Cards e containers adaptados
- ✅ Tabelas com fundo escuro
- ✅ Formulários com campos escuros
- ✅ Botões e links adaptados

#### **Componentes Específicos**
- ✅ Dashboard com estatísticas
- ✅ Lista de produtos
- ✅ Formulários de cadastro
- ✅ Movimentações de estoque
- ✅ Sistema de vendas
- ✅ Relatórios e gráficos

#### **Elementos de Navegação**
- ✅ Menu lateral (sidebar)
- ✅ Cabeçalho principal
- ✅ Breadcrumbs
- ✅ Paginação
- ✅ Alertas e notificações

### 🎨 **Paleta de Cores do Tema Escuro**

#### **Cores Principais**
- **Fundo Primário**: `#1a1a1a` (preto suave)
- **Fundo Secundário**: `#2d2d2d` (cinza escuro)
- **Sidebar**: `#1e1e1e` (preto mais escuro)
- **Cards**: `#2d2d2d` (cinza escuro)

#### **Cores de Texto**
- **Texto Primário**: `#ffffff` (branco)
- **Texto Secundário**: `#adb5bd` (cinza claro)
- **Texto Muted**: `#6c757d` (cinza médio)

#### **Cores de Bordas**
- **Bordas**: `#495057` (cinza escuro)
- **Hover**: `rgba(255, 255, 255, 0.1)` (branco transparente)

### 🚀 **Como Usar**

1. **Acesse o Sistema**: http://127.0.0.1:8000
2. **Clique no Botão de Tema**: Ícone de lua/sol no canto superior direito
3. **Tema é Salvo Automaticamente**: Sua preferência é lembrada
4. **Funciona em Todas as Páginas**: Login, dashboard, produtos, etc.

### 🔧 **Implementação Técnica**

#### **CSS Variables**
```css
:root {
    --bg-primary: #ffffff;
    --text-primary: #212529;
    /* ... outras variáveis */
}

[data-theme="dark"] {
    --bg-primary: #1a1a1a;
    --text-primary: #ffffff;
    /* ... variáveis do tema escuro */
}
```

#### **JavaScript**
```javascript
// Alternância de tema
function applyTheme(theme) {
    if (theme === 'dark') {
        body.setAttribute('data-theme', 'dark');
        themeIcon.className = 'bi bi-sun-fill';
    } else {
        body.removeAttribute('data-theme');
        themeIcon.className = 'bi bi-moon-fill';
    }
}
```

#### **Persistência**
```javascript
// Salvar preferência
localStorage.setItem('theme', newTheme);

// Carregar preferência
const savedTheme = localStorage.getItem('theme') || 'light';
```

### 📱 **Responsividade**

- ✅ **Desktop**: Tema completo com sidebar
- ✅ **Tablet**: Layout adaptado
- ✅ **Mobile**: Interface otimizada
- ✅ **Transições**: Suaves em todos os dispositivos

### 🎯 **Benefícios**

1. **Redução de Fadiga Visual**: Especialmente em ambientes com pouca luz
2. **Economia de Bateria**: Em dispositivos com telas OLED
3. **Preferência do Usuário**: Opção de personalização
4. **Acessibilidade**: Melhor contraste para alguns usuários
5. **Modernidade**: Interface mais contemporânea

### 🔍 **Elementos Especiais**

#### **Gráficos e Charts**
- Fundo escuro para melhor visualização
- Cores adaptadas para contraste
- Bordas e linhas visíveis

#### **Formulários**
- Campos com fundo escuro
- Placeholders visíveis
- Botões com cores vibrantes

#### **Tabelas**
- Cabeçalhos com fundo escuro
- Linhas alternadas para melhor leitura
- Bordas sutis

### 🎉 **Sistema Completo**

O tema escuro está **100% implementado** e funcional em todo o sistema:

- ✅ **Página de Login**
- ✅ **Dashboard Principal**
- ✅ **Gestão de Produtos**
- ✅ **Movimentações de Estoque**
- ✅ **Sistema de Vendas**
- ✅ **Relatórios e Gráficos**
- ✅ **Painel Administrativo**

**Aproveite o novo tema escuro!** 🌙✨
