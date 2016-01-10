# -*- coding: utf-8 -*-
"""
Created on Sat Dec 05 14:55:57 2015

@author: Daras Valérie, Rivière Julie
"""
import sys
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

def updateNeighbors(s1,s2,L1,L2):
    L1.remove(s1)
    L1.append(s2)
    L2.remove(s2)
    L2.append(s1)

    

def kl(graph):
    verbose = False
    
    ## Initialisation ##
    # Liste de partitions
    partitionsList = []  
    
    # Appel du Glouton
    partitionsList, graph = g.gloutonWithCut(2,graph)
    P1Final = list(partitionsList[0])
    P2Final = list(partitionsList[1])
    if verbose :
        print "Partition P1 init :", P1Final
        print "Partition P2 init :", P2Final

    # calcul du gain global initial
    globalMin = objf.calculateCut(partitionsList[0],partitionsList[1],graph)
    
    #  Initialisation du gain fictif
    GainGlobalFictif = globalMin
    print "Global Min Initial:", globalMin

    # Temps de départ
    deltaTime = -time.time()

    # Liste de tous les noeuds du graphe
    #nodesList = nx.nodes(graph)
    
    # Nombre d'iteration de l'algorithme
    iterations = 1000000
    iterationsC = 0
    
    # Nombre max de remontée de temperature consecutives
    remonteeMax = 1000

    # Nombre courant de remontée de temperature consecutives
    remontee = 0
    
    # Temperature initiale
    tempI = 9999
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
            updateNeighbors(nodeA,nodeB,nodesOnLimit,neighborsList)
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
            # récupération de la meilleure partition
            partitionsList[0] = list(P1Final)
            partitionsList[1] = list(P2Final)
        
        iterationsC +=1
        tempC = 0.99*tempC
    

    deltaTime += time.time()
    if verbose:
        print "Partition Finale 1:", P1Final
        print "Partition Finale 2:", P2Final    
    print "Temps d'exécution:", deltaTime
    print "Global cut:", globalMin
    
    
def main():
    copyFilename = "graphs/testGraph.graph"
    #copyFilename = "graphs/unitEx.graph"
    #s.copyFileUnit("graphs/data.graph",copyFilename)
    #s.copyFileUnit("graphs/add20.graph",copyFilename)
    s.copyFileUnit("graphs/3elt.graph",copyFilename)
    graph = s.createGraph(copyFilename)
    
    kl(graph)

if __name__ == '__main__':
        main()