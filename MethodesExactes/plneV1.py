# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 08:21:03 2015

@author: Valerie Daras et Julie Riviere
"""

from gurobipy import * 
import objectivefunctions as objf
import script as s

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

# Fonction permettant de définir les variables du problème et la fonction objectif
# @cij : représentation matricielle du graphe
# @graph : graphe à étudier
def defineObjf(cij, graph):
    n = graph.number_of_nodes()
    
    # Variable Xi
    global X
    X = {}
    
    #Y : Variable Yij
    global Y
    Y = {}
    
    # Variable modèle Gurobi
    global model 
    model = Model('partitioning')
    
    # Ajout de la variable Xi au modèle
    for i in range(1, n+1):
        X[i] = model.addVar(vtype=GRB.BINARY, name="X_"+str(i), obj=0)

    # Ajout de la variable Yij au modèle    
    for i in range(1, n):
        for j in range(i+1, n+1):
            Y[i,j] = model.addVar(vtype=GRB.BINARY, name="Y_"+str(i)+"_"+str(j), obj=-cij[i-1][j-1])
            Y[j,i] = Y[i,j]

    # Problème de minimisation
    model.modelSense = GRB.MINIMIZE
    model.update()
    
    
# Fonction permettant de définir les contraintes du problème  
# @cij : représentation matricielle du graphe
# @graph : graphe à étudier
# @k : nombre de partitions à créer
def defineConstraints(cij, graph, k):
    # Nombre de noeuds dans le graphe
    n = graph.number_of_nodes()
    
    # Contrainte n°1 :
    # Le nombre de partitions est égal au nombre de représentants
    model.addConstr(quicksum(X[i] for i in range (1,n+1)) == k)
    
    # Contrainte n°2 : Inégalité triangulaire 
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
        
    # Contrainte n°3 : Choix des représentants
    # Un sommet i connait soit des voisins déjà représentants, 
    # soit il devient représentant
    for i in range(1,n+1):
        model.addConstr(X[i] + quicksum(Y[i,j] for j in range (1,i)), ">=", 1)
        # Un sommet i représentant d'une partition ne peut pas avoir de sommet j voisin en-dessous de lui      
        for j in range (1,i):
            L1 = LinExpr(X[i]+Y[i,j])
            model.addConstr(L1, "<=", 1)        

    # Relaxation linéaire sur les Yij
    for i in range(1,n+1):   
        for j in range (1,i):
            model.addConstr(Y[i,j], "<=", 1)
            model.addConstr(Y[i,j], ">=", 0)
    
    
# Fonction permettant d'afficher la solution du problème
# @n : nombre de sommets
def displayPartitions(n):    
    for i in range(1,n+1):
        if model.getVarByName("X_"+str(i)).getAttr('X') == 1:
            print "Partiton avec representant",i,":"
            for j in range(i+1,n+1):
                if model.getVarByName("Y_"+str(i)+"_"+str(j)).getAttr('X') > 0:
                    print j

# Fonction permettant d'initialiser le problème et de lancer sa résolution
# @graph : graphe à étudier
# @k : nombre de partitions 
def plne(graph,k):
    
    # Calcul de la représentation matricielle du graphe
    cij = weightMatrix(graph)

    # Définition des variables et de la fonction objectif
    defineObjf(cij, graph) 

    # Définition des contraintes
    defineConstraints(cij,graph,k)

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
    if s == GRB.Status.INF_OR_UNBD and s != GRB.Status.INFEASIBLE:
        print "Optimization was stopped with status %d" % s


def main():
    copyFilename = "../graphs/unitEx.graph"
    graph = s.createGraph(copyFilename)
    plne(graph, 2)
    

if __name__ == '__main__':
    main()