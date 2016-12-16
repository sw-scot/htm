#!/usr/bin/env python3

from random import randint
from math import ceil

def gen_list(set_size,min_val,max_val):
    return [randint(min_val,max_val) for _ in range(0,set_size)]

def get_top_cols(vals,top_percent):
    top_cols = []
    hist = {}
    for col in range(len(vals)):
        if vals[col] not in hist:
            hist[vals[col]] = []
        hist[vals[col]].append(col)

    value_buckets = sorted(list(set(hist.keys())))

    value = value_buckets.pop()
    while len(top_cols) < ceil(len(vals) * top_percent):
        print(value)
        if len(hist[value]) == 0:
            value = value_buckets.pop()
        for col in hist[value]:
            top_cols.append(col)
            if len(top_cols) >= ceil(len(vals) * top_percent):
               break

    return top_cols

vals = gen_list(4096,0,100)
top_cols = get_top_cols(vals,0.02)
print(len(top_cols))
