import simpy
import random


def proceso(env, name, cpu, instrucciones,memoria,t):
    #yield env.timeout(t) #Se espera un tiempo para poder crear el proceso
    print('Se ha creado el proceso #',i)
    creacion = env.now

    with cpu.request() as req: #Se pide al cpu que nos atienda
        yield req



env = simpy.Environment()
cpu = simpy.Resource(env, capacity=1)
tiempoTotal = 0.0
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
interval = 100

for i in range(25):
    t = random.expovariate(1.0/interval)
    ni = random.randint(1,10)
    nm = random.randint(1,10)
    (proceso(env, i, cpu, ni,nm,t))
    


        
        
        
        
        
