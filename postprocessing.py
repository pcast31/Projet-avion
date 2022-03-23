from individu import *
from contraintes import *
from lirexcel import lirexcel2
from objectif import *
from affichage import *
from tk_ffichage import new_aff
from gurobipy import *
from initialisation import *

def barycentre2(x, ind):
    N,P, K = x.shape

    max_bar_j = 4
    min_bar_j = 2
    if N == 30 :
        max_bar_i = 17
        min_bar_i = 13
    if N == 35:
        max_bar_i = 20.5
        min_bar_i = 16.5

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

def postprocessing(x, ind):
    N,P,K = x.shape
    carte = np.zeros(N, P)
    placement = [(0, 0)]*K
    lien = [[] for _ in range(K)] 
    for k in range(K):
        for l in range(K):
            if ind[l] in ind[k].groupe:    
                lien[k].append(l)

    for i in range(N):
        for j in range(P):
            b = True
            for k in range(k):
                if x[i, j, k] == 1:
                    carte[i,j] = k
                    placement[k] = (i, j)
                    b = False
            if b:
                carte[i, j] = -1
    

    for i in range(N):
        liste_couple = []
        places_ok = []
        deja_vu = []
        for j in range(P):
            if carte[i, j] != -1:
                groupe = ind[carte[i, j]].groupe
                if len(groupe) == 1 and carte[i, j] not in deja_vu:
                    deja_vu += [carte[i, j], groupe[0]]
                    i1, j1 = placement[groupe[0]]
                    if i1 == i and abs(j - j1) > 1:
                        liste_couple += [(j, j1)]
                elif len(groupe) == 0:
                    places_ok += [j]
            else:
                places_ok += [j]
        
        
        

            


