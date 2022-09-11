# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# CC2019 Teoría de la computación
# Grupo#9 

class AFD():
    def __init__(self, In, Fn=None):
        self.initState = In
        self.acceptStates = [] or Fn
        self.states = []
        self.dictionary = []
        self.transitions = []
    
    