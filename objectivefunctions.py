# -*- coding: utf-8 -*-
"""
@author: Valérie Daras, Julie Rivière
"""

# Fonction permettant de calculer la valuation 
# entre les sommets s1 et s2 dans graph
# retourne 0 si s1 et s2 ne sont pas voisins
def calculateWeight(s1,s2,graph):
    # 0 is default value if (s1-s2) doesn't exist
    try:
        value = graph.get_edge_data(s1,s2,0)['weight']
    except (TypeError):
        value = 0
    return value

    
# Fonction qui calcule le coût de la coupe 
# entre les partitions p1 et p2 dans graph
def calculateCut(p1,p2,graph):
    result = 0
    for s1 in p1:
        for s2 in p2:
            result = result + calculateWeight(s1,s2,graph)
    return result 
    
# Fonction qui calcule le coût de la coupe 
# entre toutes les partitions pk dans graph
def calculateCutPk(pk,graph):
    result = 0
    for p1 in range(len(pk)):
        for p2 in range(p1+1, len(pk)):
            result = result + calculateCut(p1,p2,graph)
    return result 
    
# a tester    
def calculateRatioCut(pk,graph):
    result = 0
    ## TODO
    return result 