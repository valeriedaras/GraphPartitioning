# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 15:44:09 2015

@author: Valérie Daras, Julie Rivière
"""
import sys 
import operator
import objectivefunctions as objf

# a supprimer : pour les tests 
import script as s

# calculer la liste des tailles des sous partitions 
# se construit par appels récursifs
def calculateSizeListSubGraph(k, i, niList, graph):
    n = graph.number_of_nodes()
    #print "number of nodes in graph : ", n
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

def removeMarkingNodes(neighborsHeap, markingList):
    newList = []
                
    for i in range(len(neighborsHeap)):
        a = neighborsHeap[i][0]
        b = neighborsHeap[i][1]
        if a not in markingList:
            newList.append((a,b))
    return newList
    
   
def setPotentialNodesList(graph,node, markingList, potentialNodesList):
    # neighborsDict est un dictionnaire contenant les voisins de node
    # ex : {17: {'weight': 4}, 10: {'weight': 7}, 11: {'weight': 3}}
    neighborsDict = graph[node]
    # dans sortedNDict, le plus petit poids est en premier
    # ex : [(11, {'weight': 3}), (17, {'weight': 4}), (10, {'weight': 7})]
    sortedNDict = sorted(neighborsDict.items(), key=operator.itemgetter(1))
    # neighborsHeap : ajout des nouveaux voisins à l'ancienne potentialNodeList
    neighborsHeap = sortedNDict + potentialNodesList
    neighborsHeap.sort(key=operator.itemgetter(1))    
    # on enleve les sommets qui ont déjà été marqués
    neighborsHeap = removeMarkingNodes(neighborsHeap, markingList)
    return neighborsHeap
    
       
 # parametres : k le nombre de partitions, graphe    
def glouton(k, graph):
    # initialisation
    initGraph = graph.copy()
    niList = []
    markingList = [] 
    potentialNodesList = []
    partitionList = []
    # initialisation du sommet de départ
    s0 = nodeWithLessNeighbor(graph, markingList)
    markingList.append(s0)
    print "sommet de depart :", s0
    potentialNodesList = setPotentialNodesList(graph,s0, markingList, potentialNodesList)
    print "potentialNodesList : ", potentialNodesList
    # initialisation de i : numéro de partition courante
    i = 1
    while i < k:
        # Calcul de ni : nombre de sommets pour la prochaine partition
        niList = calculateSizeListSubGraph(k, i, niList, initGraph)
        ni = niList[i-1]
        #print ni
        # j : nombre de sommets actuellement dans la partition courante
        j=1 	# on compte le sommet de départ
        while potentialNodesList != [] and j < ni:
            m = potentialNodesList[-1][0]
            markingList.append(m)
            potentialNodesList = setPotentialNodesList(graph,m, markingList, potentialNodesList)
            j = j+1
        # Affectation de la partition créée à la liste de partitions
        partitionList.append(markingList)
        # Réinitialisation des structures
        # Restructuration du graphe : suppression des sommets marqués
        graph.remove_nodes_from(markingList)
        markingList = [] 
        potentialNodesList = []
        i = i+1
        # Initialisation de la prochaine partition
        if i != k :
            s0 = nodeWithLessNeighbor(graph, markingList)
            markingList.append(s0)
            potentialNodesList = setPotentialNodesList(graph,s0, markingList, potentialNodesList)
    # partitionList ← sommets restants 
    partitionList.append(graph.nodes())
    graph = initGraph
    # probleme : si on ne return pas le graphe, ici il est bien égal
    # à tout le graphe mais sans le return il vaut une partition...
    return partitionList, graph
    
    
     # parametres : k le nombre de partitions, graphe    
def gloutonWithCut(k, graph):
    # initialisation
    initGraph = graph.copy()
    niList = []
    markingList = [] 
    potentialNodesList = []
    partitionList = []
    # initialisation du sommet de départ
    s0 = nodeWithLessNeighbor(graph, markingList)
    markingList.append(s0)
    print "sommet de depart :", s0
    potentialNodesList = setPotentialNodesList(graph,s0, markingList, potentialNodesList)
    # initialisation de i : numéro de partition courante
    i = 1
    while i < k:
        # Calcul de ni : nombre de sommets pour la prochaine partition
        niList = calculateSizeListSubGraph(k, i, niList, initGraph)
        ni = niList[i-1]
        #print ni
        # j : nombre de sommets actuellement dans la partition courante
        j=1 	# on compte le sommet de départ
        while potentialNodesList != [] and j < ni:
            minCut = sys.maxint
            for node in potentialNodesList:
                testList = list(markingList)
                testList.append(node[0])
                remainingNodes = [x for x in graph.nodes() if x not in testList]
                if objf.calculateCut(testList,remainingNodes,graph) < minCut:
                    minCut = objf.calculateCut(testList,remainingNodes,graph)
                    minNode = node[0]
            print "prochain noeud ajouté dans la partition :", minNode
            markingList.append(minNode)
            potentialNodesList = setPotentialNodesList(graph,minNode, markingList, potentialNodesList)
            j = j+1
        # Affectation de la partition créée à la liste de partitions
        partitionList.append(markingList)
        # Réinitialisation des structures
        # Restructuration du graphe : suppression des sommets marqués
        graph.remove_nodes_from(markingList)
        markingList = [] 
        potentialNodesList = []
        i = i+1
        # Initialisation de la prochaine partition
        if i != k :
            s0 = nodeWithLessNeighbor(graph, markingList)
            markingList.append(s0)
            potentialNodesList = setPotentialNodesList(graph,s0, markingList, potentialNodesList)
    # partitionList ← sommets restants 
    partitionList.append(graph.nodes())
    graph = initGraph
    # probleme : si on ne return pas le graphe, ici il est bien égal
    # à tout le graphe mais sans le return il vaut une partition...
    return partitionList, graph

        
def main():
    copyFilename = "unitEx.graph"
    graph = s.createGraph(copyFilename)
    pList, graph = gloutonWithCut(2,graph)
    print pList
    print objf.calculateCut(pList[0],pList[1],graph)

def testremoveMarkingNodes():
    theList = [(1, {'weight': 1}), (2, {'weight': 1}), (1, {'weight': 8}),(1, {'weight': 8})]
    markingList = [1]
    theList = removeMarkingNodes(theList, markingList)
    print theList
    
if __name__ == '__main__':
        main()