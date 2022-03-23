from individu import *
from contraintes import *
from lirexcel import lirexcel2
from objectif import *
from affichage import *
from tk_ffichage import new_aff
from gurobipy import *
from initialisation import *

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
        milieu = sum([coef[1]*X[i,j,k] + X[i,j+1,lien[k][0]] + X[i,j-1,lien[k][0]] for k in range(K//2) for i in range(N) for j in [1] 
                if len(lien[k]) == 1 and lien[k][0] > k]) # Groupes, 1ère moitié des passagers
        milieu2 = sum([coef[1]*X[i,j,k] + X[i,j+1,lien[k][0]] + X[i,j-1,lien[k][0]] for k in range(K//2,K) for i in range(N) for j in [4] 
                if len(lien[k]) == 1 and lien[k][0] > k]) # Groupes, 2ème moitié des passagers
    if coef[2] > 0:
        milieu += sum([coef[2]*X[i,j,k] + X[i,j-1,lien[k][0]] + X[i,j+1,lien[k][1]] + X[i,j+1,lien[k][0]] + X[i,j-1,lien[k][1]] for k in range(K//2) for i in range(N) for j in [1] 
                if len(lien[k]) == 2 and lien[k][0] > k and lien[k][1]>k]) # Groupes, 1ère moitié des passagers
        milieu2 += sum([coef[2]*X[i,j,k] + X[i,j-1,lien[k][0]]+ X[i,j+1,lien[k][1]]+ X[i,j+1,lien[k][0]]+ X[i,j-1,lien[k][1]] for k in range(K//2,K) for i in range(N) for j in [4] 
                if len(lien[k]) == 2 and lien[k][0] > k and lien[k][1]>k]) # Groupes, 2ème moitié des passagers
    return  milieu + bordure + milieu2

def carre_max(X,i,j,i_max,j_max):
    if sum([X[i2][j2] for j2 in range(j,j_max) for i2 in range(i,i_max)])==0:
        largeur=carre_max(X,i,j,i_max,j_max+1)
        longeur=carre_max(X,i,j,i_max+1,j_max)
        if largeur+longeur==0:
            return (i_max-i)*(j_max-j)
        else:
            return max(largeur,longeur)
    else:
        return 0

def espacement(ind,X):
    (N,P,K)=np.shape(X)
    X_bin=[[sum([X[i,j,k] for k in range(K)]) for j in range(P)]for i in range(N)]
    score=0
    for i in range(N):
        for j in range(P):
            score+=carre_max(X,i,j,i+1,j+1)
    return score

def objectif_inter(model, X, ind,coef = [0,1,1] b = 1):
    model.setObjective(espacement(ind,X) - correspondance(model, X, ind, b)-bonus_seul(model,X,ind,coef), GRB.MAXIMIZE)

                    