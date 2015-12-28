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
    
    #X : Variable Xi
    global X
    X = {}
    
    #Y : Variable Xij
    global Y
    Y = {}
    
    #Z : Variable Zij
    global Z 
    Z = {}
    
    # Variable model Gurobi
    global model 
    model = Model('partitioning')
    
    for i in range(1,n+1):
        X[i] = model.addVar(vtype=GRB.BINARY, name="X_"+str(i), obj=0)
    
    for i in range(1,n):
        for j in range(i+1,n+1):
            Y[i,j] = model.addVar(vtype=GRB.CONTINUOUS, name="Y"+str(i)+"_"+str(j), obj=-cij[i-1][j-1])
            Y[j,i] = Y[i,j]

    for j in range(1,n+1):
        for i in range(1,j):
            Z[i,j] = model.addVar(vtype=GRB.BINARY, name="Z_"+str(i)+"_"+str(j), obj=0)
            
    model.modelSense = GRB.MINIMIZE
    model.update()


def defineConstraints(cij, graph, k):
    n = graph.number_of_nodes()
    
    # Le nombre de partitions est égal au nombre de représentants
    model.addConstr(quicksum(X[i] for i in range (1,n+1)) == k)

    # Relaxation linéraire sur les Yij
    for i in range(1,n+1):   
        for j in range (1,i):
            model.addConstr(Y[i,j], "<=", 1)
            model.addConstr(Y[i,j], ">=", 0)

    # Inégalité triangulaire 
    # Si i est dans une partition avec j et k, 
    # alors j et k sont aussi dans une même partition
    for i in range(1,n+1):
        for j in range (1,n+1):
            if j != i:
                for k in range (1,n+1):
                    if k!=j and k!=i:
                        L3a = LinExpr([1,1], [Y[i,j], Y[i,k]])
                        L3a.addConstant(-1)
                        L3b = LinExpr([1],[Y[j,k]])
                        model.addConstr(L3a, "<=", L3b)
    '''
    V1 : 
    # Un sommet i connait soit des voisins déjà représentants, 
    # soit il devient représentant
    for i in range(1,n+1):
        model.addConstr(X[i] + quicksum(Y[i,j] for j in range (1,i)), ">=", 1)
        # Un sommet i représentant d'une partition ne peut pas avoir de sommet j voisin en-dessous de lui      
        for j in range (1,i):
            L1 = LinExpr(X[i]+Y[i,j])
            model.addConstr(L1, "<=", 1)
    '''
    #V2 : Linéarisation des contraintes concernant le représentant d'une partition
    for j in range(1,n+1):
        model.addConstr(X[j] + quicksum(Z[i,j] for i in range (1,j) ) == 1)
    
    for j in range(1,n+1):
        for i in range(1,j):
            model.addConstr(Z[i,j], "<=", X[i])
            model.addConstr(Z[i,j], "<=", Y[i,j])
            model.addConstr(Z[i,j], ">=", X[i] + Y[i,j] -1)
    
    model.update()

def plne(graph, k):
    cij = weightMatrix(graph)
    defineObjf(cij, graph)
    defineConstraints(cij,graph,k)
    model.optimize()
    print "X[i]:", X
    '''
    for i in range(graph.number_of_nodes()):
        if Y[1,i] == 1:
            print i'''
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