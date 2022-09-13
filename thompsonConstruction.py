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
        self.acceptState = set()
        self.transitions = {}
        self.elementsPF = []
        self.countStates = 1
        self.initialState = set()
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
        
        self.getStates()
        self.PrintResults()
        
    def getStates(self):
        if (len(self.stack) != 0):
            start = self.stack.pop()
            if (start in self.symbols or start == '$'):
                return self.symbol(start)
            elif (start == '.'):
                ElA = self.getStates()
                ElB = self.getStates()
                return self.concatExp(ElA, ElB)
             
    def symbol(self, symbolN):
        Estado_A = self.countStates
        self.countStates += 1
        Estado_B = self.countStates
        self.states.add(Estado_A)
        self.states.add(Estado_B)
        
        t = (Estado_B, symbolN)
        self.transitions[Estado_A] = [t]
        self.transitions[Estado_B] = []
        
        self.stackAFN.push((Estado_A, Estado_B))
        return (Estado_A, Estado_B)
        
    def unionExp(self):
        0
    
    def concatExp(self, ElA, ElB):
        Estado_A = ElA[0]
        Estado_B = ElB[1]

        transition = (ElB[0], '$')
        
        self.transitions[ElA[1]].append(transition)
        
        return (Estado_A, Estado_B)
        
    def closureExp(self):
        0
        
    def PrintResults(self):
        #self.stackAFN.print()
        # print(self.postfixExp)
        # print(self.states)
        # print(self.symbols)
        # print(self.initialState)
        # print(self.acceptState)
        self.printT()
           
    def printT(self):
        print(self.transitions)
        for k in self.transitions:
            for a in self.transitions[k]:
                b = str(k) + ' - (' + str(a[1]) + ') -> '+str(a[0])
                print(b)
        
       
r = "01" #00.0.01|*.
N = AFN(r)
