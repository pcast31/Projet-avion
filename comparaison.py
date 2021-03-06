from individu import *
from contraintes import *
from lirexcel import lirexcel2
from objectif import *
from affichage import *
from tk_ffichage import new_aff
from gurobipy import *
from initialisation import *

def score(x, ind):
    """
    Renvoie le ratio entre le score d'une solution et le score maximal possible.
    """
    N,P,K = x.shape
    s_groupe = 0
    s_groupe_tot = 0
    s_transit = 0
    s_transit_tot = 0
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
    deja_vu = []
    for k in range(K):
        i0, j0 = placement[k]
        groupe = lien[k]
        K = (len(groupe)+1)//3
        r = (len(groupe)+1)%3
        if k not in deja_vu:
            deja_vu += groupe
            s_groupe_tot += K*4 + max(K-1, 0)*0.3*3 + (0 if r==0 else (0.3*min(1, K) if r == 1 else 2 + min(1, K)*0.3*2))
        for k2 in groupe:
            #on compte deux fois chaque voisins, il faudra le prendre en compte à la fin
            i1, j1 = placement[k2]
            if i1 == i0:
                if abs(j1 - j0) ==1:
                    s_groupe += 2
            elif abs(i1 - i0) == 1:
                if j1 == j0:
                    s_groupe += 0.3
        if 0 < ind[k].transit <= 90:
            s_transit_tot += 1
            if i0 <= N/3:
                s_transit += 1
    #print(f"Le placement des groupes est bon à {s_groupe/(2*s_groupe_tot)}, et le transit est respecté à {s_transit/s_transit_tot}.")
    return s_groupe/(2*s_groupe_tot), s_transit/s_transit_tot

def barycentre2(x, ind):
    """
    Permet de vérifier le bon placement du barycentre pour une solution qui ne serait pas obtenue via Gurobi. 
    """
    N,P, K = x.shape

    max_bar_j = 4
    min_bar_j = 2
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

def verif_enfants(X, ind, b = False):
    """
    Permet de vérifier qu'une solution non-générée par Gurobi satisfait les contraintes sur les enfants.
    """
    (N,P,K) = X.shape
    pop = [0,0]
    for k in range(K):
        if ind[k].categorie in ['H', 'F']:
            pop[0] += 1
        elif ind[k].categorie == 'E':
            pop[1] += 1
    enfants_seuls = 0
    if b and pop[1] <= pop[0]: # On choisit d'abandonner la contrainte si il y a plus d'enfants que d'adultes.
        for i in range(N):
            enfants_seuls += min(sum([ind[k].age*X[i,j,k] for j in range(P-2,P) for k in range(K)]), 0)
            enfants_seuls += min(sum([ind[k].age*X[i,j,k] for j in range(P-3,P-1) for k in range(K)]), 0)
            enfants_seuls += min(sum([ind[k].age*X[i,j,k] for j in range(2) for k in range(K)]), 0)
            enfants_seuls += min(sum([ind[k].age*X[i,j,k] for j in range(1,3) for k in range(K)]), 0)
    elif not b and pop[1] <= pop[0]:    
        for i in range(N):
            enfants_seuls += min(sum([ind[k].age*X[i,j,k] for j in range(3,P) for k in range(K)]), 0)
            enfants_seuls += min(sum([ind[k].age*X[i,j,k] for j in range(3) for k in range(K)]), 0)
    elif pop[1] <= 9*pop[0]:
        for i in range(0, N-2, 3):
            enfants_seuls += min(sum([ind[k].age**3 * X[x,j,k] for j in range(3) for x in [i,i+1,i+2] for k in range(K)]), 0)
            enfants_seuls += min(sum([ind[k].age**3 * X[x,j,k] for j in range(3,P) for x in [i,i+1,i+2] for k in range(K)]), 0)
    else:
        print("Trop d'enfants, contraintes correspondantes ignorées.")

    issues = (sum([X[11,j,k] for j in range(6) for k in range(K) if ind[k].categorie == 'E']) == 0)
    if issues:
        print("Pas d'enfants sur les issues de secours.") 
    else:
        print("Il y a des enfants sur les issues de secours !")
    print(f'Il y a {-enfants_seuls} enfants seuls.')
