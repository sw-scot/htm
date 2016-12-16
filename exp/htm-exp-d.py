#!/usr/bin/env python3

from random import random, randint, shuffle, seed
from math import floor, ceil
from copy import copy

"""
changes to -d:

class-ify the stuff

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

class SpatialPooler():
    #-----------------------------------------------------------------------------------------------
    # Network constants
    #-----------------------------------------------------------------------------------------------

    PERMANENCE_THRESHOLD      = 0.2

    CONNECTION_PERMANENCE_INC = 0.03
    CONNECTION_PERMANENCE_DEC = 0.01

    COLUMN_COUNT              = 256
    COLUMN_CELL_COUNT         = 5
    COLUMN_CONNECTION_DENSITY = 0.5
    COLUMN_ACTIVATION_DENSITY = 0.02

    DATA_WIDTH                = 2048
    DATA_SAMPLE_COUNT         = 100
    DATA_SPARSITY             = 0.2

    def __init__(self):
        #-----------------------------------------------------------------------------------------------
        # Create data structures
        #-----------------------------------------------------------------------------------------------

        self.region                = self.gen_region(self.COLUMN_COUNT, self.COLUMN_CELL_COUNT)
        self.potential_pool        = self.gen_potential_pool(self.DATA_WIDTH, self.COLUMN_COUNT, self.COLUMN_CONNECTION_DENSITY)
        self.connection_permanence = self.gen_connection_permanence(self.DATA_WIDTH, self.COLUMN_COUNT, self.potential_pool)

    #-----------------------------------------------------------------------------------------------
    # Data structure generators
    #-----------------------------------------------------------------------------------------------

    def gen_potential_pool(self, data_width, column_count, connection_density):
    
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

    def gen_connection_permanence(self, data_width, column_count, potential_pool):
        connection_permanence = []
        for i in range(0,column_count):
            connection_permanence.append([random()/2 * potential_pool[i][x] for x in range(0,data_width)])
        return connection_permanence


    def gen_region(self, col_count, cell_count):
        region = []
        for i in range(0,col_count):
            region.append([0 for x in range(0,cell_count)])
        return region


    def gen_data(self, data_width, sample_count, data_sparsity):
        data = []
        n_cells = floor(data_width * data_sparsity)
        for i in range(0,sample_count):
            d = [0 for x in range(0,data_width)]
            active_bits = [randint(0,data_width-1) for x in range(0,n_cells)]
            for bit in active_bits:
                d[bit] = 1
            data.append(d)
        return data

    def find_winning_columns(self,col_active_count,top_percent):
        top_cols = []
        cols_by_value = {}
        for col in range(len(col_active_count)):
            if col_active_count[col] not in cols_by_value:
                cols_by_value[col_active_count[col]] = []
            cols_by_value[col_active_count[col]].append(col)

        value_buckets = sorted(list(set(cols_by_value.keys())))

        value = value_buckets.pop()
        values = []
        values.append(value)
        while len(top_cols) < ceil(len(col_active_count) * top_percent):
            if len(cols_by_value[value]) == 0:
                value = value_buckets.pop()
                values.append(value)
            for col in cols_by_value[value]:
                top_cols.append(col)
                if len(top_cols) >= ceil(len(col_active_count) * top_percent):
                   break

        return top_cols, values, value_buckets

    def compute_cols(self,d):
        """
        -----------------------------------------------------------------------------------------------
         Calculate the winning column, and update potential pool permanences
        -----------------------------------------------------------------------------------------------
    
            for all potential pool connections for a column
                if connected cell is active and is connected: total_active += 1, connection_permanence += connection_permanence_inc
                if connected cell is inactive and is connected: connection_permanence -= connection_permanence_dec
                if connected cell is inactive and is not connected: connection_permanence += connection_permanence_inc
            col_active_count = total_active
        """
    
        col_active_count = [0 for _ in range(0,self.COLUMN_COUNT)]
        for col in range(0,self.COLUMN_COUNT):
            total_active = 0
            for cell_id in range(0,10):
                if d[cell_id] == 1 and self.connection_permanence[col][cell_id] > self.PERMANENCE_THRESHOLD:
                    total_active += 1
                    self.connection_permanence[col][cell_id] += self.CONNECTION_PERMANENCE_INC
                    if self.connection_permanence[col][cell_id] > 1:
                        self.connection_permanence[col][cell_id] = 1
                elif d[cell_id] == 0 and self.connection_permanence[col][cell_id] > self.PERMANENCE_THRESHOLD:
                    self.connection_permanence[col][cell_id] -= self.CONNECTION_PERMANENCE_DEC
                    if self.connection_permanence[col][cell_id] < 0:
                        self.connection_permanence[col][cell_id] = 0
                elif d[cell_id] == 1 and self.connection_permanence[col][cell_id] < self.PERMANENCE_THRESHOLD:
                    self.connection_permanence[col][cell_id] += self.CONNECTION_PERMANENCE_INC
                    if self.connection_permanence[col][cell_id] > 1:
                        self.connection_permanence[col][cell_id] = 1
            col_active_count[col] = total_active
        winning_columns = self.find_winning_columns(col_active_count, self.COLUMN_ACTIVATION_DENSITY)
        return winning_columns


if __name__ == "__main__":
    sp = SpatialPooler() 
    data = sp.gen_data(sp.DATA_WIDTH, sp.DATA_SAMPLE_COUNT, sp.DATA_SPARSITY)
    for d in data:
        print("---")
        cols, values, buckets = sp.compute_cols(d)
        print("cols: ",cols) 
        print("vals: ",values) 
        print("bkts: ",values) 
