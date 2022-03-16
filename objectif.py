import numpy as np
from random import randint
from gurobipy import *

def correspondance(model, X, ind, b):
    """
    On donne un point pour chaque passager ayant un temps de transit
    inférieur à 90 minutes assis dans le prmeier tier de l'avion.
    """
    (N,P,K) = np.shape(X)
    lst = []
    for k in range(K):
        if 0 < ind[k].transit <= 90: # Notons la malheureuse convention fixant à 0 le temps de transit d'un individu n'ayant pas de correspondance
            lst.append(k)
    corres = sum([X[i,j,k] for j in range(P) for i in range(int(N/3)) for k in lst])
    return b*corres

def bonus_groupe1(model, X, ind):
    """
    On donne 2 point pour des amis assis à côté, 1 point s'ils sont sur des rangées adjacentes.
    On linéarise en créant T, qui indique si deux amis sont à côté. 
    Beaucoup trop lourd, mais la solution obtenue en interrompant le programme est bonne. 
    """
    (N,P,K) = np.shape(X)
    lien = [[] for _ in range(K)]
    T = [[[[
        [0 for l in range(K)] for t in range(4)] for k in range(K)] for j in range(P)] for i in range(N)]
    lien = [[] for _ in range(K)] # On crée la liste des amis d'un individu donné
    for k in range(K):
        for l in range(K):
            if ind[l] in ind[k].groupe:    
                lien[k].append(l)
    for i in range(N):
        for j in range(P):
            for n in range(4):
                for k in range(K):
                    for l in lien[k]:
                        T[i][j][k][n][l]= model.addVar(vtype = GRB.BINARY)
    
    for i in range(1,N-1):
        for j in range(1,P-1):
            for k in range(K):
                for l in lien[k]:
                    model.addConstr(T[i][j][k][0][l] <= X[i,j,k])
                    model.addConstr(T[i][j][k][0][l] <= X[i,j+1,l])
                    model.addConstr(T[i][j][k][0][l] >= X[i,j,k] + X[i,j+1,l] - 1)
                    model.addConstr(T[i][j][k][1][l] <= X[i,j,k])
                    model.addConstr(T[i][j][k][1][l] <= X[i-1,j,l])
                    model.addConstr(T[i][j][k][1][l] >= X[i,j,k] + X[i-1,j,l] - 1)
                    model.addConstr(T[i][j][k][2][l] <= X[i,j,k])
                    model.addConstr(T[i][j][k][2][l] <= X[i,j-1,l])
                    model.addConstr(T[i][j][k][2][l] >= X[i,j,k] + X[i,j-1,l] - 1)
                    model.addConstr(T[i][j][k][3][l] <= X[i,j,k])
                    model.addConstr(T[i][j][k][3][l] <= X[i+1,j,l])
                    model.addConstr(T[i][j][k][3][l] >= X[i,j,k] + X[i+1,j,l] - 1)
       
    group = sum([2*T[i][j][k][0][l] + 2*T[i][j][k][2][l] + T[i][j][k][1][l] + T[i][j][k][3][l] for k in range(K)
                    for j in range(1,P-1) for i in range(1,N-1) for l in lien[k]]) # Pour une place à l'intérieur de l'avant
    droite = sum([ 2*T[i][5][k][2][l] + T[i][5][k][1][l] + T[i][5][k][3][l] for k in range(K) # Pour le bord
                    for i in range(1,N-1) for l in lien[k]]) 
    avant = sum([2*T[0][j][k][0][l] + 2*T[0][j][k][2][l] + T[0][j][k][3][l] for k in range(K)
                    for j in range(1,P-1) for l in lien[k]]) 
    gauche = sum([2*T[i][0][k][0][l] + 2*T[i][0][k][2][l] + T[i][0][k][1][l] for k in range(K)
                    for i in range(1,N-1) for l in lien[k]])
    arriere = sum([2*T[N-1][j][k][0][l] + 2*T[N-1][j][k][2][l] + T[N-1][j][k][1][l] for k in range(K)
                    for j in range(1,P-1) for l in lien[k]]) 
    return group 

