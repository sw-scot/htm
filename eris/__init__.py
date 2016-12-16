
class HTM:
    def __init__(self,config_name):
        self.load_config(config_name)
        self.sp = SpatialPooler(self.config)
        self.tp = TemporalPooler(self.config)

    def load_config(self,config_name):
        import os
        if not os.path.isdir('db/'+config_name):
            print("Cannot find dir db/{}".format(config_name))
        if not os.path.isfile('db/{}/config.py'.format(config_name)):
            print("Cannot find file db/"+config_name+'/config.py')

        from configparser import ConfigParser
        config = ConfigParser()
        config.read('db/{}/config.py'.format(config_name))
        self.config = config['HTM']

        self.config['SP_POTENTIAL_POOL_PKL'] = 'db/{}/sp_potential_pool.pkl'.format(config_name)
        self.config['SP_CONNECTION_PERMANENCE_PKL'] = 'db/{}/sp_connection_permanence.pkl'.format(config_name)
        self.config['TP_REGION_PKL'] = 'db/{}/tp_region.pkl'.format(config_name)
        
class TemporalPooler:

    def __init__(self,config):
        self.config = config
        self.COLUMN_COUNT              = int(config['COLUMN_COUNT'])
        self.COLUMN_CELL_COUNT         = int(config['COLUMN_CELL_COUNT'])

        self.load_region()
       
    def load_region(self):
        import os, pickle
        region = []
        if os.path.isfile(self.config['TP_REGION_PKL']):
            with open(self.config['TP_REGION_PKL'],"rb") as f:
                self.region = pickle.load(f)
        else:
            self.region = self.gen_region(self.COLUMN_COUNT, self.COLUMN_CELL_COUNT)
            with open(self.config['TP_REGION_PKL'],"wb") as f:
                pickle.dump(self.region,f)

    def gen_region(self, col_count, cell_count):
        region = []
        for i in range(0,col_count):
            region.append([0 for x in range(0,cell_count)])
        return region

    def propogate(self,cols):
        pass

from random import random, randint, shuffle, seed
from math import floor, ceil
from copy import copy
class SpatialPooler:

    def __init__(self,config):
        
        self.config = config

        #-----------------------------------------------------------------------------------------------
        # Network constants
        #-----------------------------------------------------------------------------------------------

        self.PERMANENCE_THRESHOLD      = float(config['PERMANENCE_THRESHOLD'])
        self.CONNECTION_PERMANENCE_INC = float(config['CONNECTION_PERMANENCE_INC'])
        self.CONNECTION_PERMANENCE_DEC = float(config['CONNECTION_PERMANENCE_DEC'])

        self.COLUMN_COUNT              = int(config['COLUMN_COUNT'])
        self.COLUMN_CELL_COUNT         = int(config['COLUMN_CELL_COUNT'])
        self.COLUMN_CONNECTION_DENSITY = float(config['COLUMN_CONNECTION_DENSITY'])
        self.COLUMN_ACTIVATION_DENSITY = float(config['COLUMN_ACTIVATION_DENSITY'])

        self.DATA_WIDTH                = int(config['DATA_WIDTH'])
        self.DATA_SAMPLE_COUNT         = int(config['DATA_SAMPLE_COUNT'])
        self.DATA_SPARSITY             = float(config['DATA_SPARSITY'])

        #-----------------------------------------------------------------------------------------------
        # Load/create data structures
        #-----------------------------------------------------------------------------------------------

        self.load_potential_pool()
        self.load_connection_permanence()

    #-----------------------------------------------------------------------------------------------
    # Data structure generators
    #-----------------------------------------------------------------------------------------------

    def load_potential_pool(self):
        import os, pickle
        if os.path.isfile(self.config['SP_POTENTIAL_POOL_PKL']):
            with open(self.config['SP_POTENTIAL_POOL_PKL'],"rb") as f:
                self.potential_pool = pickle.load(f)
        else:
            self.potential_pool = self.gen_potential_pool(self.DATA_WIDTH, self.COLUMN_COUNT, self.COLUMN_CONNECTION_DENSITY)
            with open(self.config['SP_POTENTIAL_POOL_PKL'],"wb") as f:
                pickle.dump(self.potential_pool,f)

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

    def load_connection_permanence(self):
        import os, pickle
        if os.path.isfile(self.config['SP_CONNECTION_PERMANENCE_PKL']):
            with open(self.config['SP_CONNECTION_PERMANENCE_PKL'],"rb") as f:
                self.connection_permanence = pickle.load(f)
        else:
            self.connection_permanence = self.gen_connection_permanence(self.DATA_WIDTH, self.COLUMN_COUNT, self.potential_pool)
            with open(self.config['SP_CONNECTION_PERMANENCE_PKL'],"wb") as f:
                pickle.dump(self.connection_permanence,f)

    def gen_connection_permanence(self, data_width, column_count, potential_pool):
        connection_permanence = []
        for i in range(0,column_count):
            connection_permanence.append([random()/2 * potential_pool[i][x] for x in range(0,data_width)])
        return connection_permanence


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
        if len(value_buckets) == 1 and value_buckets[0] == 0:
            return [], [], []

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
