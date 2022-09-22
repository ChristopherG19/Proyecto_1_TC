# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# CC2019 Teoría de la computación
# Grupo#9 
from AFN_Generator import *

# Se crea un Alfabeto para nombrar estados
# Obtenido de: https://www.delftstack.com/es/howto/python/python-alphabet-list/
def listAlphabet():
    a = list(map(chr, range(97, 123)))
    new = []
    for i in a:
        new.append(i.upper())
    new.reverse()
    return new

# Método de subconjuntos para la conversión de AFN a AFD
def AFN_To_AFD_SC(r):
    # Se crea el AFN y se obtienen datos del mismo
    Constr = Construction(r)
    AFN, Tiempo = Constr.Thompson_Construction()
    States = Constr.states
    Last = list(States)[-1]
    Symbols = Constr.symbols
    
    # Se inicia con el algoritmo de los documentos de clase
    Dstates = []
    # Se obtienen e_closure del primer símbolo
    DstatesTemp = e_closure(AFN, list(States)[0])
    Dstates.append(DstatesTemp)
    Dstates_marked = []
    Dstates_marked_WS = []

    while (not all(t in Dstates_marked for t in Dstates)):
        for t in Dstates:
            # Se marca el estado actual
            Dstates_marked.append(t)

            for symbol in Symbols:
                
                U = e_closure(AFN, move(AFN, t, symbol))
                
                U.sort()
                
                if (U not in Dstates):
                    Dstates.append(U)
                
                AFN.append([t, symbol ,U])
                
                # Se agregan a una lista adicional los estados (inicio y los que alcanza) y el símbolo
                # Para hacer revisiones posteriormente
                if isinstance(t, int):
                    Dstates_marked_WS.append([[t], symbol ,U])
                else:
                    Dstates_marked_WS.append([t, symbol ,U])
    

    # Se crea un abecedario
    ABC = listAlphabet()
    NewStates = {}

    # Se eliminan elementos que no aportan nada al resultado final
    for i in Dstates_marked:
        if i == []:
            Dstates_marked.remove(i)
 
    # Se nombran los estados obtenidos
    for i in Dstates_marked:
        i.sort()
        NameState = ABC.pop()
        if i not in list(NewStates.values()):
            if isinstance(i, int):
                NewStates[NameState] = [i]
            else:
                NewStates[NameState] = i
                       
    NewStates2 = []
    KeysA = []
    KeysB = []
    
    # Se obtienen la cantidad de transiciones para evaluaciones posteriores
    n = 0
    for b in Dstates_marked_WS:
        if b[0] == [] and b[2] == []:
            n += 1
            
    realLen = len(Dstates_marked_WS)-n

    # Se obtienen los nombres de los Nodos A y B para cada transición
    for i in Dstates_marked_WS:
        for key,value in NewStates.items():
            if i[0] == value:
                KeysA.append(key)
                
    for i in Dstates_marked_WS:
        for key,value in NewStates.items():
            if i[2] == value:
                KeysB.append(key)
      
    # Se eliminan más elementos que no aportan al resultado
    for x in Dstates_marked_WS:
        if(x[0] == [] and x[2] == []):
            Dstates_marked_WS.remove(x)
    
    for x in Dstates_marked_WS:
        if(x[0] == [] and x[2] == []):
            Dstates_marked_WS.remove(x) 

    # Se evalua que no falten elementos, de caso contrario se agregan "conjuntos vacíos"
    
    if (len(KeysA) != realLen):
        for i in range(len(Dstates_marked_WS)):
            if (Dstates_marked_WS[i][0] != [] and Dstates_marked_WS[i][2] == []):
                KeysA.insert(i, None)
            elif (Dstates_marked_WS[i][0] != [] and Dstates_marked_WS[i][2] != []):
                continue
    
    if (len(KeysB) != realLen):
        for i in range(len(Dstates_marked_WS)):
            if (Dstates_marked_WS[i][0] != [] and Dstates_marked_WS[i][2] == []):
                KeysB.insert(i, None)
            elif (Dstates_marked_WS[i][0] != [] and Dstates_marked_WS[i][2] != []):
                continue

    # Se crean las transiciones finales con los estados renombrados
    for i in range(realLen):
        a = KeysA[i]
        b = Dstates_marked_WS[i][1]
        c = KeysB[i]
        NewStates2.append([a, b, c])
      
    # Se obtienen los estados de inicio y aceptación  
    InitState = list(NewStates.keys())[0]
    AcceptState = []
    for key,value in NewStates.items():
        if Last in value:
            AcceptState.append(key)

    return (InitState, AcceptState, NewStates2, r, Tiempo)

# Método que imprime los resultados
def printResultsAFD(InitState, AcceptState, NewStates2):
    # Se ajusta la impresión de las transiciones
    trans = []
    for t in range(len(NewStates2)):
        if (NewStates2[t][2] != None):
            x = '(' + str(NewStates2[t][0]) + ', ' + str(NewStates2[t][1]) + ', ' + str(NewStates2[t][2]) + ')'
            trans.append(x)
            
    # Se imprimen los resultados finales
    print("\nEstado de inicio =  ", InitState)
    print("Estados de aceptación = ", ", ".join(AcceptState))
    print("Transiciones: "+ " - ".join(trans))
    print()

# Método e_closure, extraído de los documentos de clase. 
# Se obtienen todos los estados que son alcanzados por epsilon    
def e_closure(AFN, states):
    Result = []
    pila = []  
    if (isinstance(states, int)):
        pila.append(states)
        Result.append(states)
    else:
        for i in states:
            pila.append(i)
            Result.append(i)
        pila.reverse()

    while len(pila) != 0:
        t = pila.pop()

        for trans in AFN:
            if (trans[0] == t and trans[1] == '$'):
                if (trans[2] not in Result):
                    Result.append(trans[2])
                    pila.append(trans[2])
    
    return Result

# Método move, extraído de los documentos de clase. 
# Se obtienen todos los estados que son alcanzados por el símbolo ingresado a partir de un estado
def move(AFN, states, symbol):
    NewStates = []
    pila = []  
    if (isinstance(states, int)):
        pila.append(states)
    else:
        for i in states:
            pila.append(i)
        pila.reverse()
        
    while (len(pila) > 0):
        t = pila.pop()
        for trans in AFN:
            if (trans[0] == t and trans[1] == symbol):
                if (trans[2] not in NewStates):
                    NewStates.append(trans[2])
                    
    return NewStates
