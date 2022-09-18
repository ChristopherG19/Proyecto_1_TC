from asyncio.windows_events import NULL
from conversions import *

class Node():
    def __init__(self, symbol=NULL):
        self.symbol = symbol
        self.pos = '-'

        self.left = NULL
        self.right = NULL
        self.asigned = False
        self.nullable = False
        self.leaf = False

        self.firstpos = []
        self.lastpos = []
        self.followpos = []

    def __repr__(self):

        retString = ""
        if (type(self.left) == Node and type(self.right) == Node):
            retString = str(self.symbol) + ',\t' + str(self.pos) + ',\t' + str(self.nullable) + ',\t' + str(self.firstpos) + ',\t' + str(self.lastpos) + ',\t' + str(self.followpos) + ',\t' + self.left.getSymbol() + ',\t' + self.right.getSymbol()
        else:
            retString = str(self.symbol) + ',\t' + str(self.pos) + ',\t' + str(self.nullable) + ',\t' + str(self.firstpos) + ',\t' + str(self.lastpos) + ',\t' + str(self.followpos) 
        return retString

    def setAsLeaf(self):
        self.leaf = True

    def setAsign(self):
        self.asigned = True

    def setNullable(self):
        self.nullable = True

    def setPos(self, pos):
        self.pos = pos

    def setLeft(self, left):
        self.left = left

    def setRight(self, right):
        self.right = right

    def addFirstPos(self, n):
        self.firstpos.append(n)

    def addLastPos(self, n):
        self.lastpos.append(n)

    def addFollowPos(self, n):
        self.followpos.append(n)

    def isLeaf(self):
        return self.leaf

    def isAsigned(self):
        return self.asigned

    def isNullable(self):
        return self.nullable

    def getSymbol(self):
        return self.symbol

    def getPos(self):
        return self.pos

    def getLeft(self):
        return self.left

    def getLeftPos(self):
        return self.left.getPos()

    def getRight(self):
        return self.right

    def getRightPos(self):
        return self.right.getPos()

class Tree():
    def __init__(self, regex):
        self.regex = regex
        self.stack = []
        self.Arbol = []

        # conversión de regex de infix a posfix
        self.Obj = Conversion(self.regex)
        self.postfixExp = self.Obj.infixToPostfix()
        for a in (self.postfixExp):
            self.stack.append(a)

        self.check_leaves()

        self.look_for_children()

        self.generateFirstLastPos()

        # print nodes
        for a in self.Arbol:
            print(a)


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
# pruebas
r = 'a(a|b)*#'
arbol = Tree(r)

