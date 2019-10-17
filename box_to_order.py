import numpy as np
import operator 

def get_orden(lista_cord):
    total_centro = []
    definicion={}
    count = 0
    #Creando los puntos centrales.
    lista_cord.tolist()
    
    for i in lista_cord:
        count += 1
        centro=[]
        A = int((i[0] + i[2])/2)
        centro.append(A)
        B = int((i[1] + i[3])/2)
        centro.append(B)
        centro.append(count)
        total_centro.append(centro)
       
    #Sacando los rangos. 
    total_rangos_y=[]
    for i in lista_cord:
        A = abs(int((i[1] - i[3])/2))
    for c in total_centro:
        rangos_y = []
        B_1 = c[1] + A
        rangos_y.append(B_1)
        B_2 = c[1] - A
        rangos_y.append(B_2)
        rangos_y.append(c[0])
        rangos_y.append(c[2])
        total_rangos_y.append(rangos_y)
    
    
    #Creando los grupos de los rangos
    rangos_ordenados= sorted(total_rangos_y)
    gas = []
    for r_y in range(len(rangos_ordenados)):
        que_rango=[]
        que_rango.append(rangos_ordenados[r_y])
        for r_y2 in range(len(rangos_ordenados)):
            if rangos_ordenados[r_y][0] <= rangos_ordenados[r_y2][0]*1.1 and rangos_ordenados[r_y][1] >= rangos_ordenados[r_y2][1]*0.9:
                que_rango.append(r_y2)
        gas.append(que_rango)
        
  
   
    #gas = sorted(gas, key=operator.itemgetter(1, 2))
    gas.sort(key=lambda x: x[0][2])
    gas.sort(key=lambda x: x[1]) 

    
    #Crear una lista con las posiciones que deberian ser
    orden_final=[]
    cuenta = 0
    for orden in gas:
        l_cuenta=[]
        cuenta += 1
        l_cuenta.append(cuenta)
        l_cuenta.append(orden[0][3])
        orden_final.append(l_cuenta)
    
    #Meter toda la info en un dicc
    for num in range(len(total_centro)):
        definicion[num]='Centros:',total_centro[num],'Rangos y:', gas[num], 'Orden:',orden_final[num]
        orden_final[num]=orden_final[num]
    
    #Añadir a cada source su posicion concreta
    lista_cord_copy = lista_cord.tolist()
 
    for i in range(1,len(lista_cord)+1):
        for j in orden_final:          
                if i == j[1]:
                    lista_cord_copy[i-1].append(j[0])
                    #lista_cord_copy[3] = j[0]
                    pass
    
    
    #ordenando por posicion.
    lista_cord_copy.sort(key=lambda x: x[4])
    
    for i in range(len(lista_cord_copy)):
          lista_cord_copy[i].pop(4)
    
    
    lista_cord_copy = abs(np.array(lista_cord_copy))
    return lista_cord_copy
            