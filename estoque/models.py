from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class Categoria(models.Model):
    """Modelo para categorias de produtos"""
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome da Categoria")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    ativa = models.BooleanField(default=True, verbose_name="Ativa")

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Fornecedor(models.Model):
    """Modelo para fornecedores"""
    nome = models.CharField(max_length=200, verbose_name="Nome do Fornecedor")
    cnpj = models.CharField(max_length=18, unique=True, verbose_name="CNPJ")
    endereco = models.TextField(verbose_name="Endereço")
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    email = models.EmailField(verbose_name="E-mail")
    contato = models.CharField(max_length=100, verbose_name="Pessoa de Contato")
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Produto(models.Model):
    """Modelo para produtos"""
    codigo = models.CharField(max_length=50, unique=True, verbose_name="Código do Produto")
    nome = models.CharField(max_length=200, verbose_name="Nome do Produto")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, verbose_name="Categoria")
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT, verbose_name="Fornecedor")
    
    # Preços
    preco_custo = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Preço de Custo"
    )
    preco_venda = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Preço de Venda"
    )
    
    # Controle de estoque
    estoque_minimo = models.PositiveIntegerField(default=0, verbose_name="Estoque Mínimo")
    estoque_atual = models.IntegerField(default=0, verbose_name="Estoque Atual")
    
    # Unidade de medida
    UNIDADE_CHOICES = [
        ('UN', 'Unidade'),
        ('KG', 'Quilograma'),
        ('G', 'Grama'),
        ('L', 'Litro'),
        ('ML', 'Mililitro'),
        ('M', 'Metro'),
        ('CM', 'Centímetro'),
        ('CX', 'Caixa'),
        ('PC', 'Peça'),
    ]
    unidade = models.CharField(max_length=2, choices=UNIDADE_CHOICES, default='UN', verbose_name="Unidade")
    
    # Status
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['nome']

    def __str__(self):
        return f"{self.codigo} - {self.nome}"

    @property
    def margem_lucro(self):
        """Calcula a margem de lucro em percentual"""
        if self.preco_custo > 0:
            return ((self.preco_venda - self.preco_custo) / self.preco_custo) * 100
        return 0

    @property
    def status_estoque(self):
        """Retorna o status do estoque"""
        if self.estoque_atual <= 0:
            return "Sem Estoque"
        elif self.estoque_atual <= self.estoque_minimo:
            return "Estoque Baixo"
        else:
            return "Estoque Normal"

    @property
    def valor_total_estoque(self):
        """Calcula o valor total do estoque atual"""
        return self.estoque_atual * self.preco_custo


class MovimentacaoEstoque(models.Model):
    """Modelo para movimentações de estoque"""
    TIPO_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('SAIDA', 'Saída'),
        ('AJUSTE', 'Ajuste'),
        ('TRANSFERENCIA', 'Transferência'),
    ]

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, verbose_name="Produto")
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES, verbose_name="Tipo de Movimentação")
    quantidade = models.IntegerField(verbose_name="Quantidade")
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Usuário")
    data_movimentacao = models.DateTimeField(auto_now_add=True, verbose_name="Data da Movimentação")
    
    # Para transferências
    destino = models.CharField(max_length=200, blank=True, null=True, verbose_name="Destino")

    class Meta:
        verbose_name = "Movimentação de Estoque"
        verbose_name_plural = "Movimentações de Estoque"
        ordering = ['-data_movimentacao']

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.produto.nome} - {self.quantidade}"

    def save(self, *args, **kwargs):
        """Atualiza o estoque do produto ao salvar a movimentação"""
        super().save(*args, **kwargs)
        
        # Atualiza o estoque do produto
        if self.tipo == 'ENTRADA':
            self.produto.estoque_atual += self.quantidade
        elif self.tipo == 'SAIDA':
            self.produto.estoque_atual -= self.quantidade
        elif self.tipo == 'AJUSTE':
            self.produto.estoque_atual = self.quantidade
        
        self.produto.save()


class Venda(models.Model):
    """Modelo para vendas"""
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('CONCLUIDA', 'Concluída'),
        ('CANCELADA', 'Cancelada'),
    ]

    numero_venda = models.CharField(max_length=20, unique=True, verbose_name="Número da Venda")
    cliente = models.CharField(max_length=200, verbose_name="Cliente")
    data_venda = models.DateTimeField(auto_now_add=True, verbose_name="Data da Venda")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDENTE', verbose_name="Status")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Total")
    desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Desconto")
    vendedor = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Vendedor")
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")

    class Meta:
        verbose_name = "Venda"
        verbose_name_plural = "Vendas"
        ordering = ['-data_venda']

    def __str__(self):
        return f"Venda #{self.numero_venda} - {self.cliente}"

    @property
    def total_liquido(self):
        """Calcula o total líquido da venda"""
        return self.total - self.desconto


class ItemVenda(models.Model):
    """Modelo para itens de venda"""
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='itens', verbose_name="Venda")
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, verbose_name="Produto")
    quantidade = models.PositiveIntegerField(verbose_name="Quantidade")
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço Unitário")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Subtotal")

    class Meta:
        verbose_name = "Item de Venda"
        verbose_name_plural = "Itens de Venda"

    def __str__(self):
        return f"{self.produto.nome} - {self.quantidade}x"

    def save(self, *args, **kwargs):
        """Calcula o subtotal automaticamente"""
        self.subtotal = self.quantidade * self.preco_unitario
        super().save(*args, **kwargs)