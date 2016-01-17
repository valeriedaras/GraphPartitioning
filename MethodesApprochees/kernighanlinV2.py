# -*- coding: utf-8 -*-
"""
Created on Sat Dec 05 14:55:57 2015

@author: Daras Valérie, Rivière Julie
"""
import sys
import script as s
import glouton as g 
import objectivefunctions as objf
import networkx as nx
import time
       

   
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


def kl(graph,verbose):
    print "Starting KL version 2.."
    startTime = time.time()
    ## Initialisation ##
    # Liste de partitions
    partitionsList = []
    # Initialisation des listes de sommets à étudier 
    # (une par partition)
    remainingNodesS1 = []
    remainingNodesS2 = []    
    
    ## Déroulement de l'algo ##    
    # bipartition
    partitionsList, graph = g.gloutonWithCut(2,graph,False,False)
    if verbose:
        print "Partition Init 1: ", partitionsList[0]
        print "Partition Init 2: ", partitionsList[1]

    deltaTime = -time.time()
    
    ratio = 20    
    
    # Mise a jour des listes des sommets à étudier
    remainingNodesS1 = list(partitionsList[0])[len(partitionsList[0])*(100-ratio)/100:]
    remainingNodesS2 = list(partitionsList[1])[len(partitionsList[1])*(100-ratio)/100:]

    # calcul du gain global initial
    globalMin = objf.calculateCut(remainingNodesS1,remainingNodesS2,graph)
    #  Initialisation du gain fictif
    GainGlobalFictif = globalMin
    if verbose:
        print "Global Min Initial:", globalMin
        print ""
        print "Recherche de sommets uniques à changer..."   
   
    nodesList = nx.nodes(graph)
    iterations = 100
    while iterations > 0 :
        improvement = False
        localMin = sys.maxint
        
        for node in nodesList:
            gain = calculateFictifGainUnique(node, partitionsList[0], partitionsList[1], graph)
            
            # recherche du meilleur gain local            
            if gain < localMin  and gain > 0 :
                improvement = True
                localMin = gain
                s = node
                GainGlobalFictif = globalMin - gain
                if verbose:
                    print "Nouveau gain local:", localMin, "Node: ", node
                    print "Gain Global Fictif =", GainGlobalFictif

        if improvement :
            nodesList.remove(s)        
        if (GainGlobalFictif < globalMin):
            globalMin = GainGlobalFictif
            if verbose:
                print "Nouveau gain global:", globalMin, "Node:", s
                print "Le noeud",s,"a été échangé de partition"
            partitionsList = switchNodesUnique(partitionsList,s)
        
        iterations = iterations - 1
 
    stopTime = time.time()
    deltaTime += time.time()
    print "Temps d'exécution total:", stopTime-startTime
    print "Temps d'exécution KL:", deltaTime
    if verbose:
        print "Partition Finale 1:", partitionsList[0]
        print "Partition Finale 2:", partitionsList[1]
    print "Global cut:", objf.calculateCut(partitionsList[0], partitionsList[1], graph)
    
    
def main():
    copyFilename = "../graphs/testGraph.graph"
    #s.copyFileUnit("../graphs/data.graph",copyFilename)
    s.copyFileUnit("../graphs/add20.graph",copyFilename)
    #s.copyFileUnit("../graphs/3elt.graph",copyFilename)
    graph = s.createGraph(copyFilename)
    
    #graph = s.createGraph("../graphs/unitEx.graph")
    kl(graph,False)

if __name__ == '__main__':
        main()