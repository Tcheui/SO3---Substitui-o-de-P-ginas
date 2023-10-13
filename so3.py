"""SO3 - GABRIEL TOSHIYUKI  BATISTA TOYODA 22153164.ipynb
"""

#GABRIEL TOSHIYUKI BATISTA TOYODA - 22153164
#python so3.py (tamanho da memória) (arquivo.txt)
import sys
TAMANHO_MEMORIA = int(sys.argv[1]) #tamanho máximo da memória (frame)

def checaPresenca(memoria, pagina, processo): #checa se determinada pagina e processo
#estão na memória
  elemento = []
  elemento.append(processo)
  elemento.append(pagina)

  for i, item in enumerate(memoria):
    if(elemento[0] == item[0] and elemento[1] == item[1]):
      return True
  return False

def ondeEsta(memoria, pagina, processo): #dada a pagina e o processo, retorna a posição
#na memoria
  elemento = []
  elemento.append(processo)
  elemento.append(pagina)

  for i, item in enumerate(memoria):
    if(elemento[1] == item[1] and elemento[0] == item[0]):
      return i
  return -1

def separaEntrada(string): #usada para referencia de quem chega em cada
#momento, essa lista será sem limites
  memoria = []
  duplas = string.split(";")
  duplas.pop() #remove o ultimo elemento, já que a string de referencia termina em ';'
  #resultando no ultimo espaço vazio

  for item in duplas:
    dupla = item.split(",")

    lista = []
    lista.append(int(dupla[0])) #processo
    lista.append(int(dupla[1])) #pagina

    memoria.append(lista)

  return memoria

def contaFaultsFIFO(memoria, string): #retorna inteiro contendo o
#numero de page faults
  duplas = string.split(";")
  duplas.pop() #remove o ultimo elemento, já que a string de referencia termina em ';'
  if(duplas[len(duplas) - 1] == '0,0'):
    duplas.pop()
  faults = 0

  for item in duplas:
    dupla = item.split(",")
    lista = []
    lista.append(int(dupla[0])) #processo
    lista.append(int(dupla[1])) #pagina

    if((not checaPresenca(memoria, lista[1], lista[0]))): # se der page fault
      #print('FAULT')
      faults += 1
      if(len(memoria) >= TAMANHO_MEMORIA): # se a memoria estiver cheia
        oldest = memoria.pop() # remove o ultimo da memoria (mais antigo)

      memoria.insert(0, lista) #insere no topo da lista
    #print(memoria)

  return faults

def contaFaultsLRU(memoria, string):
  duplas = string.split(";")
  duplas.pop() #remove o ultimo elemento, já que a string de referencia termina em ';'
  if(duplas[len(duplas) - 1] == '0,0'):
    duplas.pop()
  faults = 0

  for item in duplas:
    dupla = item.split(",")
    lista = []
    lista.append(int(dupla[0])) #processo
    lista.append(int(dupla[1])) #pagina
    if((not checaPresenca(memoria, lista[1], lista[0]))): # se der page fault
      #print("FAULT")
      faults += 1
      if(len(memoria) >= TAMANHO_MEMORIA): # se a memoria estiver cheia
        memoria.pop() #remove o último elemento (menos usado)
        memoria.insert(0, lista) #insere o novo no topo da lista

      else: memoria.insert(0, lista) # se não, insere no topo

    else: #se estiver presente...
      i = ondeEsta(memoria, lista[1], lista[0])
      memoria.pop(i) #passa o elemento pro topo da memoria
      memoria.insert(0, lista) #indicando que foi usado recentemente
    #print(memoria)

  return faults

def contaFaults2ndChance(memoria, string):
  #numero de page faults
  duplas = string.split(";")
  duplas.pop() #remove o ultimo elemento, já que a string de referencia termina em ';'
  if(duplas[len(duplas) - 1] == '0,0'):
    duplas.pop()
  faults = 0

  segunda_chance = [] #vetor de segunda chance, composto de 0's até que uma pagina
  #seja referenciada, definindo a posição equivalente em 1 até que a página seja
  #escolhida para ser removida, definindo 0 novamente.

  for item in duplas:
    dupla = item.split(",")
    lista = []
    lista.append(int(dupla[0])) #processo
    lista.append(int(dupla[1])) #pagina

    if((not checaPresenca(memoria, lista[1], lista[0]))): # se der page fault
      #print("FAULT")
      faults += 1
      if(len(memoria) >= TAMANHO_MEMORIA): # se a memoria estiver cheia
        i = len(memoria) - 1 #ultima posição (primeira escolha do FIFO)

        while(segunda_chance[i] == 1):
          segunda_chance[i] = 0 # vetor salvo! define 0 na posição equivalente
          i -= 1 # passa pro próximo a ser removido

        memoria.pop(i) # remove da lista

      memoria.insert(0, lista) #insere no topo da lista
      segunda_chance.insert(0, 0)

    else: #se estiver presente...
      i = ondeEsta(memoria, lista[1], lista[0])
      segunda_chance[i] = 1 #coloca 1 no bit de referencia no vetor de segunda chance
    #print(memoria)

  return faults

if(len(sys.argv) > 3):
  exit()

file_path = sys.argv[2]
string = ""
with open(file_path, 'r') as file:
    for line in file:
        string += line

memoria = []  # vetor limitado a 8000 posições, cada posição equivale a 4KB (total sendo 32MB)
  # a memória é representada por uma lista de dicionários de keys Pagina, Processo
print("Page Faults FIFO: " + str(contaFaultsFIFO(memoria, string)))
memoria = []
print("Page Faults LRU: " + str(contaFaultsLRU(memoria, string)))
memoria = []
print("Page Faults 2nd Chance: " + str(contaFaults2ndChance(memoria, string)))

