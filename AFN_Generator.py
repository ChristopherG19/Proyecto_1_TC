# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# CC2019 Teoría de la computación
# Grupo#9

# Base de construcción de Thompson: https://medium.com/swlh/visualizing-thompsons-construction-algorithm-for-nfas-step-by-step-f92ef378581b

# Import de los otros archivos
from inspect import Traceback
from conversions import *
from stack import *
from operator import itemgetter

epsilon = '$'

class Construction:
    def __init__(self, expression):
        self.expression = expression
        self.states = set()
        self.symbols = []
        self.transitions = []
        self.stackAFN = []
        self.AFN = []
        self.numEstados = 0

    def Thompson_Construction(self):

        # Se obtienen los símbolos del alfabeto y se ordenan
        # $ representa epsilon
        for i in self.expression:
            if(i not in '().*+|$?' and i not in self.symbols):
                self.symbols.append(i)
        self.symbols = sorted(self.symbols)

        #Se obtiene la expresión en postfix
        self.Obj = Conversion(self.expression)
        self.postfixExp = self.Obj.infixToPostfix()

        for element in self.postfixExp:
            #print(self.states, element)
            #Dependiendo del elemento trabaja una operación diferente
            #print("\nAFNS: ",self.stackAFN, "\nEl: ", element)
            if (element in self.symbols or element == '$'):
                NewAFN = self.symbol(element)
                self.stackAFN.append(NewAFN)
            elif (element == '.'):
                A = self.stackAFN.pop()
                B = self.stackAFN.pop()
                NewAFN = self.ConcatExp(B, A)
                self.stackAFN.append(NewAFN)
            elif (element == '|'):
                A = self.stackAFN.pop()
                B = self.stackAFN.pop()
                NewAFN = self.UnionExp(B, A)
                self.stackAFN.append(NewAFN)
            elif (element in '*+?'):
                A = self.stackAFN.pop()
                if (len(self.stackAFN) > 0):
                    Comprobacion = self.stackAFN.pop()
                    if (not isinstance(Comprobacion[0], int) and not isinstance(A[0], int)):
                        if (Comprobacion[-1][0] == A[0][0] and Comprobacion[-1][2] == A[0][2]):
                            NTransitions = []

                            for trans in A:
                                NTransitions.append([trans[0]+1, trans[1], trans[2]+1])

                            A = NTransitions

                        self.stackAFN.append(Comprobacion)
                    elif (isinstance(Comprobacion[0], int) and not isinstance(A[0], int)):
                        if (Comprobacion[0] == A[0][0] and Comprobacion[2] == A[-1][2]):
                            NTransitions = []

                            for trans in A:
                                NTransitions.append([trans[0]+1, trans[1], trans[2]+1])

                            A = NTransitions

                        self.stackAFN.append(Comprobacion)
                    elif (not isinstance(Comprobacion[0], int) and isinstance(A[0], int)):
                        if (Comprobacion[-1][0] == A[0] and Comprobacion[-1][2] == A[2]):
                            NTransitions = []

                            for trans in A:
                                NTransitions.append([trans[0]+1, trans[1], trans[2]+1])

                            A = NTransitions

                        self.stackAFN.append(Comprobacion)
                    elif (isinstance(Comprobacion[0], int) and isinstance(A[0], int)):
                        if (Comprobacion[0] == A[0] and Comprobacion[2] == A[2]):
                            NTransitions = []

                            for trans in A:
                                NTransitions.append([trans[0]+1, trans[1], trans[2]+1])

                            A = NTransitions

                        self.stackAFN.append(Comprobacion)

                NewAFN = self.KleeneExp(A)
                if (not isinstance(NewAFN, int) and self.stackAFN != []):
                    if (NewAFN[0][0] == self.stackAFN[0][0] and NewAFN[1][1] != self.stackAFN[1][1] and NewAFN[-1][-1] == self.stackAFN[-1][-1]):
                        temp = []
                        for trans in NewAFN:
                            temp.append([trans[0]-1, trans[1], trans[2]-1])
                        
                        NewAFN = temp
                    
                self.stackAFN.append(NewAFN)

        AFN = self.stackAFN.pop()
        # Para imprimir resultados en dado caso se pruebe desde este archivo
        # Descomentar línea siguiente: 
        self.CheckStates(AFN)
        #self.printResults(AFN)
        if len(AFN) == 3 and isinstance(AFN[0], int):
            SortedAFN = AFN
        else:
            SortedAFN = sorted(AFN, key=itemgetter(0, 2))

        return SortedAFN

    def symbol(self, symbolT):
        self.numEstados += 1
        NodoA = self.numEstados
        self.numEstados += 1
        NodoB = self.numEstados
        self.states.add(NodoA)
        self.states.add(NodoB)

        NewEstado = [NodoA, symbolT, NodoB]

        return NewEstado

    def ConcatExp(self, AFN_A, AFN_B):
        # print("\nA: ", AFN_A)
        # print("\nB: ", AFN_B)
        self.numEstados -= 1
        AFN_C = []
        if (isinstance(AFN_A[0], int)):
            Start = AFN_A[0]-1
        else:
            Start = AFN_A[0][0]-1

        if (not isinstance(AFN_A[0], int) and not isinstance(AFN_B[0], int)):
            if (AFN_A[-1][0] == AFN_B[0][0] and AFN_A[-1][2] == AFN_B[0][2]):
                NTransitions = []

                for trans in AFN_B:
                    NTransitions.append([trans[0]+1, trans[1], trans[2]+1])

                AFN_B = NTransitions
                self.states.add(AFN_B[-1][-1])

        if (len(AFN_A) > len(AFN_B) and len(AFN_A) != 3 and len(AFN_B) != 3):
            self.states.add(Start)
            self.states.remove(list(self.states)[-1])
            #NewEstado = [AFN_B[0][0], AFN_B[1][1], AFN_B[0][0]+1]
            # if (AFN_B[0][0]-1 == AFN_A[-1][2]):
            #     temp2 = []
            #     for trans in AFN_B:
            #         temp2.append([trans[0]-1, trans[1], trans[2]-1])
            #     AFN_B = temp2
            #     self.states.remove(list(self.states)[-1])

            AFNB = sorted(AFN_B, key=itemgetter(0))
            AFN_B = AFNB
            #print("CO: ",AFN_B)

            for a in AFN_B:
                self.states.add(a[0])
                self.states.add(a[2])
                AFN_A.append(a)
            #AFN_A.append(NewEstado)
            AFN_C = AFN_A

        elif (len(AFN_A) > len(AFN_B) and len(AFN_A) != 3 and len(AFN_B) == 3):
            self.states.add(Start)
            if (AFN_A[-1][-1] == AFN_B[0]-1):
                NewEstado = [AFN_B[0]-1, AFN_B[1], AFN_B[0]]
                AFN_A.append(NewEstado)
                AFN_C = AFN_A
            else:
                NewEstado = [AFN_B[0], AFN_B[1], AFN_B[2]]
                AFN_A.append(NewEstado)
                AFN_C = AFN_A

        elif (len(AFN_A) < len(AFN_B) and len(AFN_B) != 3 and len(AFN_A) != 3):
            self.states.add(Start)
            for a in AFN_A:
                AFN_B.append(a)
            AFN_C = AFN_B
            
        elif (len(AFN_A) < len(AFN_B) and len(AFN_B) != 3 and len(AFN_A) == 3 and not isinstance(AFN_A[0], int)):
            if (AFN_A[-1][-1] == AFN_B[0][0]):
                for a in AFN_A:
                    AFN_B.append(a)
                AFN_C = AFN_B
            else:
                self.states.add(Start)
                NewEstado = [Start, AFN_A[1], AFN_A[0]]
                AFN_B.append(NewEstado)
                AFN_C = AFN_B

        elif (len(AFN_A) < len(AFN_B) and len(AFN_B) != 3 and len(AFN_A) == 3):
            if (AFN_A[-1] == AFN_B[0][0]):
                NewEstado = [AFN_A[0], AFN_A[1], AFN_B[0][0]]
                AFN_B.append(NewEstado)
                AFN_C = AFN_B
            else:
                self.states.add(Start)
                NewEstado = [Start, AFN_A[1], AFN_A[0]]
                AFN_B.append(NewEstado)
                AFN_C = AFN_B

        elif (len(AFN_A) < len(AFN_B) and len(AFN_B) == 3):
            NewEstado = [AFN_A[-1][-1], AFN_B[1], AFN_B[0]]
            AFN_A.append(NewEstado)
            AFN_C = AFN_A
            self.states.remove(list(self.states)[-1])

        elif (not isinstance(AFN_A[0],int) and len(AFN_A) == 3 and len(AFN_B) == 3):
            NewEstado = [AFN_A[-1][2], AFN_B[1], AFN_B[0]]
            AFN_A.append(NewEstado)
            AFN_C = AFN_A
            self.states.remove(list(self.states)[-1])

        elif (len(AFN_A) == 3 and len(AFN_B) == 3):
            NewEstado = [AFN_A[0], AFN_A[1], AFN_A[2]]
            NewEstado2 = [AFN_A[2], AFN_B[1], AFN_B[0]]
            AFN_C.append(NewEstado)
            AFN_C.append(NewEstado2)
            self.states.remove(list(self.states)[-1])

        elif (len(AFN_A) == len(AFN_B)):
            NewAFN = []
            for a in AFN_A:
                NewAFN.append(a)
            AFNB = sorted(AFN_B, key=itemgetter(0))
            for b in AFNB:
                NewAFN.append(b)

            AFN_C = NewAFN

        #print("\nC: ", AFN_C)
        return AFN_C

    def UnionExp(self, AFN_A, AFN_B):
        # print("\nA Un: ", AFN_A)
        # print("\nB Un: ", AFN_B)
        NewAFN =[]
        self.numEstados += 1
        if (isinstance(AFN_A[0], int)):
            Start = AFN_A[0]-1
            End = self.numEstados

            self.states.add(Start)
            self.states.add(End)
            #print(Start, End)

            NewEstado = [Start, epsilon, AFN_A[0]]
            NewEstado2 = [AFN_A[2], epsilon, End]

            NewEstado3 = [Start, epsilon, AFN_B[0]]
            NewEstado4 = [AFN_B[2], epsilon, End]

            NewAFN.append(NewEstado)
            NewAFN.append(AFN_A)
            NewAFN.append(NewEstado2)
            NewAFN.append(NewEstado3)
            NewAFN.append(AFN_B)
            NewAFN.append(NewEstado4)

        else:
            temp = []
            for trans in AFN_A:
                temp.append([trans[0]+1, trans[1], trans[2]+1])
            AFN_A = temp
            OrderTransitions = sorted(AFN_A, key=itemgetter(0, 2))
            Start = OrderTransitions[0][0]-1
            self.numEstados += 1
            End = self.numEstados
            AFN_A = OrderTransitions
            self.states.add(Start)
            self.states.add(End)

            #print(Start, End)
            # print("\nA D: ", AFN_A)

            if (len(AFN_A) == len(AFN_B)):
                temp2 = []
                
                if (not all(i in AFN_A[0] for i in AFN_B[0]) and AFN_A[-1][0] != AFN_B[0][0] and AFN_A[-1][2] != AFN_B[0][2]):
                    for trans in AFN_B:
                        temp2.append([trans[0]+2, trans[1], trans[2]+2])
                    AFN_B = temp2
                else:
                    for trans in AFN_B:
                        temp2.append([trans[0]+3, trans[1], trans[2]+3])
                    AFN_B = temp2
                OrderTransitions2 = sorted(AFN_B, key=itemgetter(0, 2))
                AFN_B = OrderTransitions2

                for a in AFN_B:
                    self.states.add(a[0])
                    self.states.add(a[2])

                End = AFN_B[-1][-1]+1
                self.states.add(End)

                #print("s: ", Start, End)

                NewEstado = [Start, epsilon, AFN_A[0][0]]
                NewEstado2 = [Start, epsilon, AFN_B[0][0]]

                NewEstado3 = [AFN_A[-1][-1], epsilon, End]
                NewEstado4 = [AFN_B[-1][2], epsilon, End]

                NewAFN.append(NewEstado)
                for a in AFN_A:
                    NewAFN.append(a)
                NewAFN.append(NewEstado2)
                NewAFN.append(NewEstado3)
                for b in AFN_B:
                    NewAFN.append(b)
                NewAFN.append(NewEstado4)

                #print("N: ", NewAFN)

            else:
                #print("B: ", AFN_B)
                if (isinstance(AFN_B[0],int)):
                    AFN_B = [AFN_B[0]+1, AFN_B[1], AFN_B[2]+1]

                    NewEstado = [Start, epsilon, AFN_A[0][0]]
                    NewEstado2 = [Start, epsilon, AFN_B[0]]

                    NewEstado3 = [AFN_A[-1][-1], epsilon, End]
                    NewEstado4 = [AFN_B[2], epsilon, End]

                    NewAFN.append(NewEstado)
                    for a in AFN_A:
                        NewAFN.append(a)
                    NewAFN.append(NewEstado2)
                    NewAFN.append(NewEstado3)
                    NewAFN.append(AFN_B)
                    NewAFN.append(NewEstado4)
                    
                else:
                    temp2 = []
                    for trans in AFN_B:
                        temp2.append([trans[0]+1, trans[1], trans[2]+1])
                    AFN_B = temp2

                    # print("\nA Un: ", AFN_A)
                    # print("\nB Un: ", AFN_B)

                    NewEstado = [Start, epsilon, AFN_A[0][0]]
                    NewEstado2 = [Start, epsilon, AFN_B[0][0]]

                    NewEstado3 = [AFN_A[-1][-1], epsilon, End]
                    NewEstado4 = [AFN_B[-1][-1], epsilon, End]

                    NewAFN.append(NewEstado)
                    for a in AFN_A:
                        NewAFN.append(a)
                    NewAFN.append(NewEstado2)
                    NewAFN.append(NewEstado3)
                    for b in AFN_B:
                        NewAFN.append(b)
                    NewAFN.append(NewEstado4)

                    #print("\nAN: ",NewAFN)

        #print("\nAN: ",NewAFN)

        return NewAFN

    def KleeneExp(self, AFN_A):
        # print("\nA Kleene: ",AFN_A)
        #print("Estado: ", self.numEstados)
        if (isinstance(AFN_A[0], int)):
            Start = AFN_A[0]-1
            self.numEstados += 1
            End = self.numEstados

            if (Start < 0):
                Start = 0
                End += 1
                self.states = {a+1 for a in self.states}
                temp = []

                # print("S: ",Start)
                # print("E: ",End)

                for trans in AFN_A:
                    temp.append([trans[0]+1, trans[1], trans[2]+1])

                AFN_A = temp
                self.states.add(Start)
                self.states.add(End)

                NewAFN = [Start, epsilon, AFN_A[0]]
                NewAFN2 = [AFN_A[-1], epsilon,End]
                NewAFN3 = [AFN_A[-1], epsilon, AFN_A[0]]
                NewAFN4 = [Start, epsilon, End]

                AFN_A.append(NewAFN)
                AFN_A.append(NewAFN2)
                AFN_A.append(NewAFN3)
                AFN_A.append(NewAFN4)

            else:
                # print("S: ",Start)
                # print("E: ",End)
                NewA =[]
                Start = AFN_A[0]-1
                self.states.add(Start)
                self.states.add(End)

                NewAFN = [Start, epsilon, AFN_A[0]]
                NewAFN2 = [AFN_A[-1], epsilon,End]
                NewAFN3 = [AFN_A[-1], epsilon, AFN_A[0]]
                NewAFN4 = [Start, epsilon, End]

                NewA.append(NewAFN)
                NewA.append(AFN_A)
                NewA.append(NewAFN2)
                NewA.append(NewAFN3)
                NewA.append(NewAFN4)

                AFN_A = NewA

        else:
            #print("Estado: ", self.numEstados)
            Start = AFN_A[0][0]-1
            self.numEstados += 1
            End = self.numEstados

            if (Start < 0):
                Start = 0
                End += 1
                self.states = {a+1 for a in self.states}
                temp = []

                # print("S: ",Start)
                # print("E: ",End)

                for trans in AFN_A:
                    temp.append([trans[0]+1, trans[1], trans[2]+1])

                AFN_A = temp
                self.states.add(Start)
                self.states.add(End)

                NewAFN = [Start, epsilon, AFN_A[0][0]]
                NewAFN2 = [AFN_A[-1][-1], epsilon,End]
                NewAFN3 = [AFN_A[-1][-1], epsilon, AFN_A[0][0]]
                NewAFN4 = [Start, epsilon, End]

                AFN_A.append(NewAFN)
                AFN_A.append(NewAFN2)
                AFN_A.append(NewAFN3)
                AFN_A.append(NewAFN4)

            else:
                NewA =[]
                temp = []

                Start = AFN_A[0][0]
                self.numEstados += 1

                self.states.add(Start)

                for trans in AFN_A:
                    temp.append([trans[0]+1, trans[1], trans[2]+1])

                AFN_A = temp
                for a in AFN_A:
                    self.states.add(a[0])
                    self.states.add(a[2])
                    NewA.append(a)

                End = AFN_A[-1][-1]+1
                self.states.add(End)

                NewAFN = [Start, epsilon, End]
                NewAFN2 = [Start, epsilon, AFN_A[0][0]]
                NewAFN3 = [AFN_A[-1][-1], epsilon, AFN_A[0][0]]
                NewAFN4 = [AFN_A[-1][-1], epsilon, End]

                NewA.append(NewAFN)
                NewA.append(NewAFN2)
                NewA.append(NewAFN3)
                NewA.append(NewAFN4)

                AFN_A = NewA


        #print("\nA Kleene salida: ",AFN_A)
        return AFN_A
    
    def CheckStates(self, Transitions):
        self.Init = 0
        self.Last = 0
                             
        if(-1 in self.states):
            self.states.remove(-1)
            N = sorted(list(self.states))
            self.states.add(N[-1]+1)
            
            N = sorted(list(self.states))
            self.Init = N[0]
            self.Last = N[-1]

        if isinstance(Transitions[0], int):
            self.states.add(Transitions[0])
            self.states.add(Transitions[2])
            self.Init = list(self.states)[0]
            self.Last = list(self.states)[-1]
        else:    
            for i in range(len(self.states)):
                if (not any(list(self.states)[-1] in sublist for sublist in Transitions)):
                    if (list(self.states)[-1] in self.states):
                        self.states.remove(list(self.states)[-1]) 

            for a in Transitions:
                self.states.add(a[0])
                self.states.add(a[2])
                
            self.Init = list(self.states)[0]
            self.Last = list(self.states)[-1]

    def printResults(self, Transitions):   
        print("\nInfix: ", self.expression)
        print("Postfix: ",self.postfixExp)
        print("Estados = ", sorted(self.states))
        print("Simbolos = ", self.symbols)
        print("Estado de inicio = ",self.Init)
        print("Estado de aceptacion = ",self.Last)
        self.printTransitions(Transitions)

    def printTransitions(self, Transitions):
        x = ""
        TransitionsN = []

        #print(Transitions)

        if (len(Transitions) == 3 and isinstance(Transitions[0], int)):
            x = '(' + str(Transitions[0]) + ', ' + str(Transitions[1]) + ', ' + str(Transitions[2]) + ')'
            TransitionsN.append(x)

        else:
            VerificadorEstados = any(-1 in sublist for sublist in Transitions)

            if (VerificadorEstados):
                NTransitions = []

                for trans in Transitions:
                    NTransitions.append([trans[0]+1, trans[1], trans[2]+1])

                OrderTransitions = sorted(NTransitions, key=itemgetter(0, 2))
            else:
                OrderTransitions = sorted(Transitions, key=itemgetter(0, 2))

            for t in range(len(OrderTransitions)):
                x = '(' + str(OrderTransitions[t][0]) + ', ' + str(OrderTransitions[t][1]) + ', ' + str(OrderTransitions[t][2]) + ')'
                TransitionsN.append(x)

        print("Transiciones: "+ " - ".join(TransitionsN))
        print()

# r1 = "a"
# r2 = "ab"
# r3 = "aab"
# r4 = "(0|1)"
# r5 = "a*"
# r6 = "(a|b)*"
# r7 = "0(0|1)0"
# r8 = "0*(0*|1)1"
# r9 = "0*11*0"
# r10 = "(b|b)*abb(a|b)*"
# r11 = "(a|b)*|(a|b)*"
# r12 = "((a|b)|(abab))|a"
# r13 = "ab*ab*"
# r14 = "(a|b)*(abba*|(ab)*ba)"
r15 = "(a|b)$"

rs = []
# rs.append(r1)
# rs.append(r2)
# rs.append(r3)
# rs.append(r4)
# rs.append(r5)
# rs.append(r6)
# rs.append(r7)
# rs.append(r8)
# rs.append(r9)
# rs.append(r10)
# rs.append(r11)
# rs.append(r12)
# rs.append(r13)
# rs.append(r14)
rs.append(r15)

for r in rs:
    Cons = Construction(r)
    N = Cons.Thompson_Construction()

