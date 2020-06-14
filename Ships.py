import random
import math
from matplotlib import pyplot as plt
from numpy import binary_repr
import itertools
import os

ships = [[44], [32], [15], [40]]
boat_N = 5 # Define el numero de barcos que quieres validar pero que sean menor que 8
velMin = 20 # Define la velocidad minima que puede tener un barco
velMax = 100 # Define la velocidad maxima que puede tener un barco
N_Ports = 4 # Define el numero de puertos que se pueden pasar 
min_Time = 0.50 
max_Time = 1
outs1 = []
arrivals1 = []
wait_Time = []
time_aux = []
general_time = []
finish = []
best_time =[]
MutationIndividue = 0.15
Boats_gen = []

def Boat():
    ships1 = []
    distance1 = []
    for item in range(boat_N):
        dato = random.randint(velMin, velMax)
        if (dato in ships1) == True:
            dato = random.randint(velMin, velMax)
        ships1.append(dato)
    
    for item in range(N_Ports):
        dato1 = random.randint(59, 200)
        distance1.append(dato1)
        
    print(ships1)  
    return ships1 , distance1

def inserta(x, lst, i):
    """Devuelve una nueva lista resultado de insertar
       x dentro de lst en la posición i.
    """
    return lst[:i] + [x] + lst[i:]

def inserta_multiple(x, lst):
    """Devuelve una lista con el resultado de
       insertar x en todas las posiciones de lst.  
    """
    return [inserta(x, lst, i) for i in range(len(lst) + 1)]

def permuta(c):
    """Calcula y devuelve una lista con todas las
       permutaciones posibles que se pueden hacer
       con los elementos contenidos en c.
    """
    if len(c) == 0:
        return [[]]
    return sum([inserta_multiple(c[0], s)
                for s in permuta(c[1:])],
               [])

def crossover(boats):        
    orderShips = generateShips(boats)
    #print(orderShips)
    Sons = []
    for item in range(len(orderShips)):        
        Pattern1 = random.choice(orderShips)        
        Pattern2 = random.choice(orderShips)        
        if Pattern1 != Pattern2:
            Son_aux = []
            crossoverPoint = random.randrange(boat_N)                         
            #print("Los padres que se van a cruzar son → Padre_1 →", pattern1, " : ", Pattern1 ,  " Padre_2 → ", pattern2, " : ", Pattern2, " El punto de cruza es → ", crossoverPoint)
            Son1 = Pattern1[0:crossoverPoint] + Pattern2[crossoverPoint:len(Pattern1)]
            Son2 = Pattern2[0:crossoverPoint] + Pattern1[crossoverPoint:len(Pattern2)]            
            #print("Los hijos resultantes son → Hijo 1 → ", Son1, " Hijo 2 → ", Son2)
            Son_aux.append(Son1)
            Son_aux.append(Son2)
            #print(Son_aux)             
            Dna =  [[] for i in range(len(Son_aux))]            
            for items in range(len(Son_aux)):
                for item in Son_aux[items]:
                    if items == 0:
                        if (item in Son2) == False:
                            if len(Dna[1]) == 0:                                
                                Dna[1].append(item)                                
                            else:
                                if (item in Dna[1]) == False:
                                    Dna[1].append(item)                                    
                    else:
                        if (item in Son1) == False:
                            if len(Dna[0]) == 0:                                
                                Dna[0].append(item)                                
                            else:
                                if (item in Dna[0]) == False:
                                    Dna[0].append(item)
            #print("Datos a agregar al  primer hijo → ", Dna[0], " : ", Son1 , " Datos a agregar al segundo hijo → ", Dna[1], " : ", Son2)
            for items in range(len(Son_aux)):
                if items == 0:                    
                    for data in range(len(Dna[1])):                        
                        come = False
                        for datas in range(len(Son1)):
                            if Dna[1][data] == Son1[datas] and come == False:
                                come = True                                    
                                #print("El dato que se va a cambiar al individuo 1 es → ", Son1[datas], " su posicion es → ", datas, "se va a cambiar por → ", Dna[0][data])
                                Son1[datas] = Dna[0][data]
                else:
                    for data in range(len(Dna[0])):
                        come = False
                        for datas in range(len(Son2)):
                            if Dna[0][data] == Son2[datas] and come == False:
                                come = True                                    
                                #print("El dato que se va a cambiar al individuo 2 es → ", Son2[datas], " su posicion es → ", datas, "se va a cambiar por → ", Dna[1][data])                                        
                                Son2[datas] = Dna[1][data]
            #print(Son1, " : ", Son2)
            Sons.append(Son1)
            Sons.append(Son2)
    SonsMutCross = mutation(Sons, boats)
    return SonsMutCross

