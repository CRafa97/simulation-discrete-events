from random import random
import math

def inverse_method(f):
    u = random()
    x = 0
    acum = 0
    for y, p in f:
        acum += p
        if u < acum:
            x = y
            break
    return x

def uniform(a, b):
    u = random()
    x = a + (b - a)*u
    return x

def exponential(lamb):
    u = random()
    x = - (1 / lamb) * math.log(u)
    return x

def normal(mean, var):
    x = 0
    while True:
        y = exponential(1)
        u = random()
        c = math.exp((-(y - 1)**2) / 2)
        if u <= c:
            x = mean + var*y
            break 
    return x

def poisson_process(lamb, T):
    s = []
    t = 0
    I = 0 
    while True:
        u = random()
        t += exponential(lamb)
        if t > T:
            break
        I += 1
        s.append((I, t))
    return s

def non_homogeneous_poisson(lamb, intensity, T):
    s = []
    t = 0
    I = 0
    while True:
        u = random()
        t += exponential(lamb)
        if t > T:
            break
        u_p = random()
        if u_p <= intensity(t) / lamb: 
            I += 1
            s.append((I, t))
    return s