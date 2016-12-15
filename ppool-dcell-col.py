#!/usr/bin/env python3

from math import ceil
from random import randint

def gen_potential_pool(data_width, column_count, connection_density):

    # [column : [potential pool]]
    potential_pool = [[] for _ in range(column_count)]
    colcell_to_dcell_counts = {}

    # number of columns each data cell will be connected to
    cols_per_dcell = ceil((data_width / column_count) / connection_density)
    dcells_per_col = ceil(data_width / 2)

    for d in range(0,data_width):
        #print(">>>> data cell:",d)
        cnxn_set = set()
        stuck_counter = 0
        while len(cnxn_set) < cols_per_dcell:
            if stuck_counter > 100:
                break
            candidate_col = randint(0,column_count-1)
            if candidate_col in cnxn_set:
                next
            if candidate_col not in colcell_to_dcell_counts:
                colcell_to_dcell_counts[candidate_col] = 0
            if colcell_to_dcell_counts[candidate_col] < dcells_per_col:
                colcell_to_dcell_counts[candidate_col] += 1
                cnxn_set.add(candidate_col)
            stuck_counter += 1
        #print("cnxn_set ",len(cnxn_set),": ",",".join(str(x) for x in cnxn_set))
        #print("counts  :",colcell_to_dcell_counts)
        for connected_cell in cnxn_set:
            potential_pool[connected_cell].append(d)
    

    return potential_pool


if __name__ == "__main__":
    potential_pool = gen_potential_pool(data_width=16384,column_count=2048,connection_density=0.5)
    #potential_pool = gen_potential_pool(data_width=16,column_count=8,connection_density=0.5)
    print(potential_pool)
    for col in potential_pool:
        print(len(col))




"""
 
1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 - 0
^             ^
1 2 2 2 2 2 2 2 1 0 0 0 0 0 0 0 - 1
  ^             ^
1 2 3 3 3 3 3 3 2 1 0 0 0 0 0 0 - 2
    ^             ^
1 2 3 4 4 4 4 4 3 2 1 0 0 0 0 0 - 3
      ^             ^
1 2 3 4 5 5 5 5 4 3 2 1 0 0 0 0 - 4
        ^             ^
1 2 3 4 5 6 6 6 5 4 3 2 1 0 0 0 - 5
          ^             ^
1 2 3 4 5 7 7 7 6 5 4 3 2 1 0 0 - 6
            ^             ^
1 2 3 4 5 7 7 8 7 6 5 4 3 2 1 0 - 7
              ^             ^

1 2 3 4 5 7 7 8 7 6 5 4 3 2 1 0
1 2 3 4 5 7 7 7 7 6 5 4 3 2 1 1
2 2 3 4 5 6 7 7 7 6 5 4 3 2 1 1
2 2 3 4 5 6 6 7 7 6 5 4 3 2 2 1
2 2 3 4 5 6 6 6 7 6 5 4 3 2 2 2
3 2 3 4 5 6 6 6 6 6 5 4 3 2 2 2
3 3 3 4 5 5 6 6 6 6 5 4 3 2 2 2
3 3 3 4 5 5 5 6 6 6 5 4 3 3 2 2
3 3 3 4 5 5 5 5 6 6 5 4 3 3 3 2
3 3 3 4 5 5 5 5 5 6 5 4 3 3 3 3
4 3 3 4 5 5 5 5 5 5 5 4 3 3 3 3
4 4 3 4 4 5 5 5 5 5 5 4 3 3 3 3
4 4 4 4 4 4 5 5 5 5 5 4 3 3 3 3
4 4 4 4 4 4 4 5 5 5 5 4 4 3 3 3
4 4 4 4 4 4 4 4 5 5 5 4 4 4 3 3
4 4 4 4 4 4 4 4 4 5 5 4 4 4 4 3
4 4 4 4 4 4 4 4 4 4 5 4 4 4 4 4


"""
