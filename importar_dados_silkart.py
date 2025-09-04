#!/usr/bin/env python3
"""
Script para importar dados do arquivo estoquesilkart.json para o sistema Django
"""

import os
import sys
import json
import django
from datetime import datetime
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sge_sistema.settings')
django.setup()

from django.contrib.auth.models import User
from estoque.models import Categoria, Fornecedor, Produto, MovimentacaoEstoque

def criar_usuario_admin():
    """Criar usuário admin se não existir"""
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@admin.com',
            password='admin123',
            first_name='Admin',
            last_name='Sistema'
        )
        print("✅ Usuário admin criado")
    else:
        print("ℹ️ Usuário admin já existe")

def criar_categorias():
    """Criar categorias baseadas nos dados do JSON"""
    categorias_data = [
        {'nome': 'Tecido', 'descricao': 'Tecidos diversos para confecção'},
        {'nome': 'Tecido Cortado', 'descricao': 'Tecidos já cortados em medidas específicas'},
        {'nome': 'Tinta', 'descricao': 'Tintas para impressão e sublimação'},
        {'nome': 'Papel', 'descricao': 'Papéis para impressão e acabamento'},
    ]
    
    categorias_criadas = []
    for cat_data in categorias_data:
        categoria, created = Categoria.objects.get_or_create(
            nome=cat_data['nome'],
            defaults={'descricao': cat_data['descricao'], 'ativa': True}
        )
        if created:
            print(f"✅ Categoria criada: {categoria.nome}")
        else:
            print(f"ℹ️ Categoria já existe: {categoria.nome}")
        categorias_criadas.append(categoria)
    
    return categorias_criadas

def criar_fornecedores():
    """Criar fornecedores baseados nos dados do JSON"""
    fornecedores_data = [
        {
            'nome': 'Admin Fornecedor',
            'cnpj': '00.000.000/0001-00',
            'endereco': 'Endereço Admin',
            'telefone': 'admin',
            'email': 'admin@admin.com',
            'contato': 'Admin',
            'ativo': True
        },
        {
            'nome': 'Kelton',
            'cnpj': '00.000.000/0002-00',
            'endereco': 'Endereço Kelton',
            'telefone': '27997584243',
            'email': 'alka.representa1@gmail.com',
            'contato': 'Kelton',
            'ativo': True
        }
    ]
    
    fornecedores_criados = []
    for forn_data in fornecedores_data:
        # Verificar se já existe fornecedor com este CNPJ
        fornecedor_existente = Fornecedor.objects.filter(cnpj=forn_data['cnpj']).first()
        
        if fornecedor_existente:
            print(f"ℹ️ Fornecedor já existe: {fornecedor_existente.nome}")
            fornecedores_criados.append(fornecedor_existente)
        else:
            # Verificar se existe com o mesmo nome
            fornecedor, created = Fornecedor.objects.get_or_create(
                nome=forn_data['nome'],
                defaults=forn_data
            )
            if created:
                print(f"✅ Fornecedor criado: {fornecedor.nome}")
            else:
                print(f"ℹ️ Fornecedor já existe: {fornecedor.nome}")
            fornecedores_criados.append(fornecedor)
    
    return fornecedores_criados

def criar_produtos_tecidos(categoria_tecido, fornecedores):
    """Criar produtos de tecidos"""
    tecidos_data = [
        {"id": 1, "type": "Cetim", "qtyMetros": "38", "width": "150", "qtyMin": "0"},
        {"id": 2, "type": "Sued Bege", "qtyMetros": "285", "width": "140", "qtyMin": "0"},
        {"id": 3, "type": "Sued Branco", "qtyMetros": "30", "width": "140", "qtyMin": "0"},
        {"id": 4, "type": "Oxford em pontas", "qtyMetros": "17.7", "width": "150", "qtyMin": "0"},
        {"id": 5, "type": "Oxfordini em pontas", "qtyMetros": "0", "width": "150", "qtyMin": "0"},
        {"id": 6, "type": "Oxfordini Off", "qtyMetros": "79", "width": "150", "qtyMin": "0"},
        {"id": 7, "type": "Malha Jersey", "qtyMetros": "125.6", "width": "175", "qtyMin": "0"},
        {"id": 8, "type": "Crepe Salinas ATIVA OFF", "qtyMetros": "35", "width": "145", "qtyMin": "0"},
        {"id": 9, "type": "Crepe Salinas EURO Branco", "qtyMetros": "230", "width": "145", "qtyMin": "0"},
        {"id": 10, "type": "Crepe Salinas EURO OFF", "qtyMetros": "140", "width": "145", "qtyMin": "0"},
        {"id": 13, "type": "Malha Textneo", "qtyMetros": "476", "width": "158", "qtyMin": "0"},
        {"id": 15, "type": "Tactel Vipal - 160gr", "qtyMetros": "640", "width": "160", "qtyMin": "0"}
    ]
    
    produtos_criados = []
    for tecido in tecidos_data:
        produto, created = Produto.objects.get_or_create(
            codigo=f"TEC{tecido['id']:03d}",
            defaults={
                'nome': tecido['type'],
                'descricao': f"Tecido {tecido['type']} - Largura: {tecido['width']}cm",
                'categoria': categoria_tecido,
                'fornecedor': fornecedores[0],  # Admin fornecedor
                'preco_custo': Decimal('25.00'),
                'preco_venda': Decimal('35.00'),
                'estoque_minimo': int(tecido['qtyMin']),
                'estoque_atual': float(tecido['qtyMetros']),
                'unidade': 'MT',
                'ativo': True
            }
        )
        if created:
            print(f"✅ Produto tecido criado: {produto.nome}")
        else:
            print(f"ℹ️ Produto tecido já existe: {produto.nome}")
        produtos_criados.append(produto)
    
    return produtos_criados

