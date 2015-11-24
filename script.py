# -*- coding: utf-8 -*-
import os 
import sys
from random import randint
import networkx as nx
import matplotlib.pyplot as plt

import objectivefunctions as objf

filename = "/home/jriviere/Bureau/OC/add20.graph"
copyFilename = "/home/jriviere/Bureau/OC/add200.graph"


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
    #print graph.number_of_nodes()
    #nx.draw(graph)
    #plt.show()
    

    


def main():
	copyFile(filename,copyFilename)	
	createGraph(copyFilename)


if __name__ == '__main__':
    try:
        main()
        sys.exit(0)
    except KeyboardInterrupt:
        exit(0)