from django import forms
from django.forms import inlineformset_factory
from .models import Produto, Categoria, Fornecedor, MovimentacaoEstoque, Venda, ItemVenda


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'descricao', 'ativa']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ativa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ['nome', 'cnpj', 'endereco', 'telefone', 'email', 'contato', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00.000.000/0000-00'}),
            'endereco': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contato': forms.TextInput(attrs={'class': 'form-control'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            'codigo', 'nome', 'descricao', 'categoria', 'fornecedor',
            'preco_custo', 'preco_venda', 'estoque_minimo', 'estoque_atual',
            'unidade', 'ativo'
        ]
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'fornecedor': forms.Select(attrs={'class': 'form-select'}),
            'preco_custo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'preco_venda': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'estoque_minimo': forms.NumberInput(attrs={'class': 'form-control'}),
            'estoque_atual': forms.NumberInput(attrs={'class': 'form-control'}),
            'unidade': forms.Select(attrs={'class': 'form-select'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.filter(ativa=True)
        self.fields['fornecedor'].queryset = Fornecedor.objects.filter(ativo=True)


class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = MovimentacaoEstoque
        fields = ['produto', 'tipo', 'quantidade', 'observacoes', 'destino']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'destino': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['produto'].queryset = Produto.objects.filter(ativo=True)

    def clean_quantidade(self):
        quantidade = self.cleaned_data.get('quantidade')
        tipo = self.cleaned_data.get('tipo')
        produto = self.cleaned_data.get('produto')
        
        if tipo == 'SAIDA' and produto and quantidade > produto.estoque_atual:
            raise forms.ValidationError(
                f'Quantidade insuficiente em estoque. Disponível: {produto.estoque_atual}'
            )
        
        return quantidade


class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['cliente', 'desconto', 'observacoes']
        widgets = {
            'cliente': forms.TextInput(attrs={'class': 'form-control'}),
            'desconto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0.00'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ItemVendaForm(forms.ModelForm):
    class Meta:
        model = ItemVenda
        fields = ['produto', 'quantidade', 'preco_unitario']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-select produto-select'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control quantidade-input'}),
            'preco_unitario': forms.NumberInput(attrs={'class': 'form-control preco-input', 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['produto'].queryset = Produto.objects.filter(ativo=True)

    def clean_quantidade(self):
        quantidade = self.cleaned_data.get('quantidade')
        produto = self.cleaned_data.get('produto')
        
        if produto and quantidade > produto.estoque_atual:
            raise forms.ValidationError(
                f'Quantidade insuficiente em estoque. Disponível: {produto.estoque_atual}'
            )
        
        return quantidade


# Formset para itens de venda
ItemVendaFormSet = inlineformset_factory(
    Venda, ItemVenda, form=ItemVendaForm,
    extra=1, can_delete=True, min_num=1
)


class BuscaProdutoForm(forms.Form):
    busca = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite o nome ou código do produto...'
        })
    )
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.filter(ativa=True),
        required=False,
        empty_label="Todas as categorias",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    status_estoque = forms.ChoiceField(
        choices=[
            ('', 'Todos os status'),
            ('baixo', 'Estoque Baixo'),
            ('sem_estoque', 'Sem Estoque'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class RelatorioDataForm(forms.Form):
    """Formulário para seleção de intervalo de datas para relatórios"""
    data_inicio = forms.DateField(
        label='Data Início',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'id': 'data-inicio'
        }),
        help_text='Selecione a data de início do período'
    )
    
    data_fim = forms.DateField(
        label='Data Fim',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'id': 'data-fim'
        }),
        help_text='Selecione a data de fim do período'
    )
    
    tipo_relatorio = forms.ChoiceField(
        label='Tipo de Relatório',
        choices=[
            ('movimentacoes', 'Movimentações de Estoque'),
            ('produtos', 'Produtos'),
            ('vendas', 'Vendas'),
            ('resumo', 'Resumo Geral')
        ],
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'tipo-relatorio'
        }),
        help_text='Selecione o tipo de relatório a ser exportado'
    )
    
    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')
        
        if data_inicio and data_fim:
            if data_inicio > data_fim:
                raise forms.ValidationError('A data de início deve ser anterior à data de fim.')
            
            # Verificar se o intervalo não é muito grande (máximo 1 ano)
            from datetime import timedelta
            if (data_fim - data_inicio).days > 365:
                raise forms.ValidationError('O intervalo de datas não pode ser maior que 1 ano.')
        
        return cleaned_data
