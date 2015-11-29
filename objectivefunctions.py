# -*- coding: utf-8 -*-
"""
@author: Valérie Daras, Julie Rivière
"""
def calculateWeight(s1,s2,graph):
    # 0 is default value if (s1-s2) doesn't exist
    try:
        value = graph.get_edge_data(s1,s2,0)['weight']
    except (TypeError):
        value = 0
    return value

    
# a tester    
def calculateCut(p1,p2,graph):
    result = 0
    for s1 in p1:
        for s2 in p2:
            result = result + calculateWeight(s1,s2,graph)
    return result 
    
# a tester    
def calculateCutPk(pk,graph):
    result = 0
    for s1 in range(len(pk)):
        for s2 in range(s1+1, len(pk)):
            result = result + calculateCut(s1,s2,graph)
    return result 
    
# a tester    
def calculateRatioCut(pk,graph):
    result = 0
    ## TODO
    return result 