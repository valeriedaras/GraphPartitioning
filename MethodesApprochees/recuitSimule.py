# -*- coding: utf-8 -*-
"""
Created on Sat Dec 05 14:55:57 2015

@author: Daras Valérie, Rivière Julie
"""

import script as s
import glouton as g 
import objectivefunctions as objf
import time
from random import random
from random import randint
from math import exp
import networkx as nx
       

   
def switchNodes(partitionsList,f1,f2):
    partitionsList[0].remove(f1)
    partitionsList[0].append(f2)
    partitionsList[1].remove(f2)
    partitionsList[1].append(f1)
    return partitionsList

def switchNodesUnique(partitionsList,f):
    if f in partitionsList[0]:
        partitionsList[0].remove(f)
        partitionsList[1].append(f)
    else :
        partitionsList[0].append(f)
        partitionsList[1].remove(f)
    return partitionsList    
        
def setRemainingNodes(partition,exchangedNodes):
    newPartition = list(partition)
    for node in exchangedNodes:
        if node in newPartition:
            newPartition.remove(node)
    return newPartition

def calculateFictifGain(s1,s2,P1,P2,graph):
    return objf.calculateGainNodesAB(s1,s2,P1,P2,graph)


def calculateFictifGainUnique(s,P1,P2,graph):
    # déplacement du sommet s de P1 vers P2
    if s in P1:
        newG = objf.nodeGain(s, P1, graph)
    else :
        newG = objf.nodeGain(s, P2, graph)
    return newG    

def selectNode(P):
    rand = randint(0,len(P)-1)
    return P[rand]
    
def neighbors(P,graph):
    Lin=[]
    Lout=[]
    for node in P:
        N = nx.neighbors(graph,node)
        for neighbor in N:
            # Voisin exterieur de P
            if neighbor not in P:
                # Node dans P a un voisin exterieur a P
                if node not in Lin:
                    Lin.append(node)
                if neighbor not in Lout:
                    Lout.append(neighbor)
    return Lin,Lout

def hasOutsideNeighbor(node, P, graph):
    N = nx.neighbors(graph,node)
    if node in P :
        while N!=[] :
            if N[0] not in P :
                return True
            N.remove(N[0])
    else :
        while N!=[] :
            if N[0] in P :
                return True
            N.remove(N[0])
    return False

def updateNeighbors(s2,s1,L1,L2,P1,P2,G):    
    L1.append(s1)
    L2.remove(s1)
    L2.append(s2)
    L1.remove(s2)
    
    
    if not hasOutsideNeighbor(s1,P1,G) :
        L1.remove(s1)

    if not hasOutsideNeighbor(s2,P2,G) :
        L2.remove(s2)
    
    N1 = nx.neighbors(G,s1)
    N2 = nx.neighbors(G,s2)

    for node1 in N1 :
        if node1 in P1:
            #print "Nodes",node1,"and",s1,"in the same partition"
            if hasOutsideNeighbor(node1,P1,G) :
                #print "Node", node1, "has a neighbor outside from",P1
                if node1 not in L1 :
                    L1.append(node1)
                    #print "L1 : ajout de", node1
            else :
                if node1 in L1 :
                    L1.remove(node1)
                #print "L1 : suppression de", node1
        else:
            #print "Nodes",node1,"and",s1,"not in the same partition"
            if not hasOutsideNeighbor(node1,P1,G) and node1 in L1:
                L1.remove(node1)
                #print "L1 : suppression de", node1
                
    for node2 in N2 : 
        if node2 in P2 :
            #print "Nodes",node2,"and",s2,"in the same partition"
            if hasOutsideNeighbor(node2,P2,G) :
                #print "Node", node2, "has a neighbor outside from",P2
                if node2 not in L2 :
                    L2.append(node2)
                    #print "L2 : ajout de", node2
            else :
                if node2 in L2 :
                    L2.remove(node2)
                #print "L2 : suppression de", node2
        else:
            #print "Nodes",node2,"and",s2,"not in the same partition"
            if not hasOutsideNeighbor(node2,P2,G) and node2 in L2:
                L2.remove(node2)
                #print "L2 : suppression de", node2
    #print "Limite de P1", L1
    #print "Limite de P2", L2

def addRandomNode(List,Partition):
    P = list(Partition)
    for node in List :
        if node in P :
            P.remove(node)
    if len(P) > 1 :
        nodeRandom = selectNode(P)
        List.append(nodeRandom)
    return List
    
