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

        # Remplazamos AFD para conseguir correcto
        self.afd = temp_afd

        # Guardamos todos los estados
        for x in self.afd:
            if(x[0] not in self.Dstates):
                self.Dstates.append(x[0])

        for x in self.afd:
            if(x[2] not in self.Dstates):
                self.Dstates.append(x[2])


    def simulation(self, w):

        if (type(w) != list):
            w = list(w)

        s = self.afd[0][0]
        i = 0
        

        while (i <= (len(w) - 1) and s):
            c = w[i]
            s = self.move(s, c)
            i += 1

        if (s == NULL or not self.EA[self.Dstates.index(s)]):
            print("no")

        else:
            print("sí")

    def move(self, state, char):
        newState = NULL # Retorna 
        for q in self.afd:
            #por cada estado en el AFD, buscar si alguno tiene transición con la letra
            if (q[0] == state):
                if (q[1] == char):
                    # Si hayn
                    newState = q[2]
        return newState


    def minimization(self):

        # separamos los estados de aceptación y los que no son
        G1 = [] # Estados de aceptación
        G2 = [] # Otros estados

        



    def detSymbols(self, arbol):
        Symbols = []
        for n in arbol.States:
            if (n.getSymbol() not in Symbols):
                Symbols.append(n.getSymbol())
        
        return Symbols


# _________________________________________
# pruebas 
# _________________________________________

#r = 'ab*ab*#'
#r = '(aa*)|(bb*)#'
#r = '(a|b)*(a|b)*a?#'

#r = '(aa|bb)*#'
#w = 'aabbaab'

#r = '(a(a|b)b)*#'
#w = 'abbaab'

r = 'a(a|b)*#'
w = 'aaab'

#r = 'a(a|b)*#'
#r = '(a|b)|(abab)'
#r = '0(0|1)0#'
#r = '0*(0*|1)1#'


arbol = Tree(r)
print()
print(arbol)
dfa = AFD()
dfa.directConstruction(arbol)
for x in dfa.afd:
    print(x)
print()
dfa.simulation(w)
