# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 15:44:09 2015

@author: Valérie Daras, Julie Rivière
"""
import sys 
import operator

# a supprimer : pour les tests 
import script as s

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
        if node not in markingList:
            if graph.degree(node) < neighborsMin:
                neighborsMin = graph.degree(node)
                nodeMin = node
                if neighborsMin == 1:
                    break
    return nodeMin
    
def setPotentialNodesList(graph,node, markingList):
    # neighborsDict est un dictionnaire contenant les voisins de node
    # ex : {17: {'weight': 4}, 10: {'weight': 7}, 11: {'weight': 3}}
    neighborsDict = graph[node]
    # dans sortedNDict, le plus petit poids est en premier
    # ex : [(11, {'weight': 3}), (17, {'weight': 4}), (10, {'weight': 7})]
    sortedNDict = sorted(neighborsDict.items(), key=operator.itemgetter(1))
    # neighborsHeap : liste ordonnée des voisins, la 1ere valeur est le sommet
    # ayant le plus petit poids
    # ex : [11, 17, 10]
    neighborsHeap = [a for (a, b) in sortedNDict]
    # on enleve les sommets qui ont déjà été marqués
    for node in markingList:
        if node in neighborsHeap:
            neighborsHeap.remove(node)
    return neighborsHeap
    
        
 # parametres : k le nombre de partitions, graphe    
def glouton(k, graph):
    # initialisation
    niList = []
    markingList = [] 
    potentialNodesList = []
    partitionList = []
    # initialisation du sommet de départ
    s0 = nodeWithLessNeighbor(graph, markingList)
    markingList.append(s0)
    potentialNodesList = setPotentialNodesList(graph,s0, markingList)
    # initialisation de i : numéro de partition courante
    i = 1
    while i < k:
        # Calcul de ni : nombre de sommets pour la prochaine partition
        niList = calculateSizeListSubGraph(k, i, niList, graph)
        ni = niList[i-1]
        # j : nombre de sommets actuellement dans la partition courante
        j=1 	# on compte le sommet de départ
        while potentialNodesList != [] and j < ni:
            m = potentialNodesList[0]
            markingList.append(m)
            potentialNodesList = setPotentialNodesList(graph,m, markingList)
            j = j+1
        # Affectation de la partition créée à la liste de partitions
        partitionList.append(markingList)
        # Réinitialisation des structures
        # Restructuration du graphe : suppression des sommets marqués
        graph.remove_nodes_from(markingList)
        #markingList = [] 
        #potentialNodesList = []
        i = i+1
        # Initialisation de la prochaine partition
        if i != k :
            s0 = nodeWithLessNeighbor(graph, markingList)
            markingList.append(s0)
            potentialNodesList = setPotentialNodesList(graph,s0, markingList)
    # partitionList ← sommets restants 
    partitionList.append(graph.nodes())
    print partitionList


            

    
        
def main():
    copyFilename = "/Users/User/Documents/GitHub/GraphPartitioning/unitEx.graph"
    graph = s.createGraph(copyFilename)
    glouton(2,graph)


if __name__ == '__main__':
        main()