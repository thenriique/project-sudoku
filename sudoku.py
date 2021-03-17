## Imports
import copy
import sys
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
        if item == '\n':
            continue
        elif item == '.' :
            line.append(0)
        else:
            line.append(int(item))

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

def firstVertice(sudoku):
    i1 = 0
    i2 = 0

    for row in sudoku:
        for column in row:
            if column == 0:
                return (i1, i2)
            
            if i2 == 8 :
                i1 = i1 + 1
                i2 = 0
            else:
                i2 = i2 + 1

def nextPosition(position):
    if position < 89:
        return position + 1
    else:
        return -1

def numberValids(sudoku, vertice):
    numbers_valids = [1,2,3,4,5,6,7,8,9]
    
    for item in list(set(sudoku[vertice[0]])): # Itens preenchidos na linha selecionada
        if item != 0 and item in numbers_valids:
            numbers_valids.remove(item)

    for item in sudoku: # Itens preenchidos na coluna selecionada
        if item[vertice[1]] != 0 and item[vertice[1]] in numbers_valids:
            numbers_valids.remove(item[vertice[1]])

    x0 = ((int)(vertice[0] / 3)) * 3
    y0 = ((int)(vertice[1] / 3)) * 3
    for a in range(0,3): # Itens preenchidos na grade (3x3)
        for b in range(0,3):
            item = sudoku[x0 + a][y0 + b]
            if item != 0 and item in numbers_valids:
                numbers_valids.remove(item)
    
    return numbers_valids

def stateFinish(sudoku):
    iDistante = 0

    for row in sudoku:
        for column in row:
            if column == 0:
                iDistante = iDistante + 1

    return iDistante

def heuristic(sudoku, vertice):
    costFisish = stateFinish(sudoku)
    possibilits = 9 - len(numberValids(sudoku, vertice))

    return costFisish + possibilits

def bfs(sudoku, vertice): # Função de Busca por Largura 
    fila = []

    fila.append(copy.deepcopy(sudoku))
    while fila:
        first = fila[0] # Primeiro item da fila

        if vertice == (): # Finaliza busca e apresenta o primeiro resultado
            break

        if first[vertice[0]][vertice[1]] != 0: # Verifica se a posição já esta preenchida
            vertice = nextVertice(vertice)
            continue

        for item in numberValids(first, vertice): # Expande os próximos vertices
            aux = copy.deepcopy(first)
            aux[vertice[0]][vertice[1]] = item
            fila.append(aux)

        fila.remove(first)

    print(fila)

def dfs(sudoku, vertice):
    if vertice == (): # Finaliza busca e apresenta o primeiro resultado
        printSudoku(sudoku)
        return True
    
    if sudoku[vertice[0]][vertice[1]] != 0: # Verifica se a posição já esta preenchida
        return dfs(sudoku, nextVertice(vertice))
        
    for item in numberValids(sudoku, vertice): # Percorre a fila
        sudoku[vertice[0]][vertice[1]] = item
        if dfs(sudoku, nextVertice(vertice)) == True:
            return True
        sudoku[vertice[0]][vertice[1]] = 0



def aStar(sudoku, vertice):
    _list = []
    _visited = []

    _list.append({"node" : copy.deepcopy(sudoku), "nodeFather" : 0, "cost" : heuristic(sudoku, vertice)})

    while _list:
        first = _list[0]
        v = firstVertice(first["node"])
        
        if stateFinish(first["node"]) == 0:
            return first

        for item in numberValids(first["node"], v):
            aux = copy.deepcopy(first["node"])
            aux[v[0]][v[1]] = item

            if aux in _visited:
                continue

            if aux not in _list:
                _list.append({"node" : copy.deepcopy(aux), "nodeFather" : copy.deepcopy(first), "cost" : heuristic(aux, nextVertice(v))})

        _list.remove(first)
        _list.sort(key=lambda x: x.get('cost'))
        _visited.append(copy.deepcopy(first))
        



## Methods
def printSudoku(sudoku):
    global debug
    if debug == True:
        print(datetime.now(), ':', 'Busca finalizada')
    inline = ''
    for row in sudoku:
        for column in row:
            inline += str(column)

    print(inline)

def printMatriz(sudoku):
    for row in sudoku:
        print(row)

def main():
    global debug
    grids = [] 

    print (sys.argv)

    try:
        # Carregando registros do arquivo de entrada
        archive = ''

        if len(sys.argv) == 3 :
            archive = openArchive(sys.argv[2])
        else: 
            archive = openArchive()

        # Montando a grade 
        for line in archive:
            grids.append(generateMatriz(line))

        # Fechando o arqivo de entrada
        archive.close()
    except:
        print('Falha no carregamento do arquivo.')


    # Verifica se tem registros
    if len(grids) == 0:
        print('Arquivo vazio! Por favor insira registros.')
        exit()

    
    if len(sys.argv) >= 2:
        if sys.argv[1] == 'dfs': # Busca por Profundidade
            for grid in grids:
                if(debug == True):
                    print(datetime.now(), ':', 'Iniciando busca')
                dfs(grid, (0,0)) 
        elif sys.argv[1] == 'bfs': # Buscando por Largura
            for grid in grids:
                if(debug == True):
                    print(datetime.now(), ':', 'Iniciando busca')
                bfs(grid, (0,0)) 
        elif sys.argv[1] == 'aStar': # Busca A*
            for grid in grids:
                if(debug == True):
                    print(datetime.now(), ':', 'Iniciando busca')
                aStar(grid, (0,0)) 
        else:
            print('Falha no algoritmo definido.')  
    else:
        print('Algoritmo não especificado.')  

## Globals Variable
debug = False

## Init
main()