def criar_produtos_tecidos_cortados(categoria_tecido_cortado, fornecedores):
    """Criar produtos de tecidos cortados"""
    tecidos_cortados_data = [
        {"id": 1, "type": "malha", "quantity": "1010", "measurement": "38x38", "qtyMin": "0"},
        {"id": 2, "type": "malha", "quantity": "100", "measurement": "41x41", "qtyMin": "0"},
        {"id": 3, "type": "malha", "quantity": "550", "measurement": "43x43", "qtyMin": "0"},
        {"id": 4, "type": "tactel", "quantity": "770", "measurement": "100x45", "qtyMin": "0"},
        {"id": 5, "type": "tactel", "quantity": "1100", "measurement": "25x55", "qtyMin": "0"},
        {"id": 6, "type": "tactel", "quantity": "80", "measurement": "45x83", "qtyMin": "0"},
        {"id": 7, "type": "tactel", "quantity": "383", "measurement": "45x45", "qtyMin": "0"},
        {"id": 8, "type": "tactel", "quantity": "0", "measurement": "25x65", "qtyMin": "0"},
        {"id": 9, "type": "tactel", "quantity": "0", "measurement": "35x95", "qtyMin": "0"},
        {"id": 10, "type": "tactel", "quantity": "170", "measurement": "43x43", "qtyMin": "0"},
        {"id": 11, "type": "tactel", "quantity": "870", "measurement": "100x50", "qtyMin": "0"}
    ]
    
    produtos_criados = []
    for tecido_cortado in tecidos_cortados_data:
        produto, created = Produto.objects.get_or_create(
            codigo=f"TEC_CORT{tecido_cortado['id']:03d}",
            defaults={
                'nome': f"{tecido_cortado['type']} {tecido_cortado['measurement']}",
                'descricao': f"Tecido cortado {tecido_cortado['type']} - Medida: {tecido_cortado['measurement']}",
                'categoria': categoria_tecido_cortado,
                'fornecedor': fornecedores[0],  # Admin fornecedor
                'preco_custo': Decimal('15.00'),
                'preco_venda': Decimal('22.00'),
                'estoque_minimo': int(tecido_cortado['qtyMin']),
                'estoque_atual': int(tecido_cortado['quantity']),
                'unidade': 'UN',
                'ativo': True
            }
        )
        if created:
            print(f"✅ Produto tecido cortado criado: {produto.nome}")
        else:
            print(f"ℹ️ Produto tecido cortado já existe: {produto.nome}")
        produtos_criados.append(produto)
    
    return produtos_criados

