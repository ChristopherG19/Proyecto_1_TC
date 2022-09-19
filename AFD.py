# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# CC2019 Teoría de la computación
# Grupo#9 

from Tree import *

class AFD():
    def __init__(self):
        self.afd = []
        self.EA = []
        self.Dstates = []
        self.Symbols = []

    def directConstruction(self, arbol):

        # Alfabeto de la expresión regex
        self.Symbols = self.detSymbols(arbol)
        # eliminamos '#' si lo trae
        self.Symbols.remove('#')

        # Firstpos de la raíz
        cant_n = len(arbol.Arbol)
        Dstates = []
        Dstates.append(arbol.Arbol[cant_n - 1].firstpos)

        Dstates_marked = []

        # [qi, e, qf]

        # Si no todos los estados de Dstates están marcados (en Dstates_marked) se continúa
        while (not all(t in Dstates_marked for t in Dstates)):
            for t in Dstates:
                # Se marca el estado actual
                Dstates_marked.append(t)

                for a in self.Symbols:
                    U = []

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

        # Determinamos estados de aceptación
        self.EA = [(len(arbol.States) - 1) in x for x in Dstates]

        # Renombramos los estados 
        newStates = ["q%s"%x for x in range(len(Dstates))]

        temp_afd = []
        for trans in self.afd:
            t = []
            for element in trans:
                if (element in Dstates):
                    t.append(newStates[Dstates.index(element)])
                else:
                    t.append(element)
            temp_afd.append(t)

        # Remplazamos
        self.afd = temp_afd

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
#r = '(aa|bb)*#'
#r = 'a(a|b)*#'
#r = '(a|b)|(abab)'
#r = '0(0|1)0#'
r = '0*(0*|1)1#'
arbol = Tree(r)
#print()
#print(arbol)
dfa = AFD()
dfa.directConstruction(arbol)
for x in dfa.afd:
    print(x)
