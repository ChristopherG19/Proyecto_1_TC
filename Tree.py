from asyncio.windows_events import NULL
from conversions import *
from node import *

class Tree():
    def __init__(self, regex):
        self.regex = regex
        self.stack = []
        self.Arbol = []
        self.States = []

        # revisar que tenga # al final de la cadena
        rrev = list(regex)
        rrev.reverse()
        if (rrev[0] != '#'):
            self.regex += '#'

        print(self.regex)    

        # conversión de regex de infix a posfix
        self.Obj = Conversion(self.regex)
        self.postfixExp = self.Obj.infixToPostfix()
        for a in (self.postfixExp):
            self.stack.append(a)

        self.check_leaves()

        self.look_for_children()

        self.checkNullability()

        self.generateFirstLastPos()

        self.followpos()

        self.generateStates()

    def __repr__(self):
        retString = ""
        for n in self.Arbol:
            retString += str(n) + '\n'
        return retString

    def check_leaves(self):

        pos = 0
        i = 0
        for e in self.stack:
            self.Arbol.append(Node(e))
            if (e not in '*+.?|'):
                # es una hoja del árbol
                self.Arbol[i].setAsLeaf()
                self.Arbol[i].setPos(pos)
                self.Arbol[i].addFirstPos(pos)
                self.Arbol[i].addLastPos(pos)
                pos += 1

            if (e in '*?'):
                self.Arbol[i].setNullable()

            i += 1

    def look_for_children(self):
        
        for i in range(len(self.Arbol)):
            # Operaciones binarias

            if (self.Arbol[i].getSymbol() in '+.|'):

                # derecha
                buscar = True
                i2 = 1                
                while (buscar and (i - i2) >= 0):
                    if (not self.Arbol[i - i2].isAsigned()):
                        # Asignar como nodo derecho
                        self.Arbol[i].setRight(self.Arbol[i - i2])
                        self.Arbol[i - i2].setAsign()
                        # Finalizar el ciclo while
                        buscar = False
                    # Si ya está asingado, regresar una posición
                    i2 += 1

                # izquierda
                buscar = True
                i2 = 2
                while (buscar and (i - i2) >= 0):
                    if (not self.Arbol[i - i2].isAsigned()):
                        # Asignar como nodo derecho
                        self.Arbol[i].setLeft(self.Arbol[i - i2])
                        self.Arbol[i - i2].setAsign()
                        # Finalizar el ciclo while
                        buscar = False
                    # Si ya está asingado, regresar una posición
                    i2 += 1

            # Operaciones unarias
            elif (self.Arbol[i].getSymbol() in '*?+'):

                # derecha e izquierda
                buscar = True
                i2 = 1
                while (buscar and (i - i2) >= 0):
                    if (not self.Arbol[i - i2].isAsigned()):
                        # Asignar como nodo derecho e izquierdo
                        self.Arbol[i].setRight(self.Arbol[i - i2])
                        self.Arbol[i].setLeft(self.Arbol[i - i2])
                        self.Arbol[i - i2].setAsign()
                        # Finalizar el ciclo while
                        buscar = False
                    # Si ya está asingado, regresar una posición
                    i2 += 1

    def checkNullability(self):
        
        for n in self.Arbol:
            if (not n.isLeaf()):
                if (n.getLeft().isNullable() and n.getRight().isNullable()):
                    # Por ende, también es nullable la concatenación
                    n.setNullable()

    def generateFirstLastPos(self):
        
        for n in self.Arbol:
            if (not n.isLeaf()):
                if (n.getSymbol() == '|'):

                    # firstpos = {iz} U {der}
                    for fp in n.getLeft().firstpos:
                        n.addFirstPos(fp)
                    for fp in n.getRight().firstpos:
                        n.addFirstPos(fp)

                    # lastpos = {iz} U {der}
                    for fp in n.getLeft().lastpos:
                        n.addLastPos(fp)
                    for fp in n.getRight().lastpos:
                        n.addLastPos(fp)

                if (n.getSymbol() in '*?+'):

                    # fistpos 
                    for fp in n.getLeft().firstpos:
                        n.addFirstPos(fp)

                    # lastpos
                    for fp in n.getRight().lastpos:
                        n.addLastPos(fp)

                if (n.getSymbol() == '.'):
                    # fistpos 
                    if n.getLeft().isNullable():
                        for fp in n.getLeft().firstpos:
                            n.addFirstPos(fp)
                        for fp in n.getRight().firstpos:
                            n.addFirstPos(fp)

                    else:
                        for fp in n.getLeft().firstpos:
                            n.addFirstPos(fp)

                    # lastpos 
                    if n.getRight().isNullable():
                        for fp in n.getLeft().firstpos:
                            n.addLastPos(fp)
                        for fp in n.getRight().firstpos:
                            n.addLastPos(fp)

                    else:
                        for fp in n.getRight().firstpos:
                            n.addLastPos(fp)

    def followpos(self):
        
        for n in self.Arbol:
            if (n.getSymbol() == '.'):
                for pos in n.getLeft().lastpos:
                    
                    # Encontrar a qué nodo pertenece la posición
                    n_temp = 0
                    for i in range(len(self.Arbol)):
                        if (self.Arbol[i].getPos() == pos):
                            n_temp = i
                            break

                    # Añadir el firstpos del lado derecho
                    for i in n.getRight().firstpos:
                        self.Arbol[n_temp].addFollowPos(i)

            if (n.getSymbol() in '*+'):
                for pos in n.lastpos:
                    # Encontrar a qué nodo pertenece la posición
                    n_temp = 0
                    for i in range(len(self.Arbol)):
                        if (self.Arbol[i].getPos() == pos):
                            n_temp = i
                            break

                    # Añadir el firstpos del lado derecho
                    for i in n.firstpos:
                        self.Arbol[n_temp].addFollowPos(i)

    def generateStates(self):
        for n in self.Arbol:
            if (n.isLeaf()):
                self.States.append(n)

