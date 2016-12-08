#!/usr/bin/env python3

from random import randint

def gen_sensor_data():
    sd = []
    sd.append([1,1,1,0,0,0, 1,0])
    sd.append([0,1,1,1,0,0, 1,0])
    sd.append([0,0,1,1,1,0, 1,0])
    sd.append([0,0,0,1,1,1, 1,0])
    sd.append([1,0,0,0,1,1, 1,0])
    sd.append([1,1,0,0,0,1, 1,0])
    return sd

def gen_pooler(dw,w=10,d=10):
    pooler = []
    permanence = []
    for i in range(0,w):
        pooler.append([randint(0,1) for x in range(0,d)])
        permanence.append([0.1 for x in range(0,dw)])
    return pooler, permanence

sensor_data = gen_sensor_data()
pooler, permanence = gen_pooler(len(sensor_data[0]))
print(sensor_data)
print(pooler)
print(permanence)

# each pooler column sees all sensor_data values

for datum in sensor_data:
    pass
