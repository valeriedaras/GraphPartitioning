# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 08:21:03 2015

@author: Valerie Daras et Julie Riviere
"""

from gurobipy import *
import script as s
import objectivefunctions as objf

# Fonction permettant de calculer la représentation matricielle d'un graphe
# @graph : graphe à étudier
# Return : matrice cij
def weightMatrix(graph):
    n = graph.number_of_nodes()
    cij = [[0 for x in range (n)] for x in range (n)]
    for i in range (n):
        for j in range (i+1, n):
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
    
    #Min : Taille min des partitions
    global Min
    Min = {}
    
    #Max : Taille max des partitions
    global Max
    Max = {}    
    
    #W : Variable W
    global W
    W = {}

    global ProdWX
    ProdWX = {}    
    global ProdYW
    ProdWY = {}
    
    # Variable model Gurobi
    global model 
    model = Model('partitioning')
    
    for i in range(1,n+1):
        X[i] = model.addVar(vtype=GRB.BINARY, name="X_"+str(i), obj=0)
    
    for i in range(1,n):
        for j in range(i+1,n+1):
            Y[i,j] = model.addVar(vtype=GRB.BINARY, name="Y_"+str(i)+"_"+str(j), obj=-cij[i-1][j-1])
            Y[j,i] = Y[i,j]

    for j in range(1,n+1):
        for i in range(1,j):
            Z[i,j] = model.addVar(vtype=GRB.BINARY, name="Z_"+str(i)+"_"+str(j), obj=0)
    
    for i in range(1,n):
        for j in range(i+1,n+1):
            W[i,j] = model.addVar(vtype=GRB.BINARY, name="W_"+str(i)+"_"+str(j), obj=0)
            W[j,i] = W[i,j]

    for i in range(1,n+1):
        ProdWX[i] = model.addVar(vtype=GRB.BINARY, name="ProdW_"+str(i), obj=0)
        #ProdYW[i] = model.addVar(vtype=GRB.INTEGER, name="ProdYW_"+str(i), obj=0)

    #Max = model.addVar(vtype=GRB.INTEGER, name="Max", obj=0)      
    Min = model.addVar(vtype=GRB.INTEGER, name="Min", obj=0)
    
    model.modelSense = GRB.MINIMIZE
    model.update()


def defineConstraints(cij, graph, k, opt, val):
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

    #V2 : Linéarisation des contraintes concernant le représentant d'une partition
    for j in range(1,n+1):
        model.addConstr(X[j] + quicksum(Z[i,j] for i in range (1,j) ) == 1)
    
    for j in range(1,n+1):
        for i in range(1,j):
            model.addConstr(Z[i,j], "<=", X[i])
            model.addConstr(Z[i,j], "<=", Y[i,j])
            model.addConstr(Z[i,j], ">=", X[i] + Y[i,j] -1)
            
    # Contrainte supplémentaire sur la taille des partitions
    if opt == 0:
        # La taille maximale d'une partition est de <val>
        # La taille maximale correspond au cardinal de l'ensemble formé par : 
        # un représentant + tous les sommets qui ont ce même représentant
        for i in range (1,n+1):
            model.addConstr(X[i]+quicksum(Y[i,j] for j in range(i+1, n+1) if X[i] == 1) <= val)
            
    elif opt == 1:
        # La différence de taille maximale 
        # entre la plus petite et la plus grande partition est de <val>
        for i in range (1,n+1):
            # Inégalité 1 et 2 :
            model.addConstr(Min <= X[i] + quicksum(Y[i,j] for j in range(i+1, n+1) if X[i] == 1))
            # Inégalité 7 et 8 : peut être inutile/redondant
            model.addConstr(X[i] + quicksum(Y[i,j] for j in range(i+1, n+1) if X[i] == 1) <= n)
        
        for i in range (1,n):
            # Inégalité 3
            model.addConstr(X[i] + quicksum(Y[i,j] for j in range(i+1, n+1) if X[i] == 1) 
            <= X[i+1] + quicksum(Y[i+1,j] for j in range(i+2, n+1) if X[i+1] == 1) + n*W[i,i+1])
        
        for i in range (1,n):
            # Inégalité 4
            model.addConstr(X[i+1] + quicksum(Y[i+1,j] for j in range(i+2, n+1) if X[i+1] == 1) 
            <= X[i] + quicksum(Y[i,j] for j in range(i+1, n+1) if X[i] == 1) + n*(1-W[i,i+1]))
        
        # Inégalité 5 : Linéarisation du produit
        for i in range(1,n):
            model.addConstr(ProdWX[i], "<=", n*W[i,i+1])
            model.addConstr(ProdWX[i], "<=", X[i] + quicksum(Y[i,j] for j in range(i+1, n+1) if X[i] == 1))
            model.addConstr(ProdWX[i], ">=", X[i] + quicksum(Y[i,j] for j in range(i+1, n+1) if X[i] == 1) -n*(1-W[i,i+1]))
            model.addConstr(Min, ">=", X[i] + quicksum(Y[i,j] for j in range(i+1, n+1) if X[i] == 1) 
                                        -ProdWX[i] + ProdWX[i+1])
        '''    
        for i in range(1,n):
            
            
            
        '''
    else:
        print "Parameter opt should be {0,1}"
        exit(0)
    
    model.update()


# Fonction permettant d'afficher la solution du problème
# @n : nombre de sommets
# @k : nombre de partitions
def displayPartitions(n,k):    
    for i in range(1,n+1):
        if model.getVarByName("X_"+str(i)).getAttr('X') == 1:
            print "Partiton avec representant",i,":"
            for j in range(i+1,n+1):
                if model.getVarByName("Y_"+str(i)+"_"+str(j)).getAttr('X') > 0:
                    print j


# Fonction permettant d'initialiser le problème et de lancer sa résolution
# @graph : graphe à étudier
# @k : nombre de partitions
# @opt et @val: si opt=0 alors val représente le nombre max de sommets dans une partition
# si opt=1, alors val représente la différence max de nombre de sommets
# entre la plus grande partition et la plus petite partiton
def plne(graph,k, opt, val):
    
    # Calcul de la représentation matricielle du graphe
    cij = weightMatrix(graph)

    # Définition des variables et de la fonction objectif
    defineObjf(cij, graph) 

    # Définition des contraintes
    defineConstraints(cij,graph,k,opt,val)

    # Lancement du solver
    model.optimize()
    
    # Vérification du status du solver / de la solution
    s = model.status
    if s == GRB.Status.UNBOUNDED:
        print "Model cannot be solved because it is unbounded"
    if s == GRB.Status.OPTIMAL:
        print "The optimal objective is %g" % model.objVal
        n = graph.number_of_nodes()
        # Affichage de la solution
        displayPartitions(n,k)
    if s == GRB.Status.INF_OR_UNBD and s != GRB.Status.INFEASIBLE:
        print "Optimization was stopped with status %d" % s


def main():
    copyFilename = "unitEx.graph"
    graph = s.createGraph(copyFilename)
    plne(graph, 2, 1, 22)
    

if __name__ == '__main__':
    main()