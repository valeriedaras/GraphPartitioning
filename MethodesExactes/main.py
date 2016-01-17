# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 08:21:03 2015

@author: Valerie Daras et Julie Riviere
"""

from gurobipy import * 
import script as s
import plneV1 as PLNEV1
import plneV2 as PLNEV2
import plneV3 as PLNEV3


def main():
    # Choose a graph to test
    
    graph = getTestGraph()
    #graph = getGraph3elt()
    #graph = getGraphAdd20()
    #graph = getGraphData()
    
            ###################################################
    
    # Choose a algorithm to test
    
    plneV1(2,graph)
    #plneV2(2,graph)
    #plneV3_MaxNodesInPartiton(2,graph,12)
    #plneV3_MaxDifferenceBetweenPartitons(2,graph,5)
    

###############################################################################
#####################              ALGORITHMS               ###################
###############################################################################
    
    
def plneV1(k,graph) :
    PLNEV1.plne(graph,k)    

def plneV2(k,graph) :
    PLNEV2.plne(graph,k)
    
# Val représente le nombre max de sommets dans une partition
def plneV3_MaxNodesInPartiton(k,graph,val) :
    PLNEV3.plne(graph, k, 0, val)

# Val représente la différence max de nombre de sommets entre les partitions
def plneV3_MaxDifferenceBetweenPartitons(k,graph,val) :
    PLNEV3.plne(graph, k, 1, val)


###############################################################################
#####################                GRAPHS                 ###################
###############################################################################


def getTestGraph():
    return s.createGraph("../graphs/unitEx.graph")

def getGraph3elt():
    copyFilename = "../graphs/3eltUnit.graph"
    s.copyFileUnit("../graphs/3elt.graph",copyFilename)
    return s.createGraph(copyFilename)
    
def getGraphAdd20():
    copyFilename = "../graphs/add20Unit.graph"
    s.copyFileUnit("../graphs/add20.graph",copyFilename)
    return s.createGraph(copyFilename)

def getGraphData():
    copyFilename = "../graphs/dataUnit.graph"
    s.copyFileUnit("../graphs/data.graph",copyFilename)
    return s.createGraph(copyFilename)

 

if __name__ == '__main__':
        main()
