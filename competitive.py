#!/usr/bin/env python3

from numpy import array, dot, random, argmax, sum, zeros

def display(v):
    import matplotlib.pyplot as plt
    #plt.imshow(v,interpolation='nearest')
    plt.imshow(v)
    plt.gray()
    plt.grid()
    plt.show()

def gen_sensor_data(samples=10,bits=8):
    return random.randint(2, size=(samples,bits))

def gen_weights():
    weights = random.rand(8,8)
    for i in range(0,len(weights)):
        total = sum(weights[i])
        weights[i] = weights[i] / total
    return weights

def find_winning_node(node_values):
    return argmax(node_values)

def main():
    sensor_data = gen_sensor_data()
    weights = gen_weights()
    epsilon = 0.01

    for datum in sensor_data:
        activation_values = datum.T.dot(weights)
        winning_node = find_winning_node(activation_values)
        nactive = sum(datum)
        dweight = epsilon * ((datum / nactive) - weights[winning_node])
        weights[winning_node] += dweight
    display(weights)

if __name__ == "__main__":
    main()



