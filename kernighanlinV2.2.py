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


def kl(graph):
    ## Initialisation ##

    # Sert à mémoriser les sommets échangés
    exchangedNodes = []
    # Liste de partitions
    partitionsList = []
    # Initialisation des listes de sommets à étudier 
    # (une par partition)
    remainingNodesS1 = []
    remainingNodesS2 = []    
    
    ## Déroulement de l'algo ##    
    # bipartition
    partitionsList, graph = g.gloutonWithCut(2,graph)
    print "Partition Init 1: ", partitionsList[0]
    print "Partition Init 2: ", partitionsList[1]
    
    ratio = 20
    
    # Mise a jour des listes des sommets à étudier
    remainingNodesS1 = list(partitionsList[0])[len(partitionsList[0])*(100-ratio)/100:]
    remainingNodesS2 = list(partitionsList[1])[len(partitionsList[1])*(100-ratio)/100:]
    
    
    optimumEqu = False
    # boucle principale

    # calcul du gain global initial
    globalMin = objf.calculateCut(remainingNodesS1,remainingNodesS2,graph)
    #  Initialisation du gain fictif
    GainGlobalFictif = globalMin
    print "Global Min Initial:", globalMin

    print "Remaining Init 1: ", remainingNodesS1
    print "Remaining Init 2: ", remainingNodesS2

    while remainingNodesS1 != [] and remainingNodesS2 != [] and not optimumEqu:
        improvement = False
        P1 = list(partitionsList[0])
        P2 = list(partitionsList[1])
    
        localMin = sys.maxint

        # On inverse l'ordre de P1 et de P2 car les derniers sommets ajoutés
        # sont les plus susceptibles à ressortir en premier
        for nodeA in reversed(remainingNodesS1):
            # s1 : sommet candidat de S1 pour un échange
            s1 = nodeA

            for nodeB in reversed(remainingNodesS2):
                # on cherche le meilleur candidat pour un échange avec s1
                # Calcul du gain lié à l'échange de a et b : G(a,b)
                gainAB = calculateFictifGain(s1, nodeB, P1, P2, graph)
                #print "Gain between", s1, nodeB, ":",gainAB              
                
                if gainAB < localMin  and gainAB > 0 :
                    localMin = gainAB
                    # s2 : sommet candidat de S2 pour un échange avec s1
                    s2 = nodeB
                    print "Nouveau gain local:", localMin, "Nodes: ", s1, s2
                    GainGlobalFictif = globalMin - gainAB
                    print "Gain Global Fictif =", GainGlobalFictif
                
                    
            # Mise a jour du gain global
            if (GainGlobalFictif < globalMin):
                improvement = True
                globalMin = GainGlobalFictif
                print "Nouveau gain global:", globalMin, "Nodes:", s1, s2
                exchangedNodes.append(s1)
                exchangedNodes.append(s2)
                
                # P ← échanger les sommets s1 et s2
                print "Les noeuds",s1,"et",s2, "ont été échangés"
                partitionsList = switchNodes(partitionsList,s1,s2)
                
                # Mise a jour des listes des sommets à étudier
                remainingNodesS1 = setRemainingNodes(partitionsList[0],exchangedNodes)
                remainingNodesS2 = setRemainingNodes(partitionsList[1],exchangedNodes)


        if (improvement == False):
            print "Optimum équilibré trouvé!"
            print "Global cut:", objf.calculateCut(partitionsList[0], partitionsList[1], graph)
            optimumEqu = True

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
                print "Nouveau gain local:", localMin, "Node: ", node
                s = node
                GainGlobalFictif = globalMin - gain
                print "Gain Global Fictif =", GainGlobalFictif

        if improvement :
            nodesList.remove(s)        
        if (GainGlobalFictif < globalMin):
            globalMin = GainGlobalFictif
            print "Nouveau gain global:", globalMin, "Node:", s
            print "Le noeud",s,"a été échangé de partition"
            partitionsList = switchNodesUnique(partitionsList,s)
            print "Global cut:", objf.calculateCut(partitionsList[0], partitionsList[1], graph)
            #print "Partition 1:", partitionsList[0]
            #print "Partition 2:", partitionsList[1]
        
        iterations = iterations - 1
 
    print "Partition Finale 1:", partitionsList[0]
    print "Partition Finale 2:", partitionsList[1]
    print "Global cut:", objf.calculateCut(partitionsList[0], partitionsList[1], graph)
    
    
def main():
    copyFilename = "testGraph.graph"
    #s.copyFileUnit("data.graph",copyFilename)
    #s.copyFileUnit("add20.graph",copyFilename)
    s.copyFileUnit("3elt.graph",copyFilename)
    graph = s.createGraph(copyFilename)
    
    #graph = s.createGraph("unitEx.graph")
    kl(graph)

if __name__ == '__main__':
        main()