def generateShips(boats):
    #comboShips = []
    orderShips =  [[] for i in range(random.randint(int(n_order / 4), int(n_order / 2) ))]
    for items in range(len(orderShips)):
        #orderShips[items].append(order[random.randint(1, len(order)) - 1])
        #print("barcos", items)
        randomsShips = []
        n = 0
        if items == 0:
            while n != boat_N:
                boat = boats[random.randrange(boat_N)] # random.choice(boats) #boats[random.randint(1, boat_N) - 1]  
                if len(orderShips[items]) == 0:
                    orderShips[items].append(boat)
                    n += 1
                else:
                    if (boat in orderShips[items]) != True:
                        orderShips[items].append(boat)
                        n += 1
        else:            
            while n != boat_N:                
                boat = boats[random.randint(1, boat_N) - 1]   # boats[random.randrange(boat_N)] # random.choice(boats) 
                if len(orderShips[items]) < 1:
                    orderShips[items].append(boat)
                    n += 1
                else:
                    if (boat in orderShips[items]) == False:
                        orderShips[items].append(boat)
                        n += 1
                #if n == boat_N and (orderShips[items] in comboShips) == True:
                    #n = 0
                boat = 0                
    #print("Barcos que fueron creados → ", orderShips)
    return orderShips

def mutation(Sons, boats):
    #print(Sons)
    MuationProb = []
    for item in range(len(Sons)):
        MuationProb.append(random.random())        
    #print(MuationProb)
    for item in range(len(MuationProb)):
        if MuationProb[item] <= MutationIndividue:
            #print("Probabilidad de mutación → ", round(MuationProb[item], 4), " Individuo que va a mutar → ", Sons[item])            
            randomIndi1 = random.randrange(boat_N)
            randomIndi2 = random.randrange(boat_N)
            #print("Puntos de mutación →→ ", randomIndi1, " : " , randomIndi2)
            if randomIndi1 == randomIndi2:                
                while randomIndi1 == randomIndi2:
                    randomIndi2 = random.randrange(boat_N)
            #print("Puntos de mutación →→ ", randomIndi1, " : " , randomIndi2)
            datos1 = Sons[item][randomIndi1]
            datos2 = Sons[item][randomIndi2]
            Sons[item][randomIndi1] = datos2
            Sons[item][randomIndi2] = datos1
            #print("individuo mutado → ", Sons[item])
    return Sons    

def selection(datas):
    if datas == 0:
        boatcrossmut = crossover(Boats)
        dat = boatcrossmut[random.randint(1, len(boatcrossmut)) - 1]
        Boats_gen.append(dat)        
    else:
        #boatcrossmut = crossover(Boats)
        #Boats_gen.append(boatcrossmut[random.randint(1, len(boatcrossmut)) - 1])
        f = 0
        one_here = False
        while f != 1:
            one_here = False
            if one_here == False:
                boatcrossmut = crossover(Boats)
                for item in range(len(boatcrossmut)):
                    if one_here == False:
                        if (boatcrossmut[item] in Boats_gen) == False:
                            Boats_gen.append(boatcrossmut[item])
                            one_here = True
                            f = 1
                    if item == len(boatcrossmut) and one_here == False:
                        f = 0
    return Boats_gen[datas]

def Port(order, distance1, item, ship_datas):
    outs1.clear()
    outs2 = []
    arrivals2 = []
    arrivals1.clear()
    out = 0
    object_ship = 0
    print("--------------------------------- Puerto : " + str(item + 1) + " ---------------------------------")    
    print("datos Barco → " , order)
    print("Distancia entre puerto → ",item + 1 , " y pueto → ", item + 2 , " : ",   distance1)    
    if item + 1 == 1:
        for data in range(len(order)):        
            outs2.append(round(out * 0.6,2))
            outs1.append(round(out,2))
            out += 0.25
    else:        
        for datas in range(len(order)):
            outs3 = out + time_aux[datas]
            outs4 = ((outs3 - int(outs3)) * 0.6 ) + int(outs3)
            #print(outs3, " : ", outs4)
            outs2.append(round(outs4,2))
            outs1.append(round(outs3,2))
            out += 0.25    
        time_skip(outs1, .25, ship_datas, 1)
    print("salida P",item +1 ,"→",outs2, " : ", outs1)

    time_aux.clear()

    for datas in range(len(outs1)):            
        object_ship = (distance1 / order[datas]) + outs1[datas]
        arrivals1.append(round(object_ship,2))
        dats = ((object_ship - int(object_ship)) * 0.6) + int(object_ship)
        arrivals2.append(round(dats ,2))    
    
    print("Llegada P", item + 2,"→" , arrivals2, " : ", arrivals1)
    room_Controller(outs1, arrivals1, ship_datas)

