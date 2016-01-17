# -*- coding: utf-8 -*-
"""
Created on Sat Dec 05 14:55:57 2015

@author: Daras Valérie, Rivière Julie
"""

import script as s
import glouton as g 
import kernighanlinV1 as KLV1
import kernighanlinV2 as KLV2

import recuitSimule as rs

def main():
    verbose = False
    # Choose a graph to test
    
    graph = getTestGraph()
    #graph = getGraph3elt()
    #graph = getGraphAdd20()
    #graph = getGraphData()
    
            ###################################################
    
    # Choose a algorithm to test
    
    #gloutonV1(2,graph,verbose)
    #gloutonV2(2,graph,verbose)
    #kernighanLinV1(graph,verbose)
    #kernighanLinV2(graph,verbose)
    recuitSimule(graph,10000, 1000, 10, verbose)
    
    

###############################################################################
#####################              ALGORITHMS               ###################
###############################################################################
    
    
def gloutonV1(k,graph,verbose) :
    g.glouton(k,graph,verbose,True)    

def gloutonV2(k,graph,verbose) :
    g.gloutonWithCut(k,graph,verbose,True)
    
def kernighanLinV1(graph,verbose) :
    KLV1.kl(graph,verbose)

def kernighanLinV2(graph,verbose) :
    KLV2.kl(graph,verbose)

def recuitSimule(graph,iterations, tempI, remonteeMax, verbose) :
    rs.recuitSimule(graph,iterations,tempI, remonteeMax, verbose)



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