# 📱 Sidebar Colapsável - Sistema de Estoque

## ✨ **Sidebar Melhorada com Funcionalidade de Esconder/Mostrar**

### 🎯 **Funcionalidades Implementadas**

#### **1. Botão de Toggle**
- **Localização**: No header principal, ao lado do título
- **Ícone**: Lista (bi-list) quando visível, seta direita (bi-arrow-right) quando escondida
- **Tooltip**: "Esconder Sidebar" / "Mostrar Sidebar"
- **Hover**: Efeito de escala (scale 1.05)

#### **2. Estados da Sidebar**
- **Visível**: Sidebar normal com navegação completa
- **Escondida**: Sidebar colapsada com largura 0 e margem negativa
- **Transição**: Animação suave de 0.3s para todos os estados

#### **3. Persistência**
- **LocalStorage**: Estado da sidebar salvo no navegador
- **Lembrança**: Sidebar mantém estado entre sessões
- **Padrão**: Sidebar visível por padrão

### 🎨 **Estilos CSS Implementados**

#### **Sidebar Colapsável**
```css
.sidebar {
    transition: all 0.3s ease;
    min-height: 100vh;
}

.sidebar.collapsed {
    margin-left: -250px;
    width: 0;
    overflow: hidden;
}

.sidebar.collapsed .nav {
    opacity: 0;
}
```

#### **Conteúdo Principal**
```css
.main-content {
    transition: all 0.3s ease;
}

.main-content.expanded {
    margin-left: 0;
    width: 100%;
}

.sidebar.collapsed + .main-content {
    margin-left: 0;
    width: 100%;
}
```

#### **Botão de Toggle**
```css
#sidebar-toggle {
    transition: all 0.3s ease;
}

#sidebar-toggle:hover {
    transform: scale(1.05);
}
```

### 📱 **Responsividade**

#### **Desktop (mais de 768px)**
- **Sidebar**: Colapsa para a esquerda
- **Conteúdo**: Expande para ocupar toda a largura
- **Transição**: Suave e elegante

#### **Mobile (768px ou menos)**
- **Sidebar**: Posição fixa com overlay
- **Conteúdo**: Sempre ocupa 100% da largura
- **Transform**: translateX para animação lateral

```css
@media (max-width: 768px) {
    .sidebar {
        position: fixed;
        top: 0;
        left: 0;
        z-index: 1000;
        width: 250px;
        height: 100vh;
        transform: translateX(-100%);
        transition: transform 0.3s ease;
    }
    
    .sidebar.show {
        transform: translateX(0);
    }
}
```

### 🔧 **JavaScript Implementado**

#### **Gerenciamento de Estado**
```javascript
// Get saved sidebar state or default to visible
const savedSidebarState = localStorage.getItem('sidebar-collapsed') === 'true';

// Apply sidebar state
function applySidebarState(collapsed) {
    if (collapsed) {
        sidebar.classList.add('collapsed');
        mainContent.classList.add('expanded');
        sidebarIcon.className = 'bi bi-arrow-right';
        sidebarToggle.title = 'Mostrar Sidebar';
    } else {
        sidebar.classList.remove('collapsed');
        mainContent.classList.remove('expanded');
        sidebarIcon.className = 'bi bi-list';
        sidebarToggle.title = 'Esconder Sidebar';
    }
}
```

#### **Event Listeners**
```javascript
// Toggle sidebar on button click
sidebarToggle.addEventListener('click', function() {
    const isCollapsed = sidebar.classList.contains('collapsed');
    const newState = !isCollapsed;
    
    applySidebarState(newState);
    localStorage.setItem('sidebar-collapsed', newState.toString());
});

// Handle window resize
window.addEventListener('resize', function() {
    if (window.innerWidth <= 768) {
        sidebar.classList.remove('collapsed');
        mainContent.classList.remove('expanded');
    }
});
```

### 🎯 **Benefícios das Melhorias**

#### **1. Mais Espaço para Conteúdo**
- **Tela Limpa**: Mais espaço para visualizar dados
- **Foco**: Usuário pode focar no conteúdo principal
- **Produtividade**: Melhor experiência para telas menores

#### **2. Flexibilidade**
- **Escolha do Usuário**: Cada usuário pode escolher sua preferência
- **Persistência**: Estado mantido entre sessões
- **Responsivo**: Funciona bem em todos os dispositivos

#### **3. Experiência de Usuário**
- **Intuitivo**: Botão claro e visível
- **Suave**: Transições elegantes
- **Consistente**: Funciona em todas as páginas

### 🔍 **Elementos da Interface**

#### **Botão de Toggle**
- **Posição**: Header principal, lado esquerdo
- **Estilo**: Botão outline secundário
- **Ícones**: 
  - `bi-list` (quando visível)
  - `bi-arrow-right` (quando escondida)
- **Hover**: Efeito de escala

#### **Sidebar**
- **ID**: `#sidebar`
- **Classes**: `sidebar`, `collapsed` (quando escondida)
- **Transição**: `all 0.3s ease`

#### **Conteúdo Principal**
- **ID**: `#main-content`
- **Classes**: `main-content`, `expanded` (quando sidebar escondida)
- **Transição**: `all 0.3s ease`

### 🚀 **Funcionalidades**

#### **1. Toggle Manual**
- **Clique**: Botão para esconder/mostrar
- **Estado**: Alterna entre visível e escondida
- **Salvamento**: Estado salvo automaticamente

#### **2. Responsividade Automática**
- **Mobile**: Sidebar sempre escondida em telas pequenas
- **Desktop**: Sidebar pode ser escondida/mostrada
- **Redimensionamento**: Ajuste automático ao redimensionar

#### **3. Persistência**
- **LocalStorage**: Estado salvo no navegador
- **Sessão**: Mantido entre recarregamentos
- **Padrão**: Sidebar visível por padrão

### 🎉 **Resultado Final**

A sidebar agora oferece:

1. **Funcionalidade de Esconder/Mostrar**: Botão intuitivo no header
2. **Transições Suaves**: Animações elegantes de 0.3s
3. **Responsividade**: Funciona perfeitamente em todos os dispositivos
4. **Persistência**: Estado mantido entre sessões
5. **Mais Espaço**: Conteúdo principal pode ocupar toda a tela

**Agora você pode esconder a sidebar quando precisar de mais espaço!** 📱✨
