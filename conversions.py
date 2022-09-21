# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# CC2019 Teoría de la computación
# Grupo#9

# Base de: https://www.geeksforgeeks.org/stack-set-2-infix-to-postfix/ 
# This code is contributed by Nikhil Kumar Singh(nickzuck_007)

from stack import *
from time import perf_counter

# Clase donde se realiza la conversión de Infix a Postfix
class Conversion(object):
    # Constructor que define valores para la precedencia y los operadores que se utilizan
    def __init__(self, expression):
        self.infix = expression
        self.precedencia = {'*': 5, '?': 5, '+': 5, '.': 4, '|': 3, '(': 0}
        self.operators = ['+', '*', '?', '|']
        
    # Retorna la precedencia de un valor
    def __getPrecedence__(self, element):
        if (self.precedencia.get(element) == None):
            return 5
        else:
            return self.precedencia.get(element)
        
    # Método que se enfoca en la conversión
    def infixToPostfix(self):
        postfixExp = ""
        postfixElements = ""
        CantElements = len(self.infix)
        
        # Se revisa la expresión y se agregan a un String temporal
        # que almacena la expresión con concatenaciones explícitas
        for element in range(CantElements):
            el1 = self.infix[element]
            if ((element + 1) < len(self.infix)):
                el2 = self.infix[element + 1]
                postfixElements += el1

                if ((el1 != '(') and (el2 != ')') and (el1 != '|') and (el2 not in self.operators)):
                    postfixElements += '.'
                
        postfixElements += self.infix[CantElements-1]
        
        stack = Stack()
        
        # Con ayuda de un stack se evalua el string temporal
        # y se ordena dependiendo de la precedencia 
        for i in postfixElements:
            if (i == '('):
                stack.push(i)
            
            elif (i == ')'):
                while (not stack.isEmpty() and stack.peek() != '('):
                    postfixExp += stack.pop()
                
                if (not stack.isEmpty() and stack.peek() != '('):
                    return -1
                else:
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
            
        # Se retorna la expresión en formato Postfix
        return postfixExp
    