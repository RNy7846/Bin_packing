from py3dbp import Packer, Bin, Item, Painter
import time
from random import random
start = time.time()

# iniciar função para encaixotamento
packer = Packer()

# Nivel de Prioridade (Packing Priority level)
#0 : Nenhum
#1 : Pode ter
#2~3 : Obrigatório

def adicionar_caminhao():
    nome = input('Nome do caminhão: ')
    comprimento = float(input('Comprimento do caminhão (em metros): '))
    largura = float(input('Largura do caminhão (em metros): '))
    altura = float(input('Altura do caminhão (em metros): '))
    peso_maximo = float(input('Peso máximo do caminhão (em kg): '))

    # iniciar Caminhão
    box = Bin(
        partno = 'Caminhão {}'.format(str(nome)),
        WHD=(largura,altura,comprimento),
        max_weight=peso_maximo,
        corner=15,
        put_type=0
    )

    packer.addBin(box)

#  adicionar itens
def ler_dados():  
    nome = input('Nome da Caixa: ')
    comprimento = float(input('Comprimento da caixa (em metros): '))
    largura = float(input('Largura da caixa (em metros): '))
    altura = float(input('Altura da caixa (em metros): '))
    peso = float(input('Peso da caixa (em kg): '))
    tipo = input("Qual o tipo de caixa? \n Cu = Cubo\n Ci = Cilindro\n")
    if tipo != "Cu" and tipo!= "Ci":
        while tipo != "Cu" and tipo!= "Ci":
            tipo = input("Qual o tipo de caixa? \n Cu = Cubo\n Ci = Cilindro\n")
    elif tipo =="Cu":
        tipo = "cube"
    else:
        tipo = "cylinder"

    rodar = int(input("A caixa pode ser rotacionada?\n 0 - Não \n 1 - Sim\n"))
    if rodar != 1 and rodar != 0:
        while rodar != 1 and rodar != 0:
            rodar = int(input("A caixa pode ser rotacionada?\n 0 - Não \n 1 - Sim\n"))
    elif rodar == 1:
        rodar = True
    else:
        rodar = False

    importancia = int(input("Insira o nível de importancia da caixa: \n 0 - Nenhum\n 1 - Alocar se possível \n 2 - Alocar \n 3 - Alocação Obrigatória\n"))
    quantidade = int(input('Qual a quantidade de caixas a ser transportada? '))
    cor = '#%06X' % round(random() * 0xffffff)
    for i in range(quantidade):
        packer.addItem(Item(
        partno='Caixa {}," ",{}'.format(str(nome),str(i+1)),
        name=nome, 
        typeof=tipo,
        WHD=(largura,altura,comprimento), 
        weight=peso,
        level=importancia,
        loadbear=100,
        updown=rodar,
        color=cor
        ))

def exibir_inventario():
    print("Em desenvolvimento")

# calcular a alocação
def alocar_caixas():
    packer.pack(bigger_first=True,
                distribute_items=False,
                fix_point=True,
                number_of_decimals=0)

# printar resultados
def plot_caminhao_e_caixas():
    b = packer.bins[0]
    volume = b.width * b.height * b.depth
    print(":::::::::::", b.string())

    print("Itens Alocados:")
    volume_t = 0
    volume_f = 0
    unfitted_name = ''
    for item in b.items:
        print("Partno : ",item.partno)
        print("Cor : ",item.color)
        print("Posição : ",item.position)
        print("Rotação : ",item.rotation_type)
        print("Dimensões (largura X altura X comprimento): ",str(item.width) +'*'+ str(item.height) +'*'+ str(item.depth))
        print("Volume : ",float(item.width) * float(item.height) * float(item.depth))
        print("Peso : ",float(item.weight))
        volume_t += float(item.width) * float(item.height) * float(item.depth)
        print("***************************************************")
    print("***************************************************")
    print("\n\n\n\n")
    print("***************************************************")
    print("Itens Não Alocados")
    for item in b.unfitted_items:
        print("Partno : ",item.partno)
        print("Cor : ",item.color)
        print("Dimensões (largura X altura X comprimento): ",str(item.width) +'*'+ str(item.height) +'*'+ str(item.depth))
        print("Volume : ",float(item.width) * float(item.height) * float(item.depth))
        print("Peso : ",float(item.weight))
        volume_f += float(item.width) * float(item.height) * float(item.depth)
        unfitted_name += '{},'.format(item.partno)
        print("***************************************************")
    print("***************************************************")
    print('Utilização de espaço : {}%'.format(round(volume_t / float(volume) * 100 ,2)))
    print('Volume residual : ', float(volume) - volume_t )
    print('Itens não alocados : ',unfitted_name)
    print('Volume de itens não alocados : ',volume_f)
    print("Distribuição de gravidade : ",b.gravity)
    stop = time.time()
    print('Tempo para alocação : ',stop - start)

    # Desenhar resultados em 3D
    painter = Painter(b)
    painter.plotBoxAndItems()


while True:
    print('\nEscolha uma opção:')
    print('1. Ler dados das caixas')
    print('2. Exibir inventário A DESENVOLVER')
    print('3. Adicionar caminhão')
    print('4. Alocar caixas')
    print('5. Plotar Resultado')
    print('6. Sair')

    opcao = input('Opção: ')

    if opcao == '1':
        ler_dados()
    elif opcao == '2':
        exibir_inventario()
    elif opcao == '3':
        adicionar_caminhao()
    elif opcao == '4':
        alocar_caixas()
    elif opcao == '5':
        plot_caminhao_e_caixas()
    elif opcao == '6':
        break
    else:
        print('Opção inválida. Por favor escolha uma opção válida.')