# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# CC2019 Teoría de la computación
# Grupo#9 
import re

class AFN():
    def __init__(self, expression):
        self.symbols = []
        self.transitions = []
        
        for i in expression:
            if(i.isalnum() or i == '&'):
                if(i not in self.symbols):
                    self.symbols.append(i)  
        
        #a = re.findall('\(.*?\)\**\+*', expression)
        #print(a)
            
        self.symbols = sorted(self.symbols)
        print(self.symbols)
    
        
    def emptyExp(self):
        0
        
    def symbolTransition(self):
        0
        
    def unionExp(self):
        0
    
    def concatExp(self):
        0
        
    def closureExp(self):
        0
    
    
        
r = "000(0|1)*"
r = "(b|b)abb(a|b)+000(0|11111)*000(0|1)*"
N = AFN(r)
