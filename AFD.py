# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# CC2019 Teoría de la computación
# Grupo#9 

from Tree import *

class AFD():
    def __init__(self):
        self.afd = []
        self.Dstates = []

    def directConstruction(self, arbol):

        # Alfabeto de la expresión regex
        Symbols = self.detSymbols(arbol)

        # Firstpos de la raíz
        cant_n = len(arbol.Arbol)
        Dstates = []
        Dstates.append(arbol.Arbol[cant_n - 1].firstpos)

        Dstates_marked = []

        # Si no todos los estados de Dstates están marcados (en Dstates_marked) se continúa
        while (not all(t in Dstates_marked for t in Dstates)):
            for t in Dstates:
                # Se marca el estado actual
                Dstates_marked.append(t)

                for a in Symbols:
                    U = []
                    if (a != '#'):
                        # Ignoramos el último #

                        # Buscamos en todo el árbol por las posiciones que tengan el símbolo
                        for x in t:
                            if arbol.States[x].getSymbol() == a:
                                # Si no está en el estado, se añade
                                for e in arbol.States[x].followpos:
                                    if (e not in U):
                                        U.append(e)
                        
                        if (len(U) > 0):
                            if (U not in Dstates):
                                Dstates.append(U)

                            self.afd.append([t, a, U])

        print('afd: ', self.afd)

        # Renombramos los estados 
        newStates = ["q%s"%x for x in range(len(Dstates))]
        
        for x in range(len(Dstates)):
            print(Dstates[x],'\t', newStates[x])

        temp_afd = []
        for trans in self.afd:
            t = []
            for element in trans:
                if (element in Dstates):
                    t.append(newStates[Dstates.index(element)])
                else:
                    t.append(element)
            temp_afd.append(t)

        self.afd = temp_afd
        print('afd: ', self.afd)


    def simulation(self):
        """"""

    def minimization(self):
        """"""


    def detSymbols(self, arbol):
        Symbols = []
        for n in arbol.States:
            if (n.getSymbol() not in Symbols):
                Symbols.append(n.getSymbol())
        
        return Symbols



# pruebas
#r = 'ab*ab*#'
#r = '(a|b)*(a|b)*a?#'
r = '(aa|bb)*#'
#r = 'a(a|b)*#'
#r = '(a|b)|(abab)'
arbol = Tree(r)
print()
print(arbol)
dfa = AFD()
dfa.directConstruction(arbol)
