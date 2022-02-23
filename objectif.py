import numpy as np
from random import randint
from gurobipy import *

def correspondance(model, X, ind):
    (N,P,K) = np.shape(X)
    lst = []
    for k in range(K):
        if 0 < ind[k].transit <= 90:
            lst.append(k)
    corres = sum([X[i,j,k] for j in range(P) for i in range(int(N/3)) for k in lst])
    return corres

def bonus_groupe(model, X, ind):
    (N,P,K) = np.shape(X)
    lien = [[] for _ in range(K)]
    T = [[[[
        [0 for l in range(K)] for t in range(4)] for k in range(K)] for j in range(P)] for i in range(N)]
    lien = [[] for _ in range(K)]
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
                    for j in range(1,P-1) for i in range(1,N-1) for l in lien[k]]) 
    droite = sum([ 2*T[i][5][k][2][l] + T[i][5][k][1][l] + T[i][5][k][3][l] for k in range(K)
                    for i in range(1,N-1) for l in lien[k]]) 
    avant = sum([2*T[0][j][k][0][l] + 2*T[0][j][k][2][l] + T[0][j][k][3][l] for k in range(K)
                    for j in range(1,P-1) for l in lien[k]]) 
    gauche = sum([2*T[i][0][k][0][l] + 2*T[i][0][k][2][l] + T[i][0][k][1][l] for k in range(K)
                    for i in range(1,N-1) for l in lien[k]])
    arriere = sum([2*T[N-1][j][k][0][l] + 2*T[N-1][j][k][2][l] + T[N-1][j][k][1][l] for k in range(K)
                    for j in range(1,P-1) for l in lien[k]]) 
    return group 

def bonus_groupe2(model, X, ind):
    (N,P,K) = np.shape(X)
    lien = [[] for _ in range(K)]
    for k in range(K):
        for l in range(K):
            if ind[l] in ind[k].groupe:    
                lien[k].append(l) 
    group = 0
    for k in range(K):
        if len(lien[k]) > 0 and lien[k][0] < k:    
            group = group + sum([sum([i*X[i,j,k] for i in range(N)]) - sum([i*X[i,j,lien[k][0]] for i in range(N)]) for j in range(P)])
            #group = group + 0.2*sum([sum([j*X[i,j,k] for j in range(P)]) - sum([j*X[i,j,lien[k][0]] for j in range(P)]) for i in range(N)])
    return group 

def bonus_seul(model, X, ind):
    (N,P,K) = np.shape(X)
    lien = [[] for _ in range(K)]
    for k in range(K):
        for l in range(K):
            if ind[l] in ind[k].groupe:    
                lien[k].append(l) 
    bordure = sum([X[i,j,k] for k in range(K) for i in range(N) for j in [0,5] if len(lien[k]) == 0])
    milieu = sum([X[i,j,k] for k in range(K) for i in range(N) for j in range(1,5) if len(lien[k]) >= 3])
    return milieu

def bonus_par_groupe(model,X,ind):
    (N,P,K) = np.shape(X)
    bonus=0
    traite=[]
    cote=0
    for k in range(K):
        if k not in traite:
            groupe=[ind[k]]+ind[k].groupe
            if len(groupe)<=3 and len(groupe)>1:
                for l in groupe:
                    traite.append(l.id)
                cote=(cote+1)%2
                print(cote,[i.id for i in groupe])
                if len(groupe)==3:
                    bonus+=sum([sum([sum([X[i,j,l.id] for i in range(N)])for j in range(3*cote,3*cote+3)]) for l in groupe])
                else:
                    x=randint(0,1)
                    bonus+=sum([sum([sum([X[i,j,l.id] for i in range(N)])for j in range(3*cote+x,3*cote+2+x)]) for l in groupe])
                #for i in range(N):
                #    for j in range(3*cote,3*cote+3):
                #        for l in groupe:
                #            model.addConstr(X[i,j,l.id]==0)
    return bonus
    

def fct_objectif(model, X, ind):
    bonus_par_groupe(model,X,ind)
    model.setObjective(bonus_groupe2(model, X, ind) - correspondance(model, X, ind) - 0.5*bonus_seul(model, X, ind)-10*bonus_par_groupe(model,X,ind), GRB.MINIMIZE) #
