import simpy
import random
import math


def proceso(evento, name, t, cpu, nmt, nm, ni, espera):

    global TT
    global TL
    
    yield evento.timeout(t) #Espera para crearse el proceso
    nmt.get(nm) #Se toma la memoria necesaria de la ram
    t1 = evento.now
    print ('Se creo el %s en el tiempo %s'%(name,t1))
    with  cpu.request() as req:
        yield req
        while (ni>0): #Si posee varias instrucciones
                t2 = evento.now
                print('%s se encuentra en el CPU en el tiempo %s'%(name,t2))
                if (ni>=3):
                    ni = ni - 3 #se restan instrucciones
                    yield evento.timeout(1)
                    if (espera == 2): #por si debe esperar
                        yield evento.timeout(random.randint(1,10))
                else:
                    print('%s esperando en el tiempo %s'%(name,evento.now))
                    ni = 0
        #Calculo de tiempos promedio
        t2 = evento.now
        TP = t2 - t1
        TL.append(TP)
        TT = TT + TP
        nmt.put(nm) #Se devuelve la memoria al container


global NP
TT = 0 #Tiempo total
TL = [] #Lista para guardar los tiempos de cada proceso
NP = 25 #Numero de procesos
random.seed(50) #Seed utilizada
evento = simpy.Environment()
nmt = simpy.resources.container.Container(evento,200, 100)
cpu = simpy.Resource(evento,capacity = 1)
for i in range(NP):
    ins = random.randint(1,10) #No de instrucciones
    nm = random.randint(1,10) #No de memoria necesaria
    espera = random.randint(1,2) #Debe esperar o no?
    t = random.expovariate(1.0/10) #indicado en la guia
    evento.process(proceso(evento,'Proceso #%d'%i,t,cpu,nmt, nm,ins,espera))
    
evento.run() #Empieza simulacion
TT = TT/NP

#Calculo de desviacion estandar
desviacion = 0
for i in range(0,len(TL)):
    x = TL[i]
    x = x - TT
    x = x*x
    desviacion = desviacion + x
    desviacion = desviacion / len(TL)
desviacion = math.sqrt(desviacion)
#Valores para comparar y realizar las graficas
print('El tiempo promedio por proceso es de %7.4f y la desviacion estandar de %7.4f' % (TT,desviacion))

    
    
