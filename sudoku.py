## Imports
import copy
from datetime import datetime

## Functions
def openArchive(inputs = 'input.txt'): # Tratamento para a abertura do arquivo de entrada
    try:
        return open(inputs, 'r') # Lê o arquivo
    except:
        return open(inputs, 'w') # Caso não exista, cria um arquivo

def openArchiveMemory(typ = ''):
    if typ != '':
        return open('memory.txt', typ)
    else:
        return openArchive('memory.txt')
            

def generateMatriz(sudoku): # Gerador da grade do sudoku
    grid = []
    line = []

    i = 0
    for item in sudoku: # Percorre cada caractere
        line.append(item)

        if len(line) == 9: # Caso já tenha 9 caracteres, insere na grade e limpa o vetor 'line'
            grid.append(line)
            line = []
            i = -1

        i += 1

    return grid

def generateLine(sudoku): # Gerador da grade do sudoku
    line = ''

    for row in sudoku:
        for column in row:
            line += column

    line += '\n'

    return line

def nextVertice(vertice):
    if vertice == (8, 8) or vertice == ():
        return ()
    elif vertice[1] < 8:
        return (vertice[0], vertice[1] + 1)
    else:
        return (vertice[0] + 1, 0)

def nextPosition(position):
    if position < 89:
        return position + 1
    else:
        return -1

def numberValids(sudoku, vertice):
    numbers_valids = ['1','2','3','4','5','6','7','8','9']

    # Validação de item preenchido
    if sudoku[vertice[0]][vertice[1]] != '.':
        return '0'
    
    for item in list(set(sudoku[vertice[0]])): # Itens preenchidos na linha selecionada
        if item != '.' and item in numbers_valids:
            numbers_valids.remove(item)

    for item in sudoku: # Itens preenchidos na coluna selecionada
        if item[vertice[1]] != '.' and item[vertice[1]] in numbers_valids:
            numbers_valids.remove(item[vertice[1]])

    x0 = ((int)(vertice[0] / 3)) * 3
    y0 = ((int)(vertice[1] / 3)) * 3
    for a in range(0,3): # Itens preenchidos na grade (3x3)
        for b in range(0,3):
            item = sudoku[x0 + a][y0 + b]
            if item != '.' and item in numbers_valids:
                numbers_valids.remove(item)
    
    return numbers_valids

def bfs(sudoku, vertice): # Função de Busca por Largura 
    fila = []

    fila.append(copy.deepcopy(sudoku))
    while fila:
        first = fila[0] # Primeiro item da fila

        if vertice == (): # Finaliza busca e apresenta o primeiro resultado
            break

        if first[vertice[0]][vertice[1]] != '.': # Verifica se a posição já esta preenchida
            vertice = nextVertice(vertice)
            continue

        for item in numberValids(first, vertice): # Expande os próximos vertices
            aux = copy.deepcopy(first)
            aux[vertice[0]][vertice[1]] = item
            fila.append(aux)

        fila.remove(first)

    print(fila)


# def bfs(sudoku, vertice): # Função de Busca por Largura 
#     if vertice == (): # Finaliza busca e apresenta o primeiro resultado
#         printSudoku(sudoku)
#         return

#     if vertice == (0,0): # Preenche arquivo com o retorno do primeiro vertice
#         archive = openArchiveMemory('w')
#         for item in numberValids(sudoku, vertice):
#             sudoku[vertice[0]][vertice[1]] = item
#             archive.write(generateLine(sudoku))
#         archive.close()
#         bfs(sudoku, nextVertice(vertice))
#         return

#     fila = list()
#     archive_read = openArchiveMemory() # Le os registros do arquivo de memoria
#     fila.append(archive_read.readlines())
#     fila = fila[0]
#     archive_read.close()

#     if(generateMatriz(fila[0])[vertice[0]][vertice[1]] != '.'): # Valida se já existe registro nessa posição
#         bfs(generateMatriz(fila[0]), nextVertice(vertice))
#         return

#     archive_write = openArchiveMemory('w')
#     matriz = []
#     for sudoku in fila: # Abre os filhos dos registros
#         sudoku = generateMatriz(sudoku)
#         for item in numberValids(sudoku, vertice):
#             if item != '0':
#                  sudoku[vertice[0]][vertice[1]] = item
#                  matriz = generateLine(sudoku)
#             archive_write.write(matriz) # Escreve os filhos no arquivo de memória
#     archive_write.close()
    
#     bfs(generateMatriz(matriz), nextVertice(vertice)) # Vai para o próximo vertice


def dfs(sudoku, vertice):
    if vertice == (): # Finaliza busca e apresenta o primeiro resultado
        printSudoku(sudoku)
        return True
    
    if sudoku[vertice[0]][vertice[1]] != '.': # Verifica se a posição já esta preenchida
        return dfs(sudoku, nextVertice(vertice))
        
    for item in numberValids(sudoku, vertice): # Percorre a fila
        sudoku[vertice[0]][vertice[1]] = item
        if dfs(sudoku, nextVertice(vertice)) == True:
            return True
        sudoku[vertice[0]][vertice[1]] = '.'

## Methods
def printSudoku(sudoku):
    global debug
    if debug == True:
        print(datetime.now(), ':', 'Busca finalizada')
    inline = ''
    for row in sudoku:
        for column in row:
            inline += column

    print(inline)

def printMatriz(sudoku):
    for row in sudoku:
        print(row)

def main():
    global debug
    grids = [] 

    # Carregando registros do arquivo de entrada
    archive = openArchive()

    # Montando a grade 
    for line in archive:
        grids.append(generateMatriz(line))

    # Fechando o arqivo de entrada
    archive.close()

    # Verifica se tem registros
    if len(grids) == 0:
        print('Arquivo vazio! Por favor insira registros.\n')
        exit()

    # Buscando por Largura
    for grid in grids:
        if(debug == True):
            print(datetime.now(), ':', 'Iniciando busca')
        bfs(grid, (0,0))   

    # Busca por profundidade
    # for grid in grids:
    #     if(debug == True):
    #         print(datetime.now(), ':', 'Iniciando busca')
    #     dfs(grid, (0,0))           

## Globals Variable
debug = True

## Init
main()