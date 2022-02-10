import numpy as np
from gurobipy import *

def correspondance(model, X, ind):
    (N,P,K) = np.shape(X)
    lst = []
    for k in range(K):
        if ind[k].transit <= 90:
            lst.append(k)
    corres = sum([X[i,j,k] for j in range(P) for i in range(int(N/3)) for k in lst])
    return corres

def bonus_groupe(model, X, ind):
    (N,P,K) = np.shape(X)
    lien = [[] for _ in range(K)]
    for k in range(K):
        for l in range(K):
            if ind[l] in ind[k].groupe:    
                lien[k].append(l)    
    group = sum([(2*X[i+1,j,l] + 2*X[i-1,j,l] + X[i,j+1,l] + X[i,j-1,l])*X[i,j,k] for k in range(K)
                    for j in range(1,P-1) for i in range(1,N-1) for l in lien[k]]) 
    avant = sum([2*X[1,j,l] + X[0,j+1,l] + X[0,j-1,l] for k in range(K)]
                    for j in range(1,P-1) for l in lien[k])
    arriere = sum([2*X[N-2,j,l] + X[N-1,j+1,l] + X[N-1,j-1,l] for k in range(K)
                    for j in range(1,P-1) for l in lien[k]])
    gauche = sum([2*X[i+1,0,l] + 2*X[i-1,0,l] + X[i,1,l] for k in range(K)]
                    for i in range(1,N-1) for l in lien[k])
    droite = sum([2*X[i+1,P-1,l] + 2*X[i-1,P-1,l] + X[i,P-2,l] for k in range(K)]
                    for i in range(1,N-1) for l in lien[k])
    return group + avant + arriere + gauche + droite

def fct_objectif(model, X, ind):
    model.setObjective(correspondance(model, X, ind) + bonus_groupe(model, X, ind), GRB.MAXIMIZE)