def room_Controller(outs1, arrivals1, ship_datas):
    wait_Time.clear()
    wait_Time2 = []
    time_aux2 = []
    for item in range(len(arrivals1)):
        wait_Time1 = random.uniform(min_Time, max_Time)
        wait_Time.append(round(wait_Time1,2))
        dats = ((wait_Time1 - int(wait_Time1)) * 0.6) + int(wait_Time1)
        wait_Time2.append(round(dats, 2))
        dats1 = arrivals1[item] + wait_Time1
        dats2 = ((dats1 - int(dats1)) * 0.6) + int(dats1)
        time_aux.append(round(dats1,2))    
        time_aux2.append(round(dats2,2))
    print("Tiempo de espera → ", wait_Time2, " : ", wait_Time)
    print("Tiempo de espera + llegada → ", time_aux2, " : ", time_aux, "\n")
    time_skip(time_aux, .5, ship_datas, 2)

def time_skip(time, less_time, ship_datas, opcion):
    time_skip1 = []
    time_skip2 = []
    time_skip1.extend(time)    
    time_skip2.extend(time)
    time_skip1.sort()
    delete = []
    list_help = []
    for dat in time_skip1:
        n = 1        
        for item in time_skip1:
            if (dat in delete) != True:
                if dat != item:            
                    if item >= (dat - less_time) and item <= (dat + less_time):
                        print("dato a evaluar → ", dat ," rango de → ", round((dat - less_time), 2), " hasta → ", round((dat + less_time),2), " → ", item)
                        if n >= 2:
                            print("hay mas de 2 barcos en un punto se evalua",dat ," el barco es → ", item)
                            delete.append(item)
                        n += 1                                                
            
    print("datos a eliminar → ",set(delete))
    for target in set(delete):
        list_help.extend(order[ship_datas])
        pos = 0
        for item in range(len(time_skip2)):
            if target == time_skip2[item]:
                print(list_help)
                print(order[ship_datas])
                print(target, " : ", time_skip2[item], " : ", pos, " : ", list_help[pos])
                if opcion == 1:
                    outs1.remove(target)
                order[ship_datas].remove(list_help[pos])
            
            pos += 1
    print(time_skip1, " : ", time_skip2)
    time_skip1.clear()
    time_skip2.clear()

def Graphyc():
    plt.title("Tiempos")
    plt.legend()
    plt.plot(general_time, 'o-', label = " Mejores casos")
    #plt.plot(worst_Fitnnes, 'o-', label = " Peores casos")
    #plt.plot(media_Fitnnes, 'o-', label = "Caso promedio")        
    plt.xlabel("Vueltas")
    plt.ylabel("Tiempo")
    plt.rcParams['toolbar'] = 'None'
    plt.legend()
    plt.show()

if __name__ == '__main__':
    os.system("clear")
    global Boats     
    (Boats , distance1) = Boat()
    ships.clear()    
    (order) = permuta(Boats)    
    print(distance1)    
    Boats_gen_aux = []
    global n_order
    n_order = len(order)
    # print(" \n\n ")
    # print("Cantidad de barcos → ", len(order), " \n Barcos → ", order)
    # print("\n")
    # for item in range(len(order)):
    #     if order.count(order[item]) >= 2:
    #         print("Se encontro que si hay repetidos → ", order[item], " en la posición →", item)
    
    for datas in range(len(order)):
        print("\n -------------------------------------- Vueltas: " + str(datas + 1) + " --------------------------------------")        
        current_boat = selection(datas)        
        Boats_gen_aux.append(str(current_boat))
        order[datas] = current_boat
        print("Dato real → ", current_boat)
        for item in range(N_Ports):            
            Port(order[datas], distance1[item], item, datas)
        time = 0
        for item in range(len(time_aux)):
            time += time_aux[item]                
        general_time.append(round(((time - int(time)) * 0.6) + int(time),2))
        print("Cuantos botes salieron → ", len(order[datas]), " : " , order[datas])
    
    print(" \n\n ")
    print("Cantidad de barcos → ", len(Boats_gen_aux), " \n Barcos → ", Boats_gen_aux)
    print("\n")
    for item in range(len(order)):
        if Boats_gen_aux.count(order[item]) >= 2:
            print("Se encontro que si hay repetidos → ", Boats_gen_aux[item], " en la posición →", item)
    
    print("\n----- otros -----")
    for item in range(len(order)):
        if order.count(order[item]) >= 2:
            print("Se encontro que si hay repetidos → ", order[item], " en la posición →", item, " Veces que aparecio → ", order.count(order[item]))
    
    print(" \n\n ")
    for datas in range(len(order)):
        finish.append(len(order[datas]))
        if len(order[datas]) == boat_N:
            print("Cantidad Barcos → ", len(order[datas]), " Tiempo → ", order[datas])
            best_time.append(general_time[datas])    
    print(" \n\n ")
    print("Mejor tiempo con todos los barcos → ", sorted(best_time)[0])        
    print("\nTiempos de llegada por vuelta de los barcos → ", general_time)
    print("\nCantidad de barcos que pudieron terminar → ", finish)    
    Graphyc()