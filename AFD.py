# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# CC2019 Teoría de la computación
# Grupo#9 

from conversions import *

class AFD():
    def __init__(self, arbol):
        """"""

class Node():
    def __init__(self, symbol, no, pos = None):
        self.symbol = symbol
        self.no = no
        self.pos = pos
        self.nullable = False
        self.firstpos = []
        self.lastpos = []
        self.nextpos = []
        self.leftpos = 0
        self.rightpos = 0

        if pos:
            self.firstpos.append(pos)
            self.lastpos.append(pos)

        if (self.symbol == '*' or self.symbol == '?' or self.symbol == '$'):
            self.nullable = True
        
    def __repr__(self):
        return (self.symbol + ', ' + str(self.no) + ', ' + str(self.firstpos) + ', ' + str(self.lastpos) + ', ' + str(self.nullable))

    def set_firstpos(self, fp):
        self.firstpos = fp

    def set_lastpos(self, lp):
        self.lastpos = lp

    def set_nextpos(self, np):
        self.nextpos = np

    def set_left(self, left):
        self.leftpos = left

    def set_right(self, right):
        self.rightpos = right

    def get_symbol(self):
        return self.symbol

    def get_no(self):
        return self.no

    def get_pos(self):
        return self.pos

    def get_firstpos(self):
        return self.firstpos

    def get_lastpos(self):
        return self.lastpos

    def get_nextpos(self):
        return self.nextpos

    def left(self):
        return self.leftpos
    
    def right(self):
        return self.rightpos


class SyntaxTree():
    def __init__(self, expresion):
        self.regex = expresion
        self.elements = []
        self.stack = []
        self.dictionary = []
        self.tree = []

        # Conversión a posfix
        self.Obj = Conversion(self.regex)
        self.postfixExp = self.Obj.infixToPostfix()
        for a in (self.postfixExp):
            self.stack.append(a)

        # Obtención del diccionario
        for x in self.postfixExp:
            if (x not in '().*+|$'):
                self.elements.append(x)
                if (x not in self.dictionary):
                    self.dictionary.append(x)


        print("stack: ", self.stack)

        # creación de nodos
        self.nodes = []
        n = 0
        p = 1
        for x in (self.stack):
            temp = 0
            if (x not in '().*+|$'):
                temp = Node(x, n, p)
                n += 1
                p += 1
            else:
                temp = Node(x, n)
                n += 1
            self.nodes.append(temp)

        # Se le sa vuelta a los nodos
        self.nodes = list(reversed(self.nodes))

        for n in (self.nodes):
            print(n)
            """"""
        
        print()

        # Obtener el lado derecho e izquierdo de cada lado
        self.getLeftRight()


    def getLeftRight(self):
        
        # copia de nodes para saber cuáles ya se han asignado
        nodos_used = []

        for x in range(len(self.nodes)):
            no_nodo = self.nodes[x].get_no() #número del nodo 
            print()
            print(self.nodes[x])
            if (self.nodes[x].get_symbol() in '|?*+.'):
                
                # asignar lado derecho
                for n in self.nodes:
                    if (n.get_no() == no_nodo-1):
                        self.nodes[x].set_right(n)
                        # si es unario se agrega también como su lado izquierdo
                        if (self.nodes[x].get_symbol() in '?*+'):
                            self.nodes[x].set_left(n)
                        # se agrega a los nodos usados (para determinar la izquierda)
                        nodos_used.append(n)

                # asignar lado izquierdo
                check = True
                i = 1 # Se salta el primero porque es la raiz
                while (check):
                    # si ya fue usado antes (en la derecha), saltar
                    if (self.nodes[i] in nodos_used):
                        if (i < len(self.nodes)):
                            i += 1
                        # Si se pasa de la lista, salir del while
                        else:
                            check = False
                    
                    # si no ha sido utilizado
                    else:
                        # verificar que no sea unario y que no se le haya establecido un lado iquierdo antes
                        if (self.nodes[x].left() == 0):
                            """
                            Es necesario reforzar más esta parte para que no tome lados izquierdos de las
                            ramas de su lado derecho!!!
                            
                            """
                            self.nodes[x].set_left(self.nodes[i])
                            nodos_used.append(self.nodes[i])
                        check = False

                print("derecha: ", self.nodes[x].right())
                print("iz: ", self.nodes[x].left())

    def get_lastpos(self):
        """"""

r = '(a|b)*a#'
afd = SyntaxTree(r)
    