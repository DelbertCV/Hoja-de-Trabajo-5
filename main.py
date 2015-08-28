import simpy
import random


def proceso(env,name,memoria,instrucciones,t):
    yield env.timeout(t)
    print('Se ha creado el proceso #%s en el tiempo %s'%(name,env.now))
    creacion = env.now

    with cpu.request() as req: #Se pide al cpu que nos atienda
        yield req
    
    
