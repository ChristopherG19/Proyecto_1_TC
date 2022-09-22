# Proyecto_1_TC
Integrantes: 
-      Christopher García 20541
       Ma. Isabel Solano 20504
## Descripción
El proyecto consiste en la implementación de los algoritmos básicos para construcción de autómatas finitos a partir de expresiones regulares. Se posee una expresión regular r y una cadena w. Con estos elementos se trabajaron los siguientes puntos:

- Conversión de expresión Infix a expresión Postfix
- Implementación del algoritmo de Construcción de Thompson (Construcción de AFN)
- Implementación del algoritmo de Construcción de Subconjuntos (Construcción de AFD)
- Implementación del algoritmo de Construcción de AFD a partir una expresión regular r (Construcción directa de AFD)
- Implementación de un algoritmo de minimización de AFD's
- Implementación de simulación de un AFN
- Implementación de simulación de un AFD

Por convención se decidio que el símbolo epsilon ε sería reemplazado por $.

## Especificaciones
-> Entrada
  Se ingresa un expresión regular r (Por ejemplo: r=(b|b)*abb(a|b)*) y una cadena a evaluar w (Por ejemplo: w=babbaaaaa)
  
-> Salida
  Para cada autómata generado se retorna un Sí, si la cadena pertenece a L(r) y No en caso contrario, y una descripción con la siguiente estructura:

- Estados = [0, ..., n]
- Simbolos = [a, b, ..., z]
- Inicio = [0]
- Aceptación = [0, 1, ..., n]
- Transiciones = (0, a, 1) - (0, $, 2) - ...

![Python](http://ForTheBadge.com/images/badges/made-with-python.svg)
