#!/usr/bin/env python3

from eris import SpatialPooler

if __name__ == "__main__":
    sp = SpatialPooler() 
    data = sp.gen_data(sp.DATA_WIDTH, sp.DATA_SAMPLE_COUNT, sp.DATA_SPARSITY)
    for d in data:
        print("---")
        cols, values, buckets = sp.compute_cols(d)
        print("cols: ",cols) 
        print("vals: ",values) 
        print("bkts: ",values) 
