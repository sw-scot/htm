#!/usr/bin/env python3

from random import random, randint

def display_matrix(mat):
    print(">>>")
    for m in mat:
        print("{0:0.2f} {1:0.2f} {2:0.2f} {3:0.2f} {4:0.2f} {5:0.2f} {6:0.2f} {7:0.2f} {8:0.2f} {9:0.2f}".format(
            m[0],
            m[1],
            m[2],
            m[3],
            m[4],
            m[5],
            m[6],
            m[7],
            m[8],
            m[9],
            ))
    print("<<<")

potential_pool = [
    [1,1,1,1,1,0,0,0,0,0],
    [0,1,1,1,1,1,0,0,0,0],
    [0,0,1,1,1,1,1,0,0,0],
    [0,0,0,1,1,1,1,1,0,0],
    [0,0,0,0,1,1,1,1,1,0],

    [0,0,0,0,0,1,1,1,1,1],
    [1,0,0,0,0,0,1,1,1,1],
    [1,1,0,0,0,0,0,1,1,1],
    [1,1,1,0,0,0,0,0,1,1],
    [1,1,1,1,0,0,0,0,0,1]]

connection_permanence = [
    [random() * potential_pool[0][x] for x in range(0,10)],
    [random() * potential_pool[1][x] for x in range(0,10)],
    [random() * potential_pool[2][x] for x in range(0,10)],
    [random() * potential_pool[3][x] for x in range(0,10)],
    [random() * potential_pool[4][x] for x in range(0,10)],

    [random() * potential_pool[5][x] for x in range(0,10)],
    [random() * potential_pool[6][x] for x in range(0,10)],
    [random() * potential_pool[7][x] for x in range(0,10)],
    [random() * potential_pool[8][x] for x in range(0,10)],
    [random() * potential_pool[9][x] for x in range(0,10)]]


region = [
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],

    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0]]


data = [
    [1,1,1,0,0,0,0,0,0,0],
    [0,1,1,1,0,0,0,0,0,0],
    [0,0,1,1,1,0,0,0,0,0],
    [0,0,0,1,1,1,0,0,0,0],
    [0,0,1,1,1,0,0,0,0,0],
    [0,1,1,1,0,0,0,0,0,0],
    [1,1,1,0,0,0,0,0,0,0]]


"""
    for all potential pool connections for a column
        if connected cell is active and is connected: total_active += 1, connection_permanence += connection_permanence_inc
        if connected cell is inactive and is connected: connection_permanence -= connection_permanence_dec
        if connected cell is inactive and is not connected: connection_permanence += connection_permanence_inc
    col_active_count = total_active
"""

PERMANENCE_THRESHOLD = 0.2
CONNECTION_PERMANENCE_INC = 0.03
CONNECTION_PERMANENCE_DEC = 0.01

display_matrix(connection_permanence)
for d in data:
    col_active_count = [0,0,0,0,0,0,0,0,0,0]
    for col in range(0,10):
        total_active = 0
        for cell_id in range(0,10):
            if d[cell_id] == 1 and connection_permanence[col][cell_id] > PERMANENCE_THRESHOLD:
                total_active += 1
                connection_permanence[col][cell_id] += CONNECTION_PERMANENCE_INC
                if connection_permanence[col][cell_id] > 1:
                    connection_permanence[col][cell_id] = 1
            elif d[cell_id] == 0 and connection_permanence[col][cell_id] > PERMANENCE_THRESHOLD:
                connection_permanence[col][cell_id] -= CONNECTION_PERMANENCE_DEC
                if connection_permanence[col][cell_id] < 0:
                    connection_permanence[col][cell_id] = 0
            elif d[cell_id] == 1 and connection_permanence[col][cell_id] < PERMANENCE_THRESHOLD:
                connection_permanence[col][cell_id] += CONNECTION_PERMANENCE_INC
                if connection_permanence[col][cell_id] > 1:
                    connection_permanence[col][cell_id] = 1
        col_active_count[col] = total_active
    max_col_active_count = max(col_active_count)
    cnt_col_active_at_max = col_active_count.count(max_col_active_count)
    max_count_winner = randint(0,cnt_col_active_at_max-1)
    idx_col_active_at_max = 0
    for col in range(0,len(col_active_count)):
        if col_active_count[col] == max_col_active_count:
            if idx_col_active_at_max == max_count_winner:
                winning_column = col
                break
            else:
               idx_col_active_at_max += 1
    print(winning_column)
     
display_matrix(connection_permanence)
