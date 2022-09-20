# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# CC2019 Teoría de la computación
# Grupo#9 
from tkinter import N
from AFN_Generator import *

def listAlphabet():
    a = list(map(chr, range(97, 123)))
    new = []
    for i in a:
        new.append(i.upper())
    new.reverse()
    return new

def AFN_To_AFD_SC(r):
    Constr = Construction(r)
    AFN = Constr.Thompson_Construction()
    States = Constr.states
    Last = list(States)[-1]
    Symbols = Constr.symbols
    
    
    Dstates = []
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
                
                if (U not in Dstates):
                    Dstates.append(U)
                
                #Dstates_marked_WS[t] = (symbol, U)

                AFN.append([t, symbol ,U])
                if isinstance(t, int):
                    Dstates_marked_WS.append([[t], symbol ,U])
                else:
                    Dstates_marked_WS.append([t, symbol ,U])
    
    ABC = listAlphabet()
    NewStates = {}

    for i in Dstates_marked:
        if i == []:
            Dstates_marked.remove(i)
        
    for i in Dstates_marked:
        NameState = ABC.pop()
        if isinstance(i, int):
            NewStates[NameState] = [i]
        else:
            NewStates[NameState] = i

    NewStates2 = []
    KeysA = []
    KeysB = []
    
    n = 0
    for b in Dstates_marked_WS:
        if b[0] == [] and b[2] == []:
            n += 1
            
    realLen = len(Dstates_marked_WS)-n

    for i in Dstates_marked_WS:
        for key,value in NewStates.items():
            if i[0] == value:
                KeysA.append(key)
                
    for i in Dstates_marked_WS:
        for key,value in NewStates.items():
            if i[2] == value:
                KeysB.append(key)
      
    #Arreglar
    for x in Dstates_marked_WS:
        if(x[0] == [] and x[2] == []):
            Dstates_marked_WS.remove(x)
    
    for x in Dstates_marked_WS:
        if(x[0] == [] and x[2] == []):
            Dstates_marked_WS.remove(x) 
    
    if (len(KeysB) != realLen):
        for i in range(len(Dstates_marked_WS)):
            if (Dstates_marked_WS[i][0] != [] and Dstates_marked_WS[i][2] == []):
                KeysB.insert(i, None)
    
    for i in range(realLen):
        if Dstates_marked_WS[i][0] == [] and Dstates_marked_WS[i][2] == []:
            n -= 1
        
        a = KeysA[i]
        b = Dstates_marked_WS[i][1]
        c = KeysB[i]
        
        NewStates2.append([a, b, c])
        
    InitState = list(NewStates.keys())[0]
    AcceptState = []
    for key,value in NewStates.items():
        if Last in value:
            AcceptState.append(key)
    
    trans = []
    for t in range(len(NewStates2)):
        if (NewStates2[t][2] != None):
            x = '(' + str(NewStates2[t][0]) + ', ' + str(NewStates2[t][1]) + ', ' + str(NewStates2[t][2]) + ')'
            trans.append(x)
    
    print("\nEstado de inicio =  ", InitState)
    print("Estados de aceptación = ", ", ".join(AcceptState))
    print("Transiciones: "+ " - ".join(trans))
    print()
    
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

r = "a|b"
AFN_To_AFD_SC(r)
