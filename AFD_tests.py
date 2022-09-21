from pprint import pprint
from AFD import *
from time import perf_counter

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
r = '0*(0*|1)1#'
w = '000000111'

# 
# r = '00*1110(0|1*)#'
# w = '01110111'

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
for x in dfa.afd:
    print(x)
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
print('\Minimización')
t4_start = perf_counter()
dfa.minimization()
t4_stop = perf_counter()
for x in dfa.afd:
    print(x)
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

print()