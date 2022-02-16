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
    T = model.addMVar(shape=(N,P,K,4,K), vtype = GRB.BINARY) # 0 droite, 1 avant, 2 gauche, 3 arriere 
    for i in range(1,N-1):
        for j in range(1,P-1):
            for k in range(K):
                for l in lien[k]:
                    model.addConstr(T[i,j,k,0,l] <= X[i,j,k])
                    model.addConstr(T[i,j,k,0,l] <= X[i,j+1,l])
                    model.addConstr(T[i,j,k,0,l] >= X[i,j,k] + X[i,j+1,l] - 1)
                    model.addConstr(T[i,j,k,1,l] <= X[i,j,k])
                    model.addConstr(T[i,j,k,1,l] <= X[i-1,j,l])
                    model.addConstr(T[i,j,k,1,l] >= X[i,j,k] + X[i-1,j,l] - 1)
                    model.addConstr(T[i,j,k,2,l] <= X[i,j,k])
                    model.addConstr(T[i,j,k,2,l] <= X[i,j-1,l])
                    model.addConstr(T[i,j,k,2,l] >= X[i,j,k] + X[i,j-1,l] - 1)
                    model.addConstr(T[i,j,k,3,l] <= X[i,j,k])
                    model.addConstr(T[i,j,k,3,l] <= X[i+1,j,l])
                    model.addConstr(T[i,j,k,3,l] >= X[i,j,k] + X[i+1,j,l] - 1)
       
    group = sum([2*T[i,j,k,0,l] + 2*T[i,j,k,2,l] + T[i,j,k,1,l] + T[i,j,k,3,l] for k in range(K)
                    for j in range(1,P-1) for i in range(1,N-1) for l in lien[k]]) 
    """avant = sum([2*T[0,j,k,1,j,l] + T[0,j,k,i,j+1,l] + T[0,j,k,0,j-1,l] for k in range(K)
                    for j in range(1,P-1) for l in lien[k]]) 
    arriere = sum([2*T[N-1,j,k,N-1,j,l] + T[N-1,j,k,N-1,j+1,l] + T[N-1,j,k,N-1,j-1,l] for k in range(K)
                    for j in range(1,P-1) for l in lien[k]]) 
    gauche = sum([2*T[i,0,k,i+1,0,l] + 2*T[i,0,k,i-1,0,l] + T[i,0,k,i,1,l] for k in range(K)
                    for i in range(1,N-1) for l in lien[k]]) 
    droite = sum([2*T[i,P-1,k,i+1,P-1,l] + 2*T[i,P-1,k,i-1,j,l] + T[i,P-1,k,i,P-1,l] for k in range(K)
                    for i in range(1,N-1) for l in lien[k]]) """
    return group 

def bonus_groupe2(model, X, ind):
    (N,P,K) = np.shape(X)
    lien = [[] for _ in range(K)]
    for k in range(K):
        for l in range(K):
            if ind[l] in ind[k].groupe:    
                lien[k].append(l) 
    group = sum([X[i+1,j,k]*X[i,j,l] for i in range(N-1) for j in range(P)  for k in range(K) for l in lien[k]])


    return group 

def fct_objectif(model, X, ind):
    model.setObjective(correspondance(model, X, ind) + bonus_groupe2(model, X, ind), GRB.MAXIMIZE) 