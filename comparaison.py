from individu import *
from contraintes import *
from lirexcel import lirexcel2
from objectif import *
from affichage import *
from tk_ffichage import new_aff
from gurobipy import *
from initialisation import *

def score(x, ind):
    N,P,K = x.shape
    s_groupe = 0
    s_transit = 0
    placement = [(0, 0)]*K
    lien = [[] for _ in range(K)] 
    for k in range(K):
        for l in range(K):
            if ind[l] in ind[k].groupe:    
                lien[k].append(l)

    for k in range(K):
        for i in range(N):
            for j in range(P):
                if x[i, j, k] == 1:
                    placement[k] = (i, j)
    for k in range(K):
        i0, j0 = placement[k]
        groupe = lien[k]
        #on compte deux fois chaque voisins mais c'est pas grave étant donné que
        #cette fonction ne sert qu'à comparer différents résultats
        for k2 in groupe:
            i1, j1 = placement[k2]
            if j1 == j0:
                if abs(i1 - i0) ==1:
                    s_groupe += 2
            elif abs(j1 - j0) == 1:
                if i1 == i0:
                    s_groupe += 1
        if ind[k].transit <= 90 and i0 <= N/3:
            s_transit += 1
    return s_groupe, s_transit

def barycentre2(x, ind):
    N,P, K = x.shape

    max_bar_j = 4
    min_bar_j = 2
    if N == 30 :
        max_bar_i = 17
        min_bar_i = 13
    if N == 35:
        max_bar_i = 20
        min_bar_i = 16

    bar = [0, 0]
    mtot = 0

    for k in range(K):
        i0 = 0
        j0 = 0
        for i in range(N):
            for j in range(P):
                i0 += i*x[i, j, k]
                if j <= 2:
                    j0 += j*x[i, j, k]
                else:
                    j0 += (j+1)*x[i, j, k]  # on compte la largeur du couloir
        bar[0] += ind[k].masse*i0
        bar[1] += ind[k].masse*j0
        mtot += ind[k].masse

    bar[0] /= mtot
    bar[1] /= mtot

    return (min_bar_i <= bar[0] <= max_bar_i) and (min_bar_j <= bar[1] <= max_bar_j) 
