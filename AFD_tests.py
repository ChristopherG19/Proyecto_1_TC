from AFD import *


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

# Construcción del árbol sintáctico
arbol = Tree(r)
print()
print('Árbol sintáctico')
print(arbol)

# Construcción directa
dfa = AFD()
dfa.directConstruction(arbol)
print('Construcción directa')
for x in dfa.afd:
    print(x)
print()

# Simulación de cadenas
print('Simulación')
if (dfa.simulation(w)):
    print('sí')
else:
    print('no')
print()

# Minimización
print('Minimización')
dfa.minimization()
for x in dfa.afd:
    print(x)
print()

# Simulación de cadenas
print('Simulación')
if (dfa.simulation(w)):
    print('sí')
else:
    print('no')
print()