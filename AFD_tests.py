# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# CC2019 Teoría de la computación
# Grupo#9 

from AFD import *
from AFN_Generator import * 
from SimulacionAFN import *
from subconjuntos  import *
from time import perf_counter

# _________________________________________
# Temporal 
# _________________________________________

# r = "a"
# r = "ab"
# r = "aab"
# r = "(0|1)"
# r = "a*"
# r = "(a|b)*"
# r = "0(0|1)0"
# r = "0*(0*|1)1"
# r = "0*11*0"
# r = "(b|b)*abb(a|b)*"
# r = "(a|b)*|(a|b)*"
# r = "((a|b)|(abab))|a"
# r = "ab*ab*"
# r = "(a|b)$"
r2 = "(a|b)*(abba*|(ab)*ba)"
w2 = "abbaaa"

# _________________________________________
# pruebas 
# _________________________________________

# r = 'ab*ab*#'
# w = 'aa'

# r = '(aa*)|(bb*)#'
# r = '(a|b)*(a|b)*a?#'

# Expresión ya minimizada
# r = '(aa|bb)*#'
# w = 'aabbaa'

# Expresión ya minimizada
# r = '(a(a|b)b)*#'
# w = 'abbaab'

# r = 'a(a|b)*#'
# w = 'aaab'

# r = 'a(a|b)*#'
# r = '(a|b)|(abab)'

# Expresión ya minimizada
# r = '0(0|1)0#'
# w = '000'

# Da no simplificado 
r = '0*(0*|1)1'
w = '000000111'

# 
# r = '00*1110(0|1*)#'
# w = '01110111'

# --------------------------------------------------
# Construcción de AFN con Thompson
print('\n--> Construcción AFN con construcción de Thompson')
t1_start = perf_counter()
Cons = Construction(r2)
AFN_Thompson = Cons.Thompson_Construction()
t1_stop = perf_counter()
Cons.printResults(AFN_Thompson)
print('Tiempo de ejecución: %.4e ms'%(t1_stop - t1_start))
# --------------------------------------------------

# --------------------------------------------------
# Simulación de cadenas en AFN
print('\n--> Simulación AFN')
t1_start = perf_counter()
ResultadoSimulacion = SimulationAFN(r2, w2)
print("\nExpresion regular:", r2)
print("Cadena a evaluar:", w2)
print("Resultado: La cadena %s"%w2, ResultadoSimulacion, "es aceptada\n")
t1_stop = perf_counter()
print('Tiempo de ejecución: %.4e ms'%(t1_stop - t1_start))
# --------------------------------------------------

# --------------------------------------------------
# Construcción de AFD con subconjuntos
print('\n--> Construcción AFD con subconjuntos')
t1_start = perf_counter()
AFD_Subconjuntos = AFN_To_AFD_SC(r2)
printResultsAFD(AFD_Subconjuntos[0], AFD_Subconjuntos[1], AFD_Subconjuntos[2])
t1_stop = perf_counter()
print('Tiempo de ejecución: %.4e ms'%(t1_stop - t1_start))
# --------------------------------------------------

# --------------------------------------------------
# Construcción del árbol sintáctico
print('\nÁrbol sintáctico')
t1_start = perf_counter()
arbol = Tree(r)
t1_stop = perf_counter()
print(arbol)
print('tiempo de ejecución: %.4e ms'%(t1_stop - t1_start))

# --------------------------------------------------
# Construcción directa
print('\nConstrucción directa')
t2_start = perf_counter()
dfa = AFD()
dfa.directConstruction(arbol)
t2_stop = perf_counter()
print(dfa)
print(dfa.getFinalStates())
print('tiempo de ejecución: %.4e ms'%(t2_stop - t2_start))

# --------------------------------------------------
# Simulación de cadenas
print('\nSimulación')
t3_start = perf_counter()
if (dfa.simulation(w)):
    print('El string %s pertenece al AFD'%w)
else:
    print('El string %s no pertenece al AFD'%w)
t3_stop = perf_counter()
print('tiempo de ejecución: %.4e ms'%(t3_stop - t3_start))

# --------------------------------------------------
# Minimización
print('\nMinimización')
t4_start = perf_counter()
dfa.minimization()
t4_stop = perf_counter()
print(dfa)
print('tiempo de ejecución: %.4e ms'%(t4_stop - t4_start))

# --------------------------------------------------
# Simulación de cadenas
print('\nSimulación')
t5_start = perf_counter()
if (dfa.simulation(w)):
    print('El string %s pertenece al AFD'%w)
else:
    print('El string %s no pertenece al AFD'%w)
t5_stop = perf_counter()
print('tiempo de ejecución: %.4e ms'%(t5_stop - t5_start))

print('\nAFN -> AFD')
states = [
    ['q0', '0', 'q1'],
    ['q0', '1', 'q2'],
    ['q1', '0', 'q1'],
    ['q1', '1', 'q3'],
    ['q2', '1', 'q4'],
    ['q3', '1', 'q4'],
    ['q3', '0', None]
] 
EA = ['q3', 'q4']
r = '0*(0*|1)1#'
istate = ['q0']
dfa2 = AFD(states, EA, r, istate) 
print(dfa2)
print(dfa.Symbols)
print(dfa2.Dstates)
print(dfa2.EA)

lines = [
    'AFD',
    'Estados = %s'%dfa2.Dstates,
    'Simbolos = %s'%dfa2.Symbols,
    'Inicio = %s'%dfa2.initState,
    'Aceptacion = %s'%dfa2.getFinalStates(),
    'Transiciones = %s'%dfa2
]

# Escribir a un archivo
with open('AFD.txt', 'w') as f:
    for line in lines:
        f.write(line)
        f.write('\n')