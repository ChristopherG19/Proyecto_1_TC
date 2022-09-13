# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# CC2019 Teoría de la computación
# Grupo#9 

#Base de construcción de Thompson: https://medium.com/swlh/visualizing-thompsons-construction-algorithm-for-nfas-step-by-step-f92ef378581b
from conversions import *
from stack import *

class AFN():
    def __init__(self, expression):
        self.expression = expression
        self.states = set()
        self.symbols = []
        self.transitions = []
        self.elementsPF = []
        self.countStates = 1
        self.stack = []
        self.stackAFN = Stack()
        
        # Se obtienen los símbolos del alfabeto
        # $ representa epsilon
        for i in expression:
            if(i not in '().*+|$' and i not in self.symbols):
                self.symbols.append(i)  
        self.symbols = sorted(self.symbols)
        
        self.Obj = Conversion(expression, self.symbols)
        self.postfixExp = self.Obj.infixToPostfix()
        
        for a in (self.postfixExp):
            self.stack.append(a)

        #print(self.postfixExp)
        #print(self.stack)

        self.Thompson_Construction()
        
    def Thompson_Construction(self): 
        
        self.prueba()
        self.initialState, self.acceptState = list(self.transitions)[0][0], list(self.transitions)[-1][-1]
        self.PrintResults()
        
        
    def prueba(self):
        exp = self.postfixExp
        
        for a in range(len(exp)):
            if (exp[a] in self.symbols or exp[a] == '$'):
                self.symbol(exp[a])
            elif (exp[a] == '.'):
                ElA = exp[a-1]
                ElB = exp[a-2]
                self.concatExp(ElB, ElA)
        
        
    def getStates(self):
        if (len(self.stack) != 0):
            start = self.stack.pop()
            if (start in self.symbols or start == '$'):
                return self.symbol(start)
            elif (start == '.'):
                ElA = self.getStates()
                ElB = self.getStates()
                self.concatExp(ElB, ElA)
             
    def symbol(self, symbolN):
        Estado_A = self.countStates
        self.countStates += 1
        Estado_B = self.countStates
        self.states.add(Estado_A)
        self.states.add(Estado_B)
        
        temp = [Estado_A, symbolN, Estado_B]
        trans = [str(x) for x in temp]
        self.transitions.append(trans)
        
        self.stackAFN.push((Estado_A, Estado_B))
        
    def concatExp(self, ElA, ElB):
        Estado_A = ElA
        Estado_B = ElB
        return (Estado_A, Estado_B)
        
    def unionExp(self):
        0
        
    def closureExp(self):
        0
        
    def PrintResults(self):
        print("\nInfix Expression:", self.expression)
        print("PostFix Expression:", self.postfixExp)
        print("Estados: ", self.states)
        print("Simbolos: ", self.symbols)
        print("Inicio: ", self.initialState)
        print("Aceptacion: ", self.acceptState)
        self.printT()
           
    def printT(self):
        x = ""
        Transitions = []
        for k in self.transitions:
            x = '(' + k[0] + ', ' + k[1] + ', ' + k[2] + ')'
            Transitions.append(x)
            
        print("Transiciones: "+ " - ".join(Transitions))
        print()
        
r = "000111" #00.0.01|*.
N = AFN(r)
