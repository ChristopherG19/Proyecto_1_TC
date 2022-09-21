# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Departamento de Ciencias de la Computación
# CC2019 Teoría de la computación
# Grupo#9 

from Tree import *

class AFD():
    def __init__(self, Transitions = None, Final_States = None, regex = None):
        self.afd = []
        self.EA = []
        self.Dstates = []
        self.Symbols = []
        self.STree = []

        # Si se le dan parámetros, se puede construir sin la construcción directa
        if (Transitions and regex and Final_States):

            for t in Transitions:
                if (t[2] != None):
                    # Si no vienen transiciones que no llevan a ningún lado
                    self.afd.append(t)
                if (t[1] and t[1] not in self.Symbols):
                    self.Symbols.append(t[1])



    def __repr__(self):
        retString = ''
        for s in self.afd:
            retString += '(' + s[0] + ' - ' + s[1] + ' - ' + s[2] + ')\n'
        return retString
            

    def directConstruction(self, arbol):

        self.STree = arbol

        # Alfabeto de la expresión regex
        self.Symbols = self.detSymbols(arbol)

        # Firstpos de la raíz
        cant_n = len(arbol.Arbol)
        Dstates = []
        Dstates.append(arbol.Arbol[cant_n - 1].firstpos)

        Dstates_marked = []

        # Si no todos los estados de Dstates están marcados (en Dstates_marked) se continúa
        while (not all(t in Dstates_marked for t in Dstates)):
            for t in Dstates:
                # Se marca el estado actual
                Dstates_marked.append(t)

                for a in self.Symbols:
                    U = []

                    # Buscamos en todo el árbol por las posiciones que tengan el símbolo
                    for x in t:
                        if arbol.States[x].getSymbol() == a:
                            # Si no está en el estado, se añade
                            for e in arbol.States[x].followpos:
                                if (e not in U):
                                    U.append(e)
                    
                    if (len(U) > 0):
                        if (U not in Dstates):
                            Dstates.append(U)

                        self.afd.append([t, a, U])

        # Determinamos estados de aceptación
        self.EA = [(len(arbol.States) - 1) in x for x in Dstates]

        # Renombramos los estados 
        newStates = ["q%s"%x for x in range(len(Dstates))]

        temp_afd = []
        for trans in self.afd:
            t = []
            for element in trans:
                if (element in Dstates):    
                    t.append(newStates[Dstates.index(element)])
                else:
                    t.append(element)
            temp_afd.append(t)

        # Remplazamos AFD para conseguir correcto
        self.afd = temp_afd

        # Guardamos todos los estados
        for x in self.afd:
            if(x[0] not in self.Dstates):
                self.Dstates.append(x[0])

        for x in self.afd:
            if(x[2] not in self.Dstates):
                self.Dstates.append(x[2])


    def simulation(self, w):

        if (type(w) != list):
            w = list(w)

        s = self.afd[0][0]
        i = 0
        

        while (i <= (len(w) - 1) and s):
            c = w[i]
            s = self.move(s, c)
            i += 1

        if (s == NULL or not self.EA[self.Dstates.index(s)]):
            return False

        else:
            return True

    def move(self, state, char):
        newState = NULL # Retorna 
        for q in self.afd:
            #por cada estado en el AFD, buscar si alguno tiene transición con la letra
            if (q[0] == state):
                if (q[1] == char):
                    # Si hayn
                    newState = q[2]
        return newState


    def minimization(self):
        G = [[]]
        for x in self.Dstates:
            G[0].append(x)

        tabla = []
        GG_new = []
        ciclo = True 
        iteracion = 0

        while (ciclo):

            # vaciar tabla
            tabla = []
                
            # Encontrar a dónde van los estados de cada grupo
            for g in G:

                tabla_t = []
                # iniciamos la tabla con los estados dentro del grupo g
                for x in range(len(g)):
                    tabla_t.append([g[x]])

                # Agregamos a los estados que llegan con cada símbolo del alfabeto
                for x in tabla_t:
                    # x[0] := qn
                    for a in self.Symbols:
                        trans_a = ''
                        for t in self.afd:
                            if (x[0] == t[0] and a == t[1]):
                                trans_a = t[2]
                        # Añadir al estado al que llega con el símbolo
                        x.append(trans_a)

                # Agregamos al grupo en el que pertenecen esos estados
                # que agregamos
                for x in tabla_t:
                    # Por los símbolos del alfabeto
                    for a in range(len(self.Symbols)):
                        # Índice en el que se agregará en la tabla
                        i_look = (1 + a)

                        trans_g = []

                        # Buscar en los nuevos conjuntos
                        for g2 in G:
                            if (x[i_look] in g2):
                                trans_g = g2

                        x.append(trans_g)

                # Agrupamos los que son iguales
                G_temp = []
                conjunto_estados_finales = []
                for x in tabla_t:

                    estados_finales = []
                    for a in range(len(self.Symbols)):
                        i_look = (1 + len(self.Symbols) + a)
                        estados_finales.append(x[i_look])

                    # Determinar si hay otros estados con los mismos estados finales
                    if (estados_finales in conjunto_estados_finales):
                        # si ya estaba, juntar los estados
                        G_temp[conjunto_estados_finales.index(estados_finales)].append(x[0])
                    else:
                        # Crear un nuevo conjunto
                        G_temp.append([x[0]])
                        conjunto_estados_finales.append(estados_finales)

                if (g in GG_new):
                    # Si ya estaba, se elimina
                    GG_new.remove(g)

                GG_new += G_temp
                
                # guardar los datos de la tabla
                tabla += tabla_t

            #GG_new = G   
            # break
            iteracion += 1   

            # Verificar ciclo 
            if (not all(q in GG_new for q in G)):
                G = []
                for g in GG_new:
                    G.append(g)

            else:
                ciclo = False   

        # Conseguir nuevos estados de aceptación
        new_EA = []
        for x in G:
            aceptacion = False
            for y in x:
                if (self.EA[self.Dstates.index(y)]):
                    aceptacion += True
                else:
                    aceptacion += False
            new_EA.append(bool(aceptacion))

        self.EA = []
        self.EA = new_EA

        # Renombrar variables y reconstruir las transiciones
        afd_temp = []
        for t in G:
            for x in tabla:
                if (t[0] == x[0]):
                    for a in range(len(self.Symbols)):
                        i_look = 1 + len(self.Symbols) + a
                        U = x[i_look]
                        if (len(U) > 0):
                            add = [t, self.Symbols[a], U]
                            afd_temp.append(add)

        # Renombramos los estados 
        newStates = ["q%s"%x for x in range(len(G))]

        temp_afd = []
        for trans in afd_temp:
            t = []
            for element in trans:
                if (element in G):    
                    t.append(newStates[G.index(element)])
                else:
                    t.append(element)
            temp_afd.append(t)

        # Remplazamos AFD para conseguir correcto
        self.afd = []
        self.afd = temp_afd

        # Guardamos todos los estados
        self.Dstates = []
        self.Dstates = newStates

    def detSymbols(self, arbol):
        Symbols = []
        for n in arbol.States:
            if (n.getSymbol() not in Symbols and n.getSymbol() != '#'):
                Symbols.append(n.getSymbol())
        
        return Symbols


