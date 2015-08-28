import simpy
import random
import math


def proceso(evento, name, t, cpu, nmt, nm, ni, espera):

    global TT
    global TL
    
    yield evento.timeout(t)
    nmt.get(nm)
    t1 = evento.now
    print ('Se creo el %s en el tiempo %s'%(name,t1))
    with  cpu.request() as req:
        yield req
        while (ni>0):
                t2 = evento.now
                print('%s se encuentra en el CPU en el tiempo %s'%(name,t2))
                if (ni>=3):
                    ni = ni - 3
                    yield evento.timeout(1)
                    if (espera == 2):
                        yield evento.timeout(random.randint(1,10))
                else:
                    print('%s esperando en el tiempo %s'%(name,evento.now))
                    ni = 0
        t2 = evento.now
        TP = t2 - t1
        TL.append(TP)
        TT = TT + TP
        print('%s termina en el tiempo %s'%(name,t2))
        T = TT/NP
        print('El tiempo promedio  es de %7.4f'%(T))
        nmt.put(nm)


global NP
TT = 0
TL = []
NP = 25
random.seed(50)
evento = simpy.Environment()
nmt = simpy.Container(evento,200, 100)
cpu = simpy.Resource(evento,capacity = 1)
for i in range(NP):
    ins = random.randint(1,10)
    nm = random.randint(1,10)
    espera = random.randint(1,2)
    t = random.expovariate(1.0/10)
    evento.process(proceso(evento,'Proceso #%d'%i,t,cpu,nmt, nm,ins,espera))
    
evento.run()
TT = TT/NP

desviacion = 0
for i in range(0,len(TL)):
    x = TL[i]
    x = x - TT
    x = x*x
    desviacion = desviacion + x
    desviacion = desviacion / len(TL)
desviacion = math.sqrt(desviacion)

print('El tiempo promedio por proceso es de %7.4f y la desviacion estandar de %7.4f' % (TT,desviacion))

    
    