def criar_produtos_tintas(categoria_tinta, fornecedores):
    """Criar produtos de tintas"""
    tintas_data = [
        {"id": 1, "color": "cyan", "type": "pigmentada", "productQty": "3", "productQtyLitros": "1", "qtyMin": "1"},
        {"id": 2, "color": "magenta", "type": "pigmentada", "productQty": "3", "productQtyLitros": "1", "qtyMin": "0"},
        {"id": 3, "color": "amarelo", "type": "pigmentada", "productQty": "3", "productQtyLitros": "1", "qtyMin": "0"},
        {"id": 4, "color": "preto", "type": "pigmentada", "productQty": "3", "productQtyLitros": "1", "qtyMin": "0"},
        {"id": 5, "color": "cyan", "type": "sublimacao", "productQty": "3", "productQtyLitros": "1", "qtyMin": "0"},
        {"id": 6, "color": "magenta", "type": "sublimacao", "productQty": "3", "productQtyLitros": "1", "qtyMin": "0"},
        {"id": 7, "color": "amarelo", "type": "sublimacao", "productQty": "3", "productQtyLitros": "1", "qtyMin": "0"},
        {"id": 8, "color": "preto", "type": "sublimacao", "productQty": "3", "productQtyLitros": "1", "qtyMin": "0"}
    ]
    
    produtos_criados = []
    for tinta in tintas_data:
        produto, created = Produto.objects.get_or_create(
            codigo=f"TINTA_{tinta['id']:03d}",
            defaults={
                'nome': f"Tinta {tinta['color']} {tinta['type']}",
                'descricao': f"Tinta {tinta['type']} na cor {tinta['color']} - {tinta['productQtyLitros']}L",
                'categoria': categoria_tinta,
                'fornecedor': fornecedores[0],  # Admin fornecedor
                'preco_custo': Decimal('45.00'),
                'preco_venda': Decimal('65.00'),
                'estoque_minimo': int(tinta['qtyMin']),
                'estoque_atual': int(tinta['productQty']),
                'unidade': 'UN',
                'ativo': True
            }
        )
        if created:
            print(f"✅ Produto tinta criado: {produto.nome}")
        else:
            print(f"ℹ️ Produto tinta já existe: {produto.nome}")
        produtos_criados.append(produto)
    
    return produtos_criados

def criar_produtos_papeis(categoria_papel, fornecedores):
    """Criar produtos de papéis"""
    papeis_data = [
        {"id": 2, "type": "papel2", "qtyUnit": "1", "qtyMetros": "400", "qtyMin": "0"},
        {"id": 5, "type": "papel5", "qtyUnit": "6", "qtyMetros": "1000", "qtyMin": "0"},
        {"id": 6, "type": "papel6", "qtyUnit": "10", "qtyMetros": "500", "qtyMin": "0"},
        {"id": 8, "type": "papel1", "qtyUnit": "15", "qtyMetros": "250", "qtyMin": "0"},
        {"id": 10, "type": "papel4", "qtyUnit": "4", "qtyMetros": "400", "qtyMin": "0"},
        {"id": 11, "type": "papel3", "qtyUnit": "1", "qtyMetros": "1000", "qtyMin": "0"}
    ]
    
    produtos_criados = []
    for papel in papeis_data:
        produto, created = Produto.objects.get_or_create(
            codigo=f"PAPEL_{papel['id']:03d}",
            defaults={
                'nome': f"Papel {papel['type']}",
                'descricao': f"Papel {papel['type']} - {papel['qtyMetros']} metros",
                'categoria': categoria_papel,
                'fornecedor': fornecedores[0],  # Admin fornecedor
                'preco_custo': Decimal('8.00'),
                'preco_venda': Decimal('12.00'),
                'estoque_minimo': int(papel['qtyMin']),
                'estoque_atual': int(papel['qtyUnit']),
                'unidade': 'UN',
                'ativo': True
            }
        )
        if created:
            print(f"✅ Produto papel criado: {produto.nome}")
        else:
            print(f"ℹ️ Produto papel já existe: {produto.nome}")
        produtos_criados.append(produto)
    
    return produtos_criados

