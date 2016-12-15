#!/usr/bin/env python3

from random import shuffle
from math import floor, ceil
from copy import copy
from scipy.stats import describe
import pickle

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

        potential_pool[c] = set([cell for cell in cnxn_set])

    return potential_pool, dcell_cnxn_count

data_width = 2**14

potential_pool, dcell_cnxn_count = gen_potential_pool(data_width=data_width, column_count=2**11, connection_density=0.5)
potential_pool_vec = []
for pool in potential_pool:
    pool_vec = [0 for x in range(0,data_width)]
    for cell in pool:
        pool_vec[cell] = 1
    potential_pool_vec.append(pool_vec)

with open('ppool-pset.pkl','wb') as f:
      pickle.dump(potential_pool,f)
with open('ppool-vector.pkl','wb') as f:
      pickle.dump(potential_pool_vec,f)
