# -*- coding: utf-8 -*-
"""
Created on Sat Dec 05 14:55:57 2015

@author: Daras Valérie, Rivière Julie
"""
import sys
import networkx as nx
import script as s
import glouton as g 
import objectivefunctions as objf


def nodeGain(node,partitionA,inA,graph):
    nbNeighborsInA = 0
    nbNeighborsInB = 0
    for neighbors in nx.all_neighbors(graph,node):
        if neighbors in partitionA:
            nbNeighborsInA += 1 
        else:
            nbNeighborsInB +=1
    #print node
    #print "voisins dans A:", nbNeighborsInA, "voisins dans B:", nbNeighborsInB
    if inA == 1:
        return nbNeighborsInB - nbNeighborsInA
    elif inA == 0:
        return nbNeighborsInA - nbNeighborsInB
        
def nodeGain2(node,partition,graph):
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
        #gain = nodeGain(node,A,1,graph)
        gain = nodeGain2(node,A,graph)
        newDictA[node] = gain
    for node in B:
        #gain = nodeGain(node,A,0,graph)
        gain = nodeGain2(node,B,graph)
        #gain = nodeGain(node,B,1,graph)
        newDictB[node] = gain
    return newDictA, newDictB
    
def calculateGainAB(gainA,gainB,epsilon):
    return gainA + gainB - 2 * epsilon
    
def sumGains(G1,G2):
    res = 0
    for g1 in G1:
        res += G1[g1]
    for g2 in G2:
        res += G2[g2]
    return res
    
def switchNodes(partitionsList,f1,f2):
    partitionsList[0].remove(f1)
    partitionsList[0].append(f2)
    partitionsList[1].remove(f2)
    partitionsList[1].append(f1)
    return partitionsList
    
def updateNeighborsGain(s1,s2,S1,S2,G1,G2,graph):
    newS1 = list(S1)
    newS1.remove(s1)
    newS1.append(s2)
    newS2 = list(S2)
    newS2.remove(s2)
    newS2.append(s1)
    # newGi : gains si on permute s1 et s2
    newG1, newG2 = associateGain(newS1,newS2,graph)
    '''for neighborsS1 in nx.all_neighbors(graph,s1):
        if neighborsS1 == s2:
            G2[neighborsS1]=newG1[neighborsS1]
        elif neighborsS1 in G1:
            G1[neighborsS1]=newG1[neighborsS1]
        elif neighborsS1 in G2:
            G2[neighborsS1]=newG2[neighborsS1]
    for neighborsS2 in nx.all_neighbors(graph,s2):
        if neighborsS2 == s1:
            G1[neighborsS2]=newG2[neighborsS2]
        elif neighborsS2 in G1:
            G1[neighborsS2]=newG1[neighborsS2]
        elif neighborsS2 in G2:
            G2[neighborsS2]=newG2[neighborsS2]'''
    return newG1, newG2
    #return G1,G2
            
def setRemainingNodes(partition,exchangedNodes):
    newPartition = list(partition)
    for node in exchangedNodes:
        if node in newPartition:
            newPartition.remove(node)
    return newPartition


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
    
    #  Initialisation des listes de gains reels (une par partition)
    G1 = []
    G2 = []
    
    #  Initialisation des listes de gains fictifs (une par partition)
    G1Fictif = []
    G2Fictif = []
    
    
    ## Déroulement de l'algo ##
    
    # bipartition
    partitionsList, graph = g.glouton(2,graph)
    # Mise a jour des listes des sommets à étudier
    remainingNodesS1 = list(partitionsList[0])
    remainingNodesS2 = list(partitionsList[1])
    print "Partition Init 1: ", remainingNodesS1
    print "Partition Init 2: ", remainingNodesS2
    
    optimum = False
    
    # boucle principale

    # calcul du gain global initial
    #globalMax = sumGains(G1,G2)
    globalMax = - sys.maxint - 1


    while remainingNodesS1 != [] and remainingNodesS2 != [] and not optimum:
        improvement = False
        S1 = list(partitionsList[0])
        S2 = list(partitionsList[1])
        #print "S1:",S1
        #print "S2:",S2 
        # calcul des gains 
        G1, G2 = associateGain(S1,S2,graph)
        #print G1,G2
    
        localMax = - sys.maxint - 1
        #print "Max Global: ", globalMax
        #print ""
        #print "********** BOUCLE SUR PARTITION 1 **********"
        
        
        # On inverse l'ordre de S1 car les derniers sommets ajoutés
        # sont les plus susceptibles à ressortir en premier
        #print "RemainingNodesS1", remainingNodesS1
        for nodeA in reversed(remainingNodesS1):
            # s1 : sommet candidat de S1 pour un échange
            s1 = nodeA
            gainA = G1[nodeA]
            #print "A:",nodeA
            #print "gainA" , gainA
            #print "RemainingNodesS2", remainingNodesS2
            #print "********** BOUCLE SUR PARTITION 2 **********"
            for nodeB in remainingNodesS2:
                # on cherche le meilleur candidat pour un échange avec s1

                #print "B:",nodeB
                gainB = G2[nodeB]
                #print "gainB" , gainB
                
                # Calcul du gain lié à l'échange de a et b : G(a,b)
                if objf.calculateWeight(s1,nodeB,graph) == 0:
                    epsilon = 0
                else:
                    epsilon = 1
                gainAB = calculateGainAB(gainA,gainB,epsilon)
                if gainAB > localMax:
                    localMax = gainAB
                    # s2 : sommet candidat de S2 pour un échange avec s1
                    s2 = nodeB
                    print "Nouveau gain local:", localMax, "Nodes: ", s1, s2

                    #  Mise a jour des gains fictifs gv de tous les voisins v de s1 et de s2 
                    #(les deux sommets associés au meilleur gain)
                    # comme si on échangeait s1 et s2
                    #print G1,G2,sumGains(G1,G2)
                    G1Fictif,G2Fictif = updateNeighborsGain(s1,s2,S1,S2,G1,G2,graph)
                    #print G1Fictif,G2Fictif   
                    #print sumGains(G1Fictif,G2Fictif)
                
                    
            # Mise a jour du gain global
            if (sumGains(G1Fictif,G2Fictif) > globalMax):
                improvement = True ;
                globalMax = sumGains(G1Fictif,G2Fictif)
                f1 = s1
                f2 = s2
                print "Nouveau gain global:", globalMax, "Nodes:", f1, f2
                exchangedNodes.append(f1)
                exchangedNodes.append(f2)
                
                # P ← échanger les sommets f1 et f2
                print "Les noeuds",f1,"et",f2, "ont été échangés"
                partitionsList = switchNodes(partitionsList,f1,f2)
                print "Partition 1:", partitionsList[0]
                print "Partition 2:", partitionsList[1]
                
                # Mise a jour des listes des sommets à étudier
                remainingNodesS1 = setRemainingNodes(partitionsList[0],exchangedNodes)
                remainingNodesS2 = setRemainingNodes(partitionsList[1],exchangedNodes)

  
        if (improvement == False):
            print "Optimum trouve!"
            optimum = True
 
    print "Partition Finale 1: ", partitionsList[0]
    print "Partition Finale 2: ", partitionsList[1]

    
def main():
    #copyFilename = "/Users/User/Documents/GitHub/GraphPartitioning/unitEx.graph"
    copyFilename = "/Users/valeriedaras/Documents/INSA/5IL/DataMining/workspace/GraphPartitioning/unitEx.graph"
    graph = s.createGraph(copyFilename)
    kl(graph)

if __name__ == '__main__':
        main()