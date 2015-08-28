import simpy
import random
import math


def proceso(evento, name, t, cpu, nmt, nm, ni, espera):

    global TT #Tiempo Total
    global TL #Lista con los tiempos individuales
    
    yield evento.timeout(t)
    nmt.get(nm) #Se solicita ram
    t1 = evento.now
    print ('Se creo el %s en el tiempo %s'%(name,t1))
    with  cpu.request() as req:
        yield req
        while (ni>0): #Instrucciones que se llevaran a cabo
                t2 = evento.now
                print('%s se encuentra en el CPU en el tiempo %s'%(name,t2))
                if (ni>=3):
                    ni = ni - 3 #Se restan 3 para las instrucciones restantes
                    yield evento.timeout(1)
                    if (espera == 2):
                        yield evento.timeout(random.randint(1,10))
                else:
                    print('%s esperando en el tiempo %s'%(name,evento.now))
                    ni = 0
        #Calculos para el tiempo promedio por proceso
        t2 = evento.now
        TP = t2 - t1
        TL.append(TP)
        TT = TT + TP
        T = TT/NP
        nmt.put(nm) #Se devuelve la ram a memoria


global NP
TT = 0 #Tiempo tota;
TL = [] #Lista para los tiempos
NP = 25 #numero de procesos
random.seed(50) #seed para poder comparar
evento = simpy.Environment()
nmt = simpy.Container(evento,200, 100) #Container con el No total de memoria
cpu = simpy.Resource(evento,capacity = 1) #Cola del cpu
for i in range(NP):
    ins = random.randint(1,10) #Numero de instrucciones
    nm = random.randint(1,10) #Numero de memoria necesaria
    espera = random.randint(1,2)  #debe esperar o no?
    t = random.expovariate(1.0/10) #Intervalos
    evento.process(proceso(evento,'Proceso #%d'%i,t,cpu,nmt, nm,ins,espera))
    
evento.run() #Simulacion
TT = TT/NP #Tiempo promedo por proceso

#Calculo de la desviacion
desviacion = 0
for i in range(0,len(TL)):
    x = TL[i]
    x = x - TT
    x = x*x
    desviacion = desviacion + x
    desviacion = desviacion / len(TL)
desviacion = math.sqrt(desviacion)
#Impresion de resultados
print('El tiempo promedio por proceso es de %7.4f y la desviacion estandar de %7.4f' % (TT,desviacion))

    
    
