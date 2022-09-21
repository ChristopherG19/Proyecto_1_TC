# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# CC2019 Teoría de la computación
# Grupo#9 

# Main
from AFN_Generator import * 
from SimulacionAFN import *
from subconjuntos  import *
from time import perf_counter

# _________________________________________
#                 Pruebas 
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
r = "(a|b)*(abba*|(ab)*ba)"
# r = "(a|b)$"

w = "abbaaa"

# --------------------------------------------------
# Construcción de AFN con Thompson
print('\n--> Construcción AFN con construcción de Thompson')
t1_start = perf_counter()
Cons = Construction(r)
AFN_Thompson = Cons.Thompson_Construction()
t1_stop = perf_counter()
Cons.printResults(AFN_Thompson)
print('Tiempo de ejecución: %.4e ms'%(t1_stop - t1_start))
# --------------------------------------------------

# --------------------------------------------------
# Simulación de cadenas en AFN
print('\n--> Simulación AFN')
t1_start = perf_counter()
ResultadoSimulacion = SimulationAFN(r, w)
print("\nExpresion regular:", r)
print("Cadena a evaluar:", w)
print("Resultado: La cadena %s"%w, ResultadoSimulacion, "es aceptada\n")
t1_stop = perf_counter()
print('Tiempo de ejecución: %.4e ms'%(t1_stop - t1_start))
# --------------------------------------------------

# --------------------------------------------------
# Construcción de AFD con subconjuntos
print('\n--> Construcción AFD con subconjuntos')
t1_start = perf_counter()
AFD_Subconjuntos = AFN_To_AFD_SC(r)
printResultsAFD(AFD_Subconjuntos[0], AFD_Subconjuntos[1], AFD_Subconjuntos[2])
t1_stop = perf_counter()
print('Tiempo de ejecución: %.4e ms'%(t1_stop - t1_start))
print()
# --------------------------------------------------