def importar_movimentacoes(produtos_mapeados, fornecedores):
    """Importar movimentações de entrada e saída"""
    # Ler arquivo JSON
    with open('estoquesilkart.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Encontrar dados de entradas e saídas
    entries_data = None
    exits_data = None
    
    for item in data:
        if item.get('type') == 'table' and item.get('name') == 'entries':
            entries_data = item.get('data', [])
        elif item.get('type') == 'table' and item.get('name') == 'exits':
            exits_data = item.get('data', [])
    
    if not entries_data or not exits_data:
        print("❌ Dados de movimentações não encontrados no JSON")
        return
    
    # Criar usuário admin se não existir
    admin_user = User.objects.get(username='admin')
    
    # Importar entradas
    print("\n📥 Importando entradas...")
    for entry in entries_data:
        try:
            # Mapear produto baseado na categoria e product_id
            produto = None
            categoria = entry['category']
            product_id = int(entry['product_id'])
            
            if categoria == 'tecido':
                produto = next((p for p in produtos_mapeados['tecidos'] if p.codigo == f"TEC{product_id:03d}"), None)
            elif categoria == 'tecido-cortado':
                produto = next((p for p in produtos_mapeados['tecidos_cortados'] if p.codigo == f"TEC_CORT{product_id:03d}"), None)
            elif categoria == 'tinta':
                produto = next((p for p in produtos_mapeados['tintas'] if p.codigo == f"TINTA_{product_id:03d}"), None)
            elif categoria == 'papel':
                produto = next((p for p in produtos_mapeados['papeis'] if p.codigo == f"PAPEL_{product_id:03d}"), None)
            
            if produto:
                # Criar movimentação de entrada
                data_movimentacao = datetime.strptime(entry['date'], '%Y-%m-%d %H:%M:%S')
                
                movimentacao = MovimentacaoEstoque.objects.create(
                    produto=produto,
                    tipo='ENTRADA',
                    quantidade=float(entry['quantity']),
                    usuario=admin_user,
                    observacoes=f"Importação do Silkart - {categoria}",
                    destino="Estoque Principal"
                )
                
                # Atualizar estoque do produto
                produto.estoque_atual += float(entry['quantity'])
                produto.save()
                
                print(f"✅ Entrada criada: {produto.nome} - {entry['quantity']} unidades")
            else:
                print(f"⚠️ Produto não encontrado para entrada: {categoria} ID {product_id}")
                
        except Exception as e:
            print(f"❌ Erro ao criar entrada: {e}")
    
    # Importar saídas
    print("\n📤 Importando saídas...")
    for exit_item in exits_data:
        try:
            # Mapear produto baseado na categoria e product_id
            produto = None
            categoria = exit_item['category']
            product_id = int(exit_item['product_id'])
            
            if categoria == 'tecido':
                produto = next((p for p in produtos_mapeados['tecidos'] if p.codigo == f"TEC{product_id:03d}"), None)
            elif categoria == 'tecido-cortado':
                produto = next((p for p in produtos_mapeados['tecidos_cortados'] if p.codigo == f"TEC_CORT{product_id:03d}"), None)
            elif categoria == 'tinta':
                produto = next((p for p in produtos_mapeados['tintas'] if p.codigo == f"TINTA_{product_id:03d}"), None)
            elif categoria == 'papel':
                produto = next((p for p in produtos_mapeados['papeis'] if p.codigo == f"PAPEL_{product_id:03d}"), None)
            
            if produto:
                # Criar movimentação de saída
                data_movimentacao = datetime.strptime(exit_item['date'], '%Y-%m-%d %H:%M:%S')
                
                movimentacao = MovimentacaoEstoque.objects.create(
                    produto=produto,
                    tipo='SAIDA',
                    quantidade=float(exit_item['quantity']),
                    usuario=admin_user,
                    observacoes=f"Importação do Silkart - {categoria}",
                    destino="Venda/Produção"
                )
                
                # Atualizar estoque do produto
                produto.estoque_atual -= float(exit_item['quantity'])
                produto.save()
                
                print(f"✅ Saída criada: {produto.nome} - {exit_item['quantity']} unidades")
            else:
                print(f"⚠️ Produto não encontrado para saída: {categoria} ID {product_id}")
                
        except Exception as e:
            print(f"❌ Erro ao criar saída: {e}")

def main():
    """Função principal para importar todos os dados"""
    print("🚀 Iniciando importação dos dados do Silkart...")
    
    try:
        # 1. Criar usuário admin
        criar_usuario_admin()
        
        # 2. Criar categorias
        print("\n📁 Criando categorias...")
        categorias = criar_categorias()
        categoria_tecido = categorias[0]
        categoria_tecido_cortado = categorias[1]
        categoria_tinta = categorias[2]
        categoria_papel = categorias[3]
        
        # 3. Criar fornecedores
        print("\n🏢 Criando fornecedores...")
        fornecedores = criar_fornecedores()
        
        # 4. Criar produtos
        print("\n📦 Criando produtos...")
        produtos_tecidos = criar_produtos_tecidos(categoria_tecido, fornecedores)
        produtos_tecidos_cortados = criar_produtos_tecidos_cortados(categoria_tecido_cortado, fornecedores)
        produtos_tintas = criar_produtos_tintas(categoria_tinta, fornecedores)
        produtos_papeis = criar_produtos_papeis(categoria_papel, fornecedores)
        
        # Mapear produtos para importação
        produtos_mapeados = {
            'tecidos': produtos_tecidos,
            'tecidos_cortados': produtos_tecidos_cortados,
            'tintas': produtos_tintas,
            'papeis': produtos_papeis
        }
        
        # 5. Importar movimentações
        print("\n📊 Importando movimentações...")
        importar_movimentacoes(produtos_mapeados, fornecedores)
        
        # 6. Resumo final
        print("\n🎉 Importação concluída com sucesso!")
        print(f"📊 Resumo:")
        print(f"   - Categorias: {Categoria.objects.count()}")
        print(f"   - Fornecedores: {Fornecedor.objects.count()}")
        print(f"   - Produtos: {Produto.objects.count()}")
        print(f"   - Movimentações: {MovimentacaoEstoque.objects.count()}")
        
    except Exception as e:
        print(f"❌ Erro durante a importação: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
