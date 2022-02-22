import numpy as np
from random import randint
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
    group = sum([X[i+1,j,k]*X[i,j,l] for i in range(N-1) for j in range(P)  for k in range(K) for l in lien[k]])


    return group 


def bonus_groupe3(model, X, ind):

    (N,P,K) = np.shape(X)
    lien = [[] for _ in range(K)]
    for k in range(K):
        for l in range(K):
            if ind[l] in ind[k].groupe:    
                lien[k].append(l)

    traite=[]
    dic_x={}
    dic_y={}

    dic_absx={}
    dic_absy={}
    group=0
    for k in range(K):
        if k not in traite and lien[k]!=[]:
            traite.append(k)
            for l in lien[k]:
                traite.append(l)

            groupe=[k]+lien[k]

            for l in groupe:
                dic_x[l]=sum([sum([j*X[i,j,l] for i in range(N)]) for j in range(P)])
                dic_y[l]=sum([sum([i*X[i,j,l] for i in range(N)]) for j in range(P)])
            
        
            for id in range(len(groupe)-1):
                        l1=groupe[id]
                        l2=groupe[id+1]

                        model.addConstr(10*dic_y[l1]+dic_x[l1]>=10*dic_y[l2]+dic_x[l2])
                        dic_absx[(k,l1,l2)]=model.addVar(vtype=GRB.INTEGER,name="absx"+str(l1)+','+str(l2))
                        model.addConstr(dic_absx[(k,l1,l2)]>=dic_x[l1]-dic_x[l2])
                        model.addConstr(dic_absx[(k,l1,l2)]>=-dic_x[l1]+dic_x[l2])
                        group+= dic_absx[(k,l1,l2)]#dic_x[groupe[id]]-dic_x[groupe[id+1]]

                        #model.addConstr(dic_y[groupe[id]]>=dic_y[groupe[id+1]])
                        dic_absy[(k,l1,l2)]=model.addVar(vtype=GRB.INTEGER,name="absy"+str(l1)+','+str(l2))
                        model.addConstr(dic_absy[(k,l1,l2)]>=dic_y[l1]-dic_y[l2])
                        model.addConstr(dic_absy[(k,l1,l2)]>=-dic_y[l1]+dic_y[l2])
                        group+= 2*dic_absy[(k,l1,l2)]#(dic_y[groupe[id]]-dic_y[groupe[id+1]])                    
       
    return group 



def fct_objectif(model, X, ind):
    model.setObjective(bonus_groupe3(model, X, ind)-correspondance(model, X, ind), GRB.MINIMIZE) 
