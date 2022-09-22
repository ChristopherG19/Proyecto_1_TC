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

# Método de simulación: Recibe una expresión regular y una cadena a evaluar
def SimulationAFN(r, w):
    # Se crea el AFN y se obtienen elementos del mismo
    Constr = Construction(r)
    AFN, Tiempo = Constr.Thompson_Construction()
    States = Constr.states
    AcceptState = []
    AcceptState.append(list(States)[-1])
    
    # Se inicia con el algoritmo de simulación
    # Se realiza E-closure del símbolo inicial
    S = e_closure(AFN, list(States)[0])
    cadena = []
    for i in w:
        cadena.append(i)    
    cadena.reverse()

    while(len(cadena) > 0):
        c = cadena.pop()  
        a = move(AFN, S, c)
        S = e_closure(AFN, a)

    # Si la cadena es aceptada se retornará "sí", de lo contrario "no"
    if (intersection(S, AcceptState) != []):
        return "si", Tiempo
    else:
        return "no", Tiempo  
    
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
