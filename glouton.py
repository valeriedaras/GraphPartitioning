# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 15:44:09 2015

@author: Valérie Daras, Julie Rivière
"""
import sys 

# calculer la liste des tailles des sous partitions 
# se construit par appels récursifs
def calculateSizeListSubGraph(k, i, niList, graph):
    n = graph.number_of_nodes()
    s = 0
    for j in niList:    
        s = s + j
    ni = (n - s) / (k-(i-1))
    niList.append(ni)
    return niList
    
def nodeWithLessNeighbor(graph,markingList):
    # on parcourt tous les sommets non marqués et on renvoit
    # celui qui a le moins de voisins
    neighborsMin = sys.maxint
    for node in graph.nodes():
        if node in markingList:
            if graph.degree(node) < neighborsMin:
                neighborsMin = graph.degree(node)
                nodeMin = node
                if neighborsMin == 1:
                    break
    return nodeMin
        
    
def frontiere(k, graph):
    i = 1
    niList = []
    markingList = [] 
    while i < k:
        if i < k:
            niList = calculateSizeListSubGraph(k, i, niList, graph)
            ni = niList[i-1]
            # choix du sommet non marqué Vd 
            #choiceVd(currentFront, )
        
        