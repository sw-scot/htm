#!/usr/bin/env python3

from random import random, randint, shuffle
from math import floor, ceil
from copy import copy

"""
changes to -c:

replace the single active column selector to active columns selection

"""

#-----------------------------------------------------------------------------------------------
# Utility functions
#-----------------------------------------------------------------------------------------------

def display_data(mat):
    print(">>>")
    for m in mat:
        print("".join(str(x) for x in m))
    print("<<<")

def display_perms(mat):
    print(">>>")
    for m in mat:
        fmtstr = []
        for i in range(0,len(m)):
            fmtstr.append("{{0[{}]:0.2f}}".format(i))
        fmtstr = " ".join(fmtstr)
        print(fmtstr.format(m))
    print("<<<")

#-----------------------------------------------------------------------------------------------
# Data structure generators
#-----------------------------------------------------------------------------------------------

def gen_potential_pool(data_width, column_count, connection_density):

    # [column : [potential pool]]
    potential_pool = [[] for _ in range(0,column_count)]

    dcells_per_col = ceil(data_width * connection_density)
    avg_col_per_dcell = (column_count * connection_density)
    dcell_cnxn_count = {}
    candidate_cells_template = [x for x in range(data_width)]

    for c in range(column_count):
        candidate_cells = copy(candidate_cells_template)
        shuffle(candidate_cells)
        cnxn_set = set()
        while len(cnxn_set) < dcells_per_col:
            candidate = candidate_cells.pop(0)


            if candidate not in dcell_cnxn_count:
                dcell_cnxn_count[candidate] = 0

            #if dcell_cnxn_count[candidate] > avg_col_per_dcell:
            #    continue

            if candidate not in cnxn_set:
                dcell_cnxn_count[candidate] += 1
                cnxn_set.add(candidate)

        potential_pool[c] = [0 for x in range(0,data_width)]
        for cell in cnxn_set:
             potential_pool[c][cell] = 1

    return potential_pool

def gen_connection_permanence(data_width, column_count, potential_pool):
    connection_permanence = []
    for i in range(0,column_count):
        connection_permanence.append([random() * potential_pool[i][x] for x in range(0,data_width)])
    return connection_permanence


def gen_region(col_count,cell_count):
    region = []
    for i in range(0,col_count):
        region.append([0 for x in range(0,cell_count)])
    return region


def gen_data(data_width,sample_count,data_sparsity):
    data = []
    n_cells = floor(data_width * data_sparsity)
    for i in range(0,sample_count):
        d = [0 for x in range(0,data_width)]
        active_bits = [randint(0,data_width-1) for x in range(0,n_cells)]
        for bit in active_bits:
            d[bit] = 1
        data.append(d)
    return data

#-----------------------------------------------------------------------------------------------
# Network constants
#-----------------------------------------------------------------------------------------------

PERMANENCE_THRESHOLD      = 0.2

CONNECTION_PERMANENCE_INC = 0.03
CONNECTION_PERMANENCE_DEC = 0.01

COLUMN_COUNT              = 256
COLUMN_CELL_COUNT         = 5
COLUMN_CONNECTION_DENSITY = 0.5

DATA_WIDTH                = 2048
DATA_SAMPLE_COUNT         = 100
DATA_SPARSITY             = 0.02

#-----------------------------------------------------------------------------------------------
# Create data structures
#-----------------------------------------------------------------------------------------------

data                  = gen_data(DATA_WIDTH, DATA_SAMPLE_COUNT, DATA_SPARSITY)
region                = gen_region(COLUMN_COUNT, COLUMN_CELL_COUNT)
potential_pool        = gen_potential_pool(DATA_WIDTH, COLUMN_COUNT, COLUMN_CONNECTION_DENSITY)
connection_permanence = gen_connection_permanence(DATA_WIDTH, COLUMN_COUNT, potential_pool)


#-----------------------------------------------------------------------------------------------
# Calculate the winning column, and update potential pool permanences
#-----------------------------------------------------------------------------------------------
#
#    for all potential pool connections for a column
#        if connected cell is active and is connected: total_active += 1, connection_permanence += connection_permanence_inc
#        if connected cell is inactive and is connected: connection_permanence -= connection_permanence_dec
#        if connected cell is inactive and is not connected: connection_permanence += connection_permanence_inc
#    col_active_count = total_active
#

#display_perms(connection_permanence)

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

#display_perms(connection_permanence)
