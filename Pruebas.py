
# m = [[-1, '$', 0], [-1, '$', 6], [0, '$', 1], 
#      [0, '$', 3], [1, 'b', 2], [2, '$', 5], 
#      [3, 'b', 4], [4, '$', 5], [5, '$', 6], [5, '$', 0]]

# nm = []

# for trans in m:
#     nm.append([trans[0]+1, trans[1], trans[2]+1])
    
# print(nm)

# n = {0,1,-1,2,3}

# nw = {a+1 for a in n}

# print(nw)

# from operator import itemgetter

# n = [[0, '$', 1], [1, 'b', 2], 
#     [2, '$', 5], [0, '$', 3], 
#     [3, 'b', 4], [4, '$', 5], 
#     [-1, '$', 0], [5, '$', 6], 
#     [5, '$', 0], [-1, '$', 6]] 

# newN = sorted(n, key=itemgetter(0))

# for a in newN:
#     print(a[0],"-",a[1],"->",a[2])


# N = [['1', '1', '2']]
# N2 = ['1', '1', '2']

# print(N[0][0])
# print(N2[0][0][0][0])

# numEstados = [f'{n}' for n in range(10)]
# print(numEstados[0])
# print(numEstados.pop(0))
# print(numEstados.pop(0))
# print(numEstados)


# prueba = [['1', '1', '2'], ['3', '0', '4'], ['5', '0', '6']] 

# inicio = prueba[0][0]
# fin = prueba[-1][-1]

# print(prueba)

# temps = []
# for transition in prueba:
#     temp = []
#     for element in range(len(transition)):
#         print(element, transition.index(transition[element],0))
#     temps.append(temp)    
        
# print(temps)

# Modificación transiciones
# temps = []
# for transition in self.transitions:
#     temp = []
#     for element in transition:
#         if element == str(max(self.states)) or element == str(Estado_B):
#             element = element.replace(element, str(ElB[1]))
#         elif int(element)-1 == ElB[0]:
#             print(element)
#             element = str(ElA[1])
#             print(element)
        
#         if (len(temp) <= len(transition)):
#             temp.append(element)
#     temps.append(temp)   
                
# self.transitions = temps

# print(self.transitions)
# for n in range(len(self.transitions)):
#     if n == 0:
#         continue
#     if n-1 >= 0:
#         if self.transitions[n][0] == str(int(self.transitions[n][2])+1):
#             self.transitions[n][2] = str(int(self.transitions[n][2])-1)

                        