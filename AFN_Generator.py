# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# CC2019 Teoría de la computación
# Grupo#9

# Base de construcción de Thompson: https://medium.com/swlh/visualizing-thompsons-construction-algorithm-for-nfas-step-by-step-f92ef378581b

# Import de los otros archivos
from conversions import *
from stack import *
from operator import itemgetter
from time import perf_counter

# Símbolo epsilon utilizado a lo largo de Thompson
epsilon = '$'

# Clase construction: Construye un autómata finito mediante una expresión regular y con construcción de Thompson
class Construction:
    # Constructor: Inicializa todos los elementos a utilizar
    def __init__(self, expression):
        self.expression = expression
        self.states = set()
        self.symbols = []
        self.transitions = []
        self.stackAFN = []
        self.AFN = []
        self.numEstados = 0
        self.FinalTransitions = []

    # Método Thompson_Construction: Construye el AFN mediante con construcción de Thompson
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
        t1_start = perf_counter()


        for element in self.postfixExp:
            # Dependiendo del elemento trabaja una operación diferente
            
            # Si es un símbolo o epsilon crea un componente del tipo símbolo
            if (element in self.symbols or element == '$'):
                NewAFN = self.symbol(element)
                self.stackAFN.append(NewAFN)
            
            # Si es una concatenación se obtienen los valores a concatenar
            # y se crea un componente del tipo concatenación    
            elif (element == '.'):
                A = self.stackAFN.pop()
                B = self.stackAFN.pop()
                NewAFN = self.ConcatExp(B, A)
                self.stackAFN.append(NewAFN)
            
            # Si es una unión se obtienen los valores a unir
            # y se crea un componente del tipo unión  
            elif (element == '|'):
                A = self.stackAFN.pop()
                B = self.stackAFN.pop()
                NewAFN = self.UnionExp(B, A)
                self.stackAFN.append(NewAFN)
                
            # Si es una cerradura se obtiene el valor a utilizar
            # y se crea un componente del tipo cerradura
            elif (element in '*+?'):
                A = self.stackAFN.pop()
                # Se evaluan diferentes casos dependiendo de que elemento tendrá la cerradura 
                # y se retorna el valor final
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

        # El último elemento (AFN) completo se obtiene al realizar el último pop al stack de AFN's (Componentes)
        AFN = self.stackAFN.pop()
        # Se evaluan los estados con este método para revisar que todos estén bien
        self.CheckStates(AFN)
        t1_stop = perf_counter()
        # Para imprimir resultados en dado caso se pruebe desde este archivo
        # Descomentar línea siguiente: 
        # self.printResults(AFN)
        
        # Se ordenan los valores para poder visualizarlos mejor
        if len(AFN) == 3 and isinstance(AFN[0], int):
            SortedAFN = AFN
        else:
            SortedAFN = sorted(AFN, key=itemgetter(0, 2))
        tiempo = (t1_stop - t1_start)
        # Finalmente se retorna el AFN para ser utilizado en otros archivos o funciones
        return SortedAFN, tiempo

    # Componente símbolo: Se crean relaciones del tipo NodoA-[simbolo]->NodoB
    def symbol(self, symbolT):
        self.numEstados += 1
        NodoA = self.numEstados
        self.numEstados += 1
        NodoB = self.numEstados
        self.states.add(NodoA)
        self.states.add(NodoB)

        NewEstado = [NodoA, symbolT, NodoB]

        return NewEstado

    # Componente concatenación: Se crean las concatenaciones entre dos elementos
    # y se corrijen los estados para que todos lleven un orden bueno
    def ConcatExp(self, AFN_A, AFN_B):
        self.numEstados -= 1
        AFN_C = []
        if (isinstance(AFN_A[0], int)):
            Start = AFN_A[0]-1
        else:
            Start = AFN_A[0][0]-1

        # Al igual que antes, se comprueban diversos casos dependiendo de los
        # elementos o el orden utilizado y se procede a concatenar ambos elementos
        
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
            AFNB = sorted(AFN_B, key=itemgetter(0))
            AFN_B = AFNB
            
            for a in AFN_B:
                self.states.add(a[0])
                self.states.add(a[2])
                AFN_A.append(a)
                
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
                NewEstado = [AFN_A[0], AFN_A[1], AFN_A[2]]
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

        #Se retorna el elemento resultante
        return AFN_C

    # Componente unión: Se crean las uniones entre dos elementos
    # y se corrijen los estados para que todos lleven un orden bueno
    def UnionExp(self, AFN_A, AFN_B):
        NewAFN =[]
        self.numEstados += 1
        
        # Se realizan verificaciones para saber que camino tomar
        # dependiendo del orden y los elementos brindados
        if (isinstance(AFN_A[0], int)):
            Start = AFN_A[0]-1
            End = self.numEstados

            self.states.add(Start)
            self.states.add(End)

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

            else:
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

        # Retorna el nuevo componente de la unión
        return NewAFN

    # Componente cerradura: Se crea la cerradura 
    # y se corrijen los estados para que todos lleven un orden bueno
    def KleeneExp(self, AFN_A):
        #Dependiendo del valor que se se reciba toma un camino diferente
        if (isinstance(AFN_A[0], int)):
            Start = AFN_A[0]-1
            self.numEstados += 1
            End = self.numEstados

            if (Start < 0):
                Start = 0
                End += 1
                self.states = {a+1 for a in self.states}
                temp = []

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
            Start = AFN_A[0][0]-1
            self.numEstados += 1
            End = self.numEstados

            if (Start < 0):
                Start = 0
                End += 1
                self.states = {a+1 for a in self.states}
                temp = []
                
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


        # Retorna el AFN con su cerradura
        return AFN_A
    
    # Método que revisa los estados finales obtenidos para
    # comprobar que sean coherentes con las transiciones
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

    # Método para imprimir resultados
    def printResults(self, Transitions):   
        print("\nInfix: ", self.expression)
        print("Postfix: ",self.postfixExp)
        print("Estados = ", sorted(self.states))
        print("Simbolos = ", self.symbols)
        print("Estado de inicio = ",self.Init)
        print("Estado de aceptacion = ",self.Last)
        self.printTransitions(Transitions)

    # Método para imprimir en el formato requerido las transiciones
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
                
        self.FinalTransitions = " - ".join(TransitionsN)
        print("Transiciones: "+ " - ".join(TransitionsN))
        print()

