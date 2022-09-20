# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# CC2019 Teoría de la computación
# Grupo#9 

from AFN_Generator import *

# r = "(b|b)*abb(a|b)*"
# w = "babbaaaa"

# Python program to illustrate the intersection
# of two lists in most simple way https://www.geeksforgeeks.org/python-intersection-two-lists/
def intersection(lst1, lst2):
	lst3 = [value for value in lst1 if value in lst2]
	return lst3

def Simulation(r, w):
    Constr = Construction(r)
    AFN = Constr.Thompson_Construction()
    States = Constr.states

    AcceptState = []
    AcceptState.append(list(States)[-1])
    
    S = e_closure(AFN, list(States)[0])
    cadena = []
    for i in w:
        cadena.append(i)    
    cadena.reverse()
    
    #print("S inicial: ", S)
    
    while(len(cadena) > 0):
        c = cadena.pop()  
        a = move(AFN, S, c)
        S = e_closure(AFN, a)
        #print(S)

    # print(FinalStates)
    if (intersection(S, AcceptState) != []):
        return "Si"
    else:
        return "No"   
    
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