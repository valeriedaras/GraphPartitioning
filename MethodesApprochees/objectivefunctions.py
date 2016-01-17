# -*- coding: utf-8 -*-
"""
@author: Valérie Daras, Julie Rivière
"""

import networkx as nx

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

# 
def nodeGain(node,partition,graph):
    nbNeighborsIn = 0
    nbNeighborsOut = 0
    for neighbors in nx.all_neighbors(graph,node):
        if neighbors in partition:
            nbNeighborsIn += 1
        else:
            nbNeighborsOut +=1
    #print node
    #print "voisins dans A:", nbNeighborsInA, "voisins dans B:", nbNeighborsInB
    return nbNeighborsOut - nbNeighborsIn


def associateGain(A,B,graph):
    newDictA = {}
    newDictB = {}
    for node in A:
        gain = nodeGain(node,A,graph)
        newDictA[node] = gain
    for node in B:
        gain = nodeGain(node,B,graph)
        newDictB[node] = gain
    #print "Dict A :", newDictA
    #print "Dict B :", newDictB
    return newDictA, newDictB
    
def calculateGainAB(gainA,gainB,epsilon):
    return gainA + gainB - 2 * epsilon

def calculateGainNodesAB(nodeA,nodeB,PA,PB,graph):
    gainA = nodeGain(nodeA,PA,graph)
    gainB = nodeGain(nodeB,PB,graph)
    return gainA + gainB - 2 * calculateWeight(nodeA,nodeB,graph)
    
def sumGains(G1,G2):
    res = 0
    for g1 in G1:
        res += G1[g1]
    for g2 in G2:
        res += G2[g2]
    return res
    
    
def updateNeighborsGain(s0,S1,S2,graph):
    newS1 = list(S1)
    newS2 = list(S2)
    if s0 in newS1:
        newS1.remove(s0)
        newS2.append(s0)
    else :
        newS2.remove(s0)
        newS1.append(s0)
    # newGi : gains si on déplace s0
    newG1, newG2 = associateGain(newS1,newS2,graph)
    #return newG1, newG2
    return sumGains(newG1,newG2)


# Fonction qui calcule le coût de la coupe 
# entre toutes les partitions pk dans graph
def calculateCutPk(pk,graph):
    result = 0
    for p1 in range(len(pk)):
        for p2 in range(p1+1, len(pk)):
            result = result + calculateCut(p1,p2,graph)
    return result 