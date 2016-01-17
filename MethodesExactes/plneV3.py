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
  
    #W : Variable Wij
    global W 
    W = {} 

    #A1 : Variable A1
    global A1
    A1 = {}  

    #A2 : Variable A2
    global A2
    A2 = {}
    
    #B : Variable B
    global B
    B = {} 

    #XX : Variable XX
    global XX
    XX = {}    
    
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
            W[i,j] = model.addVar(vtype=GRB.INTEGER, name="W_"+str(i)+"_"+str(j), obj=0)
            W[j,i] = W[i,j]
            A1[i,j] = model.addVar(vtype=GRB.INTEGER, name="A1_"+str(i)+"_"+str(j), obj=0)
            A1[j,i] = A1[i,j]
            A2[i,j] = model.addVar(vtype=GRB.INTEGER, name="A2_"+str(i)+"_"+str(j), obj=0)
            A2[j,i] = A2[i,j]
            B[i,j] = model.addVar(vtype=GRB.BINARY, name="B_"+str(i)+"_"+str(j), obj=0)
            B[j,i] = B[i,j]
            XX[i,j] = model.addVar(vtype=GRB.BINARY, name="XX_"+str(i)+"_"+str(j), obj=0)
            XX[j,i] = XX[i,j]
    
    
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
                for h in range (1,n+1):
                    if h!=j and h!=i:
                        L3a = LinExpr([1,1], [Y[i,j], Y[i,h]])
                        L3a.addConstant(-1)
                        L3b = LinExpr([1],[Y[j,h]])
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
            model.addConstr(X[i]+quicksum(Y[i,j] for j in range(i+1, n+1)) <= val)
            
    elif opt == 1:
        # La différence de taille maximale 
        # entre la plus petite et la plus grande partition est de <val>
            
        for a in range (1,n):
            for b in range (a+1,n+1):
                # Contraintes pour le produit XX[a,b]=X[a]*X[b]
                model.addConstr(XX[a,b], "<=", X[a])
                model.addConstr(XX[a,b], "<=", X[b])
                model.addConstr(XX[a,b], ">=", X[a] + X[b] - 1)
                
                # Expression linéraire pour calculer la taille de la partition 
                # à partir du sommet a
                abs1 = LinExpr(quicksum(Y[a,j] for j in range(a+1, n+1)))
                
                # Expression linéraire pour calculer la taille de la partition 
                # à partir du sommet b
                abs2 = LinExpr(quicksum(Y[b,j] for j in range(b+1, n+1)))
                
                # Contraintes pour la valeur absolue de la différence de taille
                # Le facteur XX[a,b] permet d'assurer que 
                # les deux sommets a et b sont des représentants
                model.addConstr(XX[a,b]*(abs1 - abs2), "==", A1[a,b] - A2[a,b])

                # Contraintes pour la valeur absolue
                model.addConstr(A1[a,b], ">=", 0)
                model.addConstr(A1[a,b], "<=", B[a,b]*n)
                model.addConstr(A2[a,b], ">=", 0)
                model.addConstr(A2[a,b], "<=", (1-B[a,b])*n)
                model.addConstr(W[a,b], "==",  A1[a,b] + A2[a,b])
                model.addConstr(W[a,b], "<=", val)

    else:
        print "Parameter opt should be {0,1}"
        exit(0)
    
    model.update()


# Fonction permettant d'afficher la solution du problème
# @n : nombre de sommets
def displayPartitions(n):    
    for i in range(1,n+1):
        if model.getVarByName("X_"+str(i)).getAttr('X') > 0:
            print "Partiton avec representant",i,":"
            for j in range(i+1,n+1):
                if model.getVarByName("Y_"+str(i)+"_"+str(j)).getAttr('X') > 0:
                    print j

# Fonction permettant d'afficher la solution du problème
# @n : nombre de sommets
def displaySizeDifference(n):    
    for i in range(1,n+1):
        for j in range (i+1,n+1):
            print "W_",i,"_",j,":",model.getVarByName("W_"+str(i)+"_"+str(j)).getAttr('X')



# Fonction permettant d'initialiser le problème et de lancer sa résolution
# @graph : graphe à étudier
# @k : nombre de partitions
# @opt et @val: si opt=0 alors val représente le nombre max de sommets dans une partition
# si opt=1, alors val représente la différence max de nombre de sommets
# entre la plus grande partition et la plus petite partiton
def plne(graph, k, opt, val):
    
    # Calcul de la représentation matricielle du graphe
    cij = weightMatrix(graph)

    # Définition des variables et de la fonction objectif
    defineObjf(cij,graph) 

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
        displayPartitions(n)
        if opt == 1:
            displaySizeDifference(n)
    if s == GRB.Status.INF_OR_UNBD and s != GRB.Status.INFEASIBLE:
        print "Optimization was stopped with status %d" % s


def main():
    copyFilename = "../graphs/unitEx.graph"
    graph = s.createGraph(copyFilename)
    plne(graph, 3, 0, 11)
    

if __name__ == '__main__':
    main()