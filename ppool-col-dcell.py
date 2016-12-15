#!/usr/bin/env python3

from math import ceil
from random import randint, seed, shuffle

def gen_potential_pool(data_width, column_count, connection_density):

    # [column : [potential pool]]
    potential_pool = [[] for _ in range(column_count)]

    # number of columns each data cell will be associated with
    dcell_cnxn_counts = {}

    # ideal number of columns each data cell is associated with
    #cols_per_dcell = ceil((data_width / column_count) / connection_density)
    cols_per_dcell = connection_density

    # number of data cells each column is associated with
    dcells_per_col = ceil(data_width / 2)

    print("cols_per_dcell: ",cols_per_dcell)
    print("dcells_per_col: ",dcells_per_col)

    for c in range(0,column_count):
        print(">>>> col:",c)

        cnxn_set = set()
        candidate_cells = [x for x in range(0,data_width)]
        shuffle(candidate_cells)
        while len(cnxn_set) < dcells_per_col:
            if 0 == len(candidate_cells):
                print(c,"Ran out of candidates, aborting")
                break
            candidate_cell = candidate_cells.pop(0)
            if candidate_cell not in dcell_cnxn_counts:
                dcell_cnxn_counts[candidate_cell] = 0
            if dcell_cnxn_counts[candidate_cell] < cols_per_dcell:
                dcell_cnxn_counts[candidate_cell] += 1
                cnxn_set.add(candidate_cell)
        print("cnxn_set ",len(cnxn_set))
        if len(cnxn_set) != dcells_per_col:
            print("Cannot converge, aborting")
            exit(0)

        for connected_cell in cnxn_set:
            potential_pool[c].append(connected_cell)
    

    return potential_pool


if __name__ == "__main__":
    seed(1)
    potential_pool = gen_potential_pool(data_width=16384,column_count=2048,connection_density=64)
    #potential_pool = gen_potential_pool(data_width=16384,column_count=2048,connection_density=0.5)
    #potential_pool = gen_potential_pool(data_width=16,column_count=8,connection_density=0.5)
    print(potential_pool)
    for col in potential_pool:
        print(len(col))
