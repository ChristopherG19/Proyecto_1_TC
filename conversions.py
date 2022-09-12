# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# CC2019 Teoría de la computación
# Grupo#9

# Base de: https://www.geeksforgeeks.org/stack-set-2-infix-to-postfix/ 
# This code is contributed by Nikhil Kumar Singh(nickzuck_007)

from stack import *

class Conversion(object):
    def __init__(self, expression):
        self.symbols = []
        self.infix = expression
        self.precedencia = {'(': 0, '+': 1, '?': 1, '*': 1, '|': 2, '.': 3}
        self.operators = ['+', '*', '?', '|']
        
        # Se obtienen los símbolos del alfabeto
        # $ representa epsilon
        for i in expression:
            if(i not in '().*+|$' and i not in self.symbols):
                self.symbols.append(i)  
        
        self.symbols = sorted(self.symbols)

    def __getSymbols__(self):
        return self.symbols
    
    def __getExpression__(self):
        return self.infix
    
    def __getPrecedence__(self, element):
        if (self.precedencia.get(element) == None):
            return 4
        else:
            return self.precedencia.get(element)
        
    def infixToPostfix(self):
        postfixExp = ""
        postfixElements = ""
        CantElements = len(self.infix)
        
        for element in range(CantElements):
            el1 = self.infix[element]
            
            if ((element + 1) < len(self.infix)):
                el2 = self.infix[element + 1]
                postfixElements += el1
                
                if ((el1 != '(') and (el2 != ')') and (el1 not in self.operators) and (el2 not in self.operators)):
                    postfixElements += '.'
                
        postfixElements += self.infix[CantElements-1]
        print(postfixElements)
        
        stack = Stack()
        
        for i in postfixElements:
            if (i == '('):
                stack.push(i)
            
            elif (i == ')'):
                while (not stack.isEmpty() and stack.peek() != '('):
                    postfixExp += stack.pop()
                stack.pop()
                
            else:
                while (not stack.isEmpty()):
                    element = stack.peek()
                    precedenceElement = self.__getPrecedence__(element)
                    precedenceActualEl = self.__getPrecedence__(i)
                    
                    if (precedenceElement >= precedenceActualEl):
                        postfixExp += stack.pop()
                    else:
                        break
                    
                stack.push(i)

        while (not stack.isEmpty()):
            postfixExp += stack.pop()
            

        print(postfixExp)
        
r = "(b|b)abb(a|b)"
r2 = "000(0|1)"
a = Conversion(r2)
a.infixToPostfix()