def bonus_absolu(model,X,ind):
    (N,P,K) = np.shape(X)
    lien = [[] for _ in range(K)]
    for k in range(K):
        for l in range(K):
            if ind[l] in ind[k].groupe:    
                lien[k].append(l)
    traite=[]
    dic={}
    bonus=0
    for k in range(K):
        if ind[k] not in traite:
            groupe=[ind[k].id]+lien[k]
            for l in groupe:
                traite.append(l)
            for i in range(len(groupe)-1):
                    l1=groupe[i]
                    l2=groupe[i+1]
                    if l1>l2:
                        dic[(l1,l2)]=model.addVar(vtype=GRB.INTEGER)
                        model.addConstr(dic[(l1,l2)]>=sum([sum([i*X[i,j,l1]-i*X[i,j,l2] for i in range(N)]) for j in range(P)]))
                        model.addConstr(dic[(l1,l2)]>=sum([sum([i*X[i,j,l2]-i*X[i,j,l1] for i in range(N)]) for j in range(P)]))
                        bonus+=dic[(l1,l2)]
    return bonus



def bonus_groupe2(model, X, ind, a):
    """
    On calcule le nombre de rangées séparant le chef du groupe de chacun de ses compères.
    Puisque ce chef est défini comme étant assis le plus à l'avant de l'avion, on ne calcule que des distances positives.
    Linéaire, et permet de placer les groupes de petite taille sur une même rangée.
    """
    (N,P,K) = np.shape(X)
    lien = [[] for _ in range(K)] # On crée la liste des amis d'un individu donné
    for k in range(K):
        for l in range(K):
            if ind[l] in ind[k].groupe:    
                lien[k].append(l) 
    group = 0
    for k in range(K):
        if len(lien[k]) > 0 and lien[k][0] < k: # La seconde condition caractérise un non-chef de groupe
            group = group + sum([sum([i*X[i,j,k] for i in range(N)]) - sum([i*X[i,j,lien[k][0]] for i in range(N)]) for j in range(P)])
            #group = group + 0.2*sum([sum([j*X[i,j,k] for j in range(P)]) - sum([j*X[i,j,lien[k][0]] for j in range(P)]) for i in range(N)])
    return a*group 

def bonus_seul(model, X, ind, coef):
    """
    On récompense le fait qu'un passager seul soit proche d'une fenêtre afin qu'il ne sépare pas un groupe.
    Pour les groupes de 2 ou 3 : on récompense le fait qu'un chef de groupe soit sur les colonnes 2 ou 5, 
    et qu'un non-chef soit sur une place adjacente. On associe à la moitié des passagers l'un des côtés de l'avion.
    coef est la liste des coefficients devant le bonus pour chaque groupe
    """
    (N,P,K) = np.shape(X)
    lien = [[] for _ in range(K)] # On crée la liste des amis d'un individu donné
    for k in range(K):
        for l in range(K):
            if ind[l] in ind[k].groupe:    
                lien[k].append(l) 
    bordure = coef[0]*sum([X[i,j,k] for k in range(K) for i in range(N) for j in [0,5] if len(lien[k]) == 0]) # Individus seuls
    milieu,milieu2 = 0,0
    if coef[1] > 0:
        milieu = sum([coef[1]*X[i,j,k] + 1*X[i,j+1,lien[k][0]] + 1*X[i,j-1,lien[k][0]] for k in range(K//2) for i in range(N) for j in [1] 
                if len(lien[k]) == 1 and lien[k][0] > k]) # Groupes, 1ère moitié des passagers
        milieu2 = sum([coef[1]*X[i,j,k] + 1*X[i,j+1,lien[k][0]] + 1*X[i,j-1,lien[k][0]] for k in range(K//2,K) for i in range(N) for j in [4] 
                if len(lien[k]) == 1 and lien[k][0] > k]) # Groupes, 2ème moitié des passagers
    if coef[2] > 0:
        milieu += sum([coef[2]*X[i,j,k] + X[i,j+1,lien[k][0]] + X[i,j-1,lien[k][0]] + X[i,j+1,lien[k][1]] + X[i,j-1,lien[k][1]]  for k in range(K//2) for i in range(N) for j in [1] 
                if len(lien[k]) == 2 and lien[k][0] > k and lien[k][1]>k]) # Groupes, 1ère moitié des passagers
        milieu2 += sum([coef[2]*X[i,j,k] + X[i,j+1,lien[k][0]] + X[i,j-1,lien[k][0]]+ X[i,j+1,lien[k][1]] + X[i,j-1,lien[k][1]] for k in range(K//2,K) for i in range(N) for j in [4] 
                if len(lien[k]) == 2 and lien[k][0] > k and lien[k][1]>k]) # Groupes, 2ème moitié des passagers
    return  milieu + bordure + milieu2





def fct_objectif(model, X, ind, coef = [0,2,2], a = 1, b = 1):
    """
    Récapitule les différents objectifs, avec les signes qui vont bien.
    """
    model.setObjective(bonus_groupe2(model, X, ind, a) - correspondance(model, X, ind, b)-bonus_seul(model,X,ind,coef), GRB.MINIMIZE) #
