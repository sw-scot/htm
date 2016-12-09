#!/usr/bin/env python3

from random import randint, random, seed

def gen_sensor_data():
    sd = []
    sd.append([1,1,1,0,0,0, 1,0])
    sd.append([0,1,1,1,0,0, 1,0])
    sd.append([0,0,1,1,1,0, 1,0])
    sd.append([0,0,0,1,1,1, 1,0])
    sd.append([1,0,0,0,1,1, 1,0])
    sd.append([1,1,0,0,0,1, 1,0])
    return sd

def gen_pooler(data_width,cols=256,cells=64):
    pooler = []
    permanence = []
    for i in range(0,cols):
        pooler.append([0 for x in range(0,cells)])
        permanence.append([random()/4 for x in range(0,data_width)])
    return pooler, permanence

def get_top_cols(scores):
    score_bucket = {}
    for i in range(0,len(scores)):
        if scores[i] not in score_bucket:
            score_bucket[scores[i]] = []
        score_bucket[scores[i]].append(i)
    sorted_scores = sorted(score_bucket.keys())
    return score_bucket[sorted_scores[-1:][0]]
    

sensor_data = gen_sensor_data()
pooler, permanence = gen_pooler(len(sensor_data[0]))

# each pooler column sees all sensor_data values

seed(7)
threshold = 0.2
for datum in sensor_data:
    print("Datum: ",datum)
    # compute overlap score for each column
    overlap_scores = []
    for c in range(0,len(pooler)):
        score = 0
        for d in range(0,len(datum)):
            if 1 == datum[d] and permanence[c][d] > threshold:
                score += 1
        overlap_scores.append(score)
    top_cols = get_top_cols(overlap_scores)

    # update sensor to pooler permanence

    for c in range(0,len(pooler)):
        for d in range(0,len(datum)):
            if 1 == datum[d] and permanence[c][d] >= threshold:
                permanence[c][d] += 0.08
            elif 0 == datum[2] and permanence[c][d] >= threshold:
                permanence[c][d] -= 0.03

    # 
