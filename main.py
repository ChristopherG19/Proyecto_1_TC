# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# CC2019 Teoría de la computación
# Grupo#9 

# Main 
from SimulacionAFN import *

r = "(b|b)*abb(a|b)*"
w = "a"

Resultado = Simulation(r, w)

print("\nExpresion regular:", r)
print("Cadena a evaluar:", w)
print("Resultado:", Resultado, "es aceptada\n")
