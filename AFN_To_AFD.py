# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# CC2019 Teoría de la computación
# Grupo#9 

#Base de construcción de Thompson: https://medium.com/swlh/visualizing-thompsons-construction-algorithm-for-nfas-step-by-step-f92ef378581b

#Import de los otros archivos
from conversions import *
from stack import *

#Clase Estado que explica NodoA - (transicion(simbolo)) -> NodoB
class State():    
    #Empieza con Null por defecto
    NodoA = None
    NodoB = None
    transicion = None
    
    # Constructor para asignar valores, si no recibe simbolo de 
    # transición utiliza epsilon
    def __init__(self, NoA, NoB, symbol=None):
        self.NodoA = NoA
        self.NodoB = NoB
        self.transicion = symbol or '$'
    
    #Setters
    def changeNodoA(self, newNoA):
        self.NodoA = newNoA
        
    def changeNodoB(self, newNoB):
        self.NodoB = newNoB
    
    #Método para obtener el string de la transición en formato solicitado
    def __str__(self):
        return '(' + str(self.NodoA) + ', ' + str(self.transicion) + ', ' + str(self.NodoB) + ')'

#Clase Construction que se encarga del desarrollo del AFN (Thompson en este caso)
class Construction():
    
    #Constructor que crea arrays y stacks necesarios para almacenar toda la información
    def __init__(self, expression):
        self.exp = expression
        self.stackAFN = Stack()
        self.countStates = 0
        self.states = set()
        self.symbols = []
        self.transitions = {}
        
        # Se obtienen los símbolos del alfabeto y se ordenan
        # $ representa epsilon
        for i in expression:
            if(i not in '().*+|$' and i not in self.symbols):
                self.symbols.append(i)  
        self.symbols = sorted(self.symbols)
        
        #Se obtiene la expresión en postfix
        self.Obj = Conversion(expression)
        self.postfixExp = self.Obj.infixToPostfix()
        
        #Se llama el método de Thompson
        self.Thompson_Construction()
        
    #Método Thompson: Construye el AFN con Thompson
    def Thompson_Construction(self):
        print("\nPostfix: ",self.postfixExp)
        #Lee cada elemento de la expresion en postfix
        for element in self.postfixExp:
            #print(element)
            #Dependiendo del elemento trabaja una operación diferente
            if (element in self.symbols or element == '$'):
                self.symbol(element)
            elif (element == '.'):
                if (self.stackAFN.size()-1 > 0):
                    AFN_B = self.stackAFN.pop()
                    AFN_A = self.stackAFN.pop()
                    self.concatExp(AFN_B, AFN_A)
            elif (element == '|'):
                if (self.stackAFN.size()-1 > 0):
                    AFN_B = self.stackAFN.pop()
                    AFN_A = self.stackAFN.pop()
                    self.unionExp(AFN_B, AFN_A)
        
        #print(self.transitions)
        print()
        Init = list(self.states)[0]
        Last = list(self.states)[-1]
        print("Estado de inicio: ",Init)
        print("Estado de aceptacion: ",Last)
        print("Cant. Estados: ",Last)
        self.printT()
        print()
        #self.stackAFN.__str__()
        
    def printT(self):
        x = ""
        Transitions = []

        for k in self.transitions:
            for y in self.transitions[k]:
                x = '(' + str(k) + ', ' + str(y[0]) + ', ' + str(y[1]) + ')'
                Transitions.append(x)
            
        print("Transiciones: "+ " - ".join(Transitions))
    
    def symbol(self, element):
        #Con ayuda del contador de estados se "nombran" los mismos
        self.countStates += 1
        Estado_A = self.countStates
        self.countStates += 1
        Estado_B = self.countStates
        
        #Se crea un estado con el estadoA, estadoB y la transición entre ambos
        EstadoSymbol = State(Estado_A, Estado_B, element)

        #Se agregan al listado de estados
        self.states.add(Estado_A)
        self.states.add(Estado_B)
        
        #Se agregan al estado de "AFN's" disponibles para otras operaciones
        self.stackAFN.push(EstadoSymbol)
        
        #print("Symbol: ",EstadoSymbol.__str__())
        
        #Se agrega la transición al array de transiciones
        self.transitions[Estado_A] = [(element, Estado_B)]
        self.transitions[Estado_B] = []
        
    #Recibe dos AFN's para trabajar
    def concatExp(self, ElB, ElA):
        '''
            De momento estoy revisando el tema del conteo de estados
            y transiciones pero en este método se concatenan los estados 
            y se agrega el nuevo AFN resultante al stack
        '''
        EstadoConcatA = State(ElA.NodoA, ElA.NodoB, ElA.transicion)
        self.countStates -= 1
        ElB.changeNodoB(self.countStates)
        EstadoConcatB = State(ElA.NodoB, ElB.NodoB, ElB.transicion)
        
        self.stackAFN.push(EstadoConcatA)
        self.stackAFN.push(EstadoConcatB)
        
        self.transitions[ElB.NodoB] = []
        self.transitions[ElA.NodoB] = [(ElB.transicion, ElB.NodoA)]
        
        #print(EstadoConcatA.__str__())
        #print(EstadoConcatB.__str__())
    
    #Recibe dos AFN's para trabajar
    def unionExp(self, ElB, ElA):
        '''
            De momento estoy revisando el tema del conteo de estados
            y transiciones pero en este método se crearan las transiciones
            con epsilon a los estados iniciales de los AFN's entrantes y desde
            los estados finales al estado de aceptación y se agrega el 
            nuevo AFN resultante al stack, al igual que las transiciones
        '''
        a = max(ElA.NodoA, ElA.NodoB,ElB.NodoA, ElB.NodoB) - 1
        
        ElA.changeNodoA(ElB.NodoA-1)
        ElA.changeNodoB(ElB.NodoB-1)
        ElB.changeNodoA(ElB.NodoA+1)
        ElB.changeNodoB(ElB.NodoB+1)
         
        Estado_A = self.countStates - a
        Estado_B = ElB.NodoB+1
                
        #print(Estado_A,ElA.NodoA,ElA.NodoB,ElB.NodoA,ElB.NodoB, Estado_B)
        
        Estado_C = State(Estado_A, ElA.NodoA, '$')
        Estado_D = State(Estado_A, ElB.NodoA, '$')
        Estado_E = State(ElA.NodoB, Estado_B, '$')
        Estado_F = State(ElB.NodoB, Estado_B, '$')
        
        self.states.add(Estado_A)
        self.states.add(Estado_B)
        self.states.add(ElA.NodoA)
        self.states.add(ElA.NodoB)
        self.states.add(ElB.NodoA)
        self.states.add(ElB.NodoB)
        
        self.stackAFN.push(Estado_C)
        self.stackAFN.push(ElA)
        self.stackAFN.push(Estado_E)
        self.stackAFN.push(Estado_D)
        self.stackAFN.push(ElB)
        self.stackAFN.push(Estado_F)
        
        #self.stackAFN.__str__()
        
        self.transitions[Estado_A] = [('$', ElA.NodoA)]
        self.transitions[ElA.NodoA] = [(ElA.transicion, ElA.NodoB)]
        self.transitions[ElB.NodoA] = [(ElB.transicion, ElB.NodoB)]
        self.transitions[Estado_A].append(('$', ElB.NodoA))
        self.transitions[ElA.NodoB] = [('$', Estado_B)]
        self.transitions[ElB.NodoB] = [('$', Estado_B)]
        
        
  
r = "(0|1)01" #00.0.01|*.
N = Construction(r)      