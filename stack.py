# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# CC2019 Teoría de la computación
# Grupo#9 

# Base de: https://www.geeksforgeeks.org/stack-set-2-infix-to-postfix/ 
# This code is contributed by Nikhil Kumar Singh(nickzuck_007)

class Stack():
    def __init__(self):
        self.stack = []
        
    def size(self):
        return len(self.stack)
        
    def isEmpty(self):
        return True if (self.size() == 0) else False
    
    def peek(self):
        return self.stack[-1] if (not self.isEmpty()) else "No Elements" 
    
    def pop(self):
        return self.stack.pop() if (not self.isEmpty()) else "No Elements" 
    
    def push(self, element):
        self.stack.append(element)
        
    def clear(self):
        self.stack = []
        
    def getElement(self, i):
        return self.stack[i]
        
    def __str__(self):
        for i in self.stack:
            print(i)