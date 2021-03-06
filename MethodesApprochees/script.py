# -*- coding: utf-8 -*-
"""
@author: Valérie Daras, Julie Rivière
"""

import os 
import sys
from random import randint
import networkx as nx
import matplotlib.pyplot as plt

import objectivefunctions as objf



# copyFile prend un fichier source (.graph) et le modifie en ajoutant
# un poids random pour chaque voisin 
# notation : poids1 voisin1 poids2 voisin2...
# creation de ce fichier pour pouvoir rejouer les tests avec les memes données
def copyFile(source, destination):
    src = open(source, 'r')
    dst = open(destination, 'w')
    firstLine = 0
    newline = ""
    for line in src:
        if firstLine == 0:
            firstLine = firstLine+1 
            newline = line 
        else:
            i = 0 
            newline = ""
            while i < len(line):
                if line[i] == " ":
                    rand = randint(1,10)
                    newline = newline + line[i] + str(rand) + " "
                else:
                    newline = newline + line[i]
                i += 1
        dst.write("%s" % newline) 
    src.close()
    dst.close()

# même comportement que copyFile mais poids = 1    
def copyFileUnit(source, destination):
    src = open(source, 'r')
    dst = open(destination, 'w')
    firstLine = 0
    newline = ""
    for line in src:
        if firstLine == 0:
            firstLine = firstLine+1 
            newline = line 
        else:
            i = 0 
            newline = ""
            while i < len(line):
                if line[i] == " ":
                    rand = 1
                    newline = newline + line[i] + str(rand) + " "
                else:
                    newline = newline + line[i]
                i += 1
        dst.write("%s" % newline) 
    src.close()
    dst.close()
    

### Graph functions ###
 
# Cree un graphe a partir du graphe décrit dans le fichier source   
def createGraph(source):
    graph=nx.Graph()
    src = open(source, 'r')
    numLine = 0
    for line in src:
        if numLine != 0:
            tab = str.rsplit(line)
            i = 0
            j = 1
            while j < len(tab):
                # la structure de graphe est redondante dans le .graph
                # pour avoir toujours le meme poids entre 2 sommets,
                # on conserve seulement le 1er poids rencontré
                if not graph.has_edge(numLine,int(tab[j])): 
                    graph.add_edge(numLine,int(tab[j]),weight=int(tab[i]))
                i = i + 2 
                j = j + 2
        numLine = numLine+1 
                
    src.close()
    return graph

# Dessine le graphe     
def drawGraph(graph):
    nx.draw(graph)
    plt.show()

# Recuperer le nombre de noeuds d'un graphe    
def getNumberOfNodes(graph):
    return graph.number_of_nodes()
    
### MAIN ###

def main():
	copyFile("data.graph","dataUnit.graph")	
	createGraph("dataUnit.graph")


if __name__ == '__main__':
        main()