# Iterations : nombre d'itérations de l'algorithme
# tempI : Temperature initiale
# remonteeMax : Nombre de remontée consécutives autorisées
def recuitSimule(graph, iterations, tempI, remonteeMax,verbose):
    print "Starting Recuit Simule with", iterations, "iterations,", tempI, "as initial temperature and", remonteeMax, "as max upgoing movements"

    deltaTime0 = -time.time()    
    
    ## Initialisation ##
    # Liste de partitions
    partitionsList = [] 
    
    # Appel du Glouton
    partitionsList, graph = g.gloutonWithCut(2,graph,False,False)
    P1Final = list(partitionsList[0])
    P2Final = list(partitionsList[1])
    if verbose :
        print "Partition P1 init :", P1Final
        print "Partition P2 init :", P2Final

    print "Number of nodes in graph:", nx.number_of_nodes(graph)
    # calcul du gain global initial
    globalMin = objf.calculateCut(partitionsList[0],partitionsList[1],graph)
    
    #  Initialisation du gain fictif
    GainGlobalFictif = globalMin
    print "Global Min Initial:", globalMin

    # Temps de départ
    deltaTime = -time.time()
    
    # Nombre d'iteration de l'algorithme
    iterationsC = 0

    # Nombre courant de remontée de temperature consecutives
    remontee = 0
    
    # Temperature courante
    tempC = tempI
    
    list_pourcentage = [0,10,20,30,40,50,60,70,80,90]
    
    nodesOnLimit,neighborsList = neighbors(partitionsList[0],graph)
    
    # Boucle principale
    while iterationsC < iterations :
        pourcentage = (iterationsC*100)/iterations
        if pourcentage in list_pourcentage:
            del(list_pourcentage[0])
            print '------------------',pourcentage, "% effectués", '------------------'            
            
        change = False

        # Candidat aleatoire de la partition P1
        nodeA = selectNode(nodesOnLimit)
        # Candidat aleatoire de la partition P2
        nodeB = selectNode(neighborsList)

        # Calcul du gain lié à l'échange de nodeA et nodeB : G(nodeA,nodeB)
        gainAB = calculateFictifGain(nodeA, nodeB, partitionsList[0], partitionsList[1], graph)
        
        if verbose:
            print "Gain entre",nodeA,"et",nodeB,"=",gainAB
        # Amelioration solution locale
        if gainAB >= 0 :
            change = True
            remontee = 0
            if verbose :
                print "Descente en temperature avec les noeuds", nodeA, "et", nodeB                
                
        else:
            # Acceptation de la solution dégradante 
            if random() < exp(gainAB/tempC) and remontee < remonteeMax :
                change = True
                remontee +=1
                if verbose :
                    print "Remontee en temperature avec les noeuds", nodeA, "et", nodeB                

        # Changement a effectuer                                        
        if change :
            # On echange les sommets nodeA et nodeB
            partitionsList = switchNodes(partitionsList,nodeA,nodeB)
            updateNeighbors(nodeA,nodeB,nodesOnLimit,neighborsList,partitionsList[0],partitionsList[1],graph)
            
            GainGlobalFictif = GainGlobalFictif - gainAB
            if verbose:
                print "Les noeuds",nodeA,"et",nodeB, "ont été échangés"
                print "Gain fictif =", GainGlobalFictif
            
            if GainGlobalFictif < globalMin and GainGlobalFictif > 0:
                globalMin = GainGlobalFictif
                print "Update globalMin =",globalMin
                P1Final = list(partitionsList[0])
                P2Final = list(partitionsList[1])
        
        # cas où la remontee de temperature n'a que fait dégrader la solution
        if remontee == remonteeMax and not change :
            print "Degradation trop élevée --> récupération des anciennes partitions"
            # récupération de la meilleure partition
            partitionsList[0] = list(P1Final)
            partitionsList[1] = list(P2Final)
            nodesOnLimit,neighborsList = neighbors(partitionsList[0],graph)
        
        addRandomNode(nodesOnLimit, partitionsList[0])
        addRandomNode(neighborsList, partitionsList[1])        
        
        iterationsC +=1
        tempC = 0.99*tempC
    

    deltaTime += time.time()
    deltaTime0 += time.time()
    if verbose:
        print "Partition Finale 1:", P1Final
        print "Partition Finale 2:", P2Final    
    print "Temps d'exécution recuit-simule:", deltaTime
    print "Temps d'exécution global:", deltaTime0
    print "Global cut:", globalMin
    
    
def main():
    copyFilename = "../graphs/testGraph.graph"
    #copyFilename = "../graphs/unitEx.graph"
    #s.copyFileUnit("../graphs/data.graph",copyFilename)
    #s.copyFileUnit("../graphs/add20.graph",copyFilename)
    s.copyFileUnit("../graphs/3elt.graph",copyFilename)
    graph = s.createGraph(copyFilename)
    recuitSimule(graph, 100000, 10000, 30,False)
    

if __name__ == '__main__':
        main()