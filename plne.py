# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 08:21:03 2015

@author: valeriedaras
"""

''' Notations :
Graphe G=(V,E)
Identification d'une partition :    variable xi par sommet i
                                    xi = 1 si xi est représentant d'une partition
                                    xi = 0 sinon
                                    
Identification de deux sommets i et j :
                                    xij = 1 si i et j dans la même partition
                                    xij = 0 sinon
                                    
Poids entre deux sommets i et j : cij
                                    
Identification d'arêtes entre deux sommets i et j :
                ensemble Ec = {(i,j) tel que (i,j) appartenant à E et xij = 0, i!=j}
                variable Aij = 1 si xij = 0 et (i,j) appartient à E
                         Aij = 0 sinon
                         
                         si l'arrete n'existe pas => Aij initialisé à 0
                         
Fonction objectif : 
                min (sum sur i de 1 à n-1, sum sur j de i+1 à n, (cij x Aij), i<j)
                
                
Contraintes : 
1. Unicité d'un représentant dans une partition:
    Pour un sommet i, sum sur j de 1 à n, j!=i, (xi x xj x Aij = 0)
2. Nombre de parties : k = sum sur i de 1 à n, (xi)
3. Inégalité triangulaire : xij + xik -1 <= xjk 
4. Choix d'un représentant : pour tout les sommets i tels que xi=1
                            sum sur j de 1 à i-1 (xi x xij) = 0
                
'''
import sys
from gurobipy import *
import script as s
import objectivefunctions as objf

def weightMatrix(graph):
    cij = [[0 for x in range (graph.number_of_nodes())] for x in range (graph.number_of_nodes())]  
    for i in range (graph.number_of_nodes()):
        for j in range (graph.number_of_nodes()):
            cij[i][j] = objf.calculateWeight(i+1,j+1,graph)
    return cij

def defineObjf(cij, graph):
    n = graph.number_of_nodes()
    
    # Variable Aij
    global A 
    A = {}
    
    # Variable Xi
    global X
    X = {}
    
    #Y : Variable Xij
    global Y
    Y = {}
    
    # Variable model Gurobi
    global model 
    model = Model('partitioning')
    
    for i in range(n):
        X[i] = model.addVar(vtype=GRB.BINARY, name="X"+str(i), obj=0)
        if i < n:
            for j in range(i+1):
                A[i,j] = model.addVar(vtype=GRB.BINARY, name="A"+str(i)+str(j), obj=cij[i][j])
                A[j,i] = A[i,j]
                Y[i,j] = model.addVar(vtype=GRB.BINARY, name="Y"+str(i)+str(j), obj=0)
                Y[j,i] = Y[i,j]
    model.modelSense = GRB.MINIMIZE
    #model.modelSense = GRB.MAXIMIZE
    model.update()

'''
Contraintes : 
1. Unicité d'un représentant dans une partition:
    Pour un sommet i, sum sur j de 1 à n, j!=i, (xi x xj x Aij = 0)
2. Nombre de parties : k = sum sur i de 1 à n, (xi)
3. Inégalité triangulaire : xij + xik -1 <= xjk 
4. Choix d'un représentant : pour tout les sommets i tels que xi=1
                            sum sur j de 1 à i-1 (xi x xij) = 0'''

def defineConstraints(graph, k):
    n = graph.number_of_nodes()
    
    # Contrainte 1
    for i in range(n):
        for j in range (i-1):
            L1 = LinExpr([1,1], [X[i], Y[i,j]])
            model.addConstr(L1, "<=", 1)
    
    # Contrainte 2
    model.addConstr(quicksum(X[i] for i in range (n)) == k)
    
    # Contrainte 3
    for i in range(n):
        for j in range (i, n):
            for k in range (j, n):
                L3 = LinExpr([1,1], [Y[i,j], Y[i,k]])
                model.addConstr(L3, "<=", Y[j,k] + 1)

    # Contrainte 4
    for i in range(n):
        model.addConstr(X[i] + quicksum(Y[i,j] for j in range (i-1)), ">=", 1)

    # Update      
    model.update()

def plne(graph, k):
    cij = weightMatrix(graph)
    defineObjf(cij, graph)
    defineConstraints(graph,k)
    model.optimize()
    print "X[i]:", X
    print "Y[i,j]:", Y[1,3]
    for i in range(graph.number_of_nodes()):
        if Y[2,i] == 1:
            print i
        if Y[i,2] == 1:
            print i 
    s = model.status
    if s == GRB.Status.UNBOUNDED:
        print "Model cannot be solved because it is unbounded"
        #exit(0)
    if s == GRB.Status.OPTIMAL:
        print "The optimal objective is %g" % model.objVal
        #exit(0)
    if s == GRB.Status.INF_OR_UNBD and status != GRB.Status.INFEASIBLE:
        print "Optimization was stopped with status %d" % s
        #exit(0) 

def main():
    #copyFilename = "/Users/User/Documents/GitHub/GraphPartitioning/unitEx.graph"
    copyFilename = "/Users/valeriedaras/Documents/INSA/5IL/DataMining/workspace/GraphPartitioning/unitEx.graph"
    graph = s.createGraph(copyFilename)
    plne(graph, 2)


if __name__ == '__main__':
        main()