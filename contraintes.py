import numpy as np
from gurobipy import *



def barycentre_restreint(m, X, ind, N, P, K):
    """
    Calcule le barycentre et le contraint à rester dans une zone donnée.
    """
    max_bar_j = 3.5
    min_bar_j = 2.5
    max_bar_i = 16
    min_bar_i = 14
    if N == 35:
        max_bar_i = 19
        min_bar_i = 17

    bar = [0, 0]
    mtot = 0

    for k in range(K):
        i0 = 0
        j0 = 0
        for i in range(N):
            for j in range(P):
                i0 += i*X[i, j, k]
                if j <= 2:
                    j0 += j*X[i, j, k]
                else:
                    j0 += (j+1)*X[i, j, k]  # on compte la largeur du couloir
        bar[0] += ind[k].masse*i0
        bar[1] += ind[k].masse*j0
        mtot += ind[k].masse

        #Le code suivant permet de compter le barycentre 
        #au centre des chaises roulantes/brancards
        """
        if ind[k].categorie in ["H", "F", "E"]:
            bar[0] += ind[k].masse*i0
            bar[1] += ind[k].masse*j0
            mtot += ind[k].masse
        elif ind[k] == "R":
            bar[0] += ind[k].masse*(i0 + 1/2)
            bar[1] += ind[k].masse*(j0 + 1/2)
            mtot += ind[k].masse
        else:
            bar[0] += ind[k].masse*(i0 + 3/2)
            bar[1] += ind[k].masse*(j0 + 1)
            mtot += ind[k].masse"""
    bar[0] /= mtot
    bar[1] /= mtot

    C1 = m.addConstr(bar[0] <= max_bar_i, name="Cbar1")
    C2 = m.addConstr(bar[1] <= max_bar_j, name="Cbar2")
    C3 = m.addConstr(bar[0] >= min_bar_i, name="Cbar3")
    C4 = m.addConstr(bar[1] >= min_bar_j, name="Cbar4")

    return C1, C2, C3, C4



def barycentre(m, X, ind, N, P, K):
    """
    Calcule le barycentre et le contraint à rester dans une zone donnée.
    """
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
                i0 += i*X[i, j, k]
                if j <= 2:
                    j0 += j*X[i, j, k]
                else:
                    j0 += (j+1)*X[i, j, k]  # on compte la largeur du couloir
        bar[0] += ind[k].masse*i0
        bar[1] += ind[k].masse*j0
        mtot += ind[k].masse

        #Le code suivant permet de compter le barycentre 
        #au centre des chaises roulantes/brancards
        """
        if ind[k].categorie in ["H", "F", "E"]:
            bar[0] += ind[k].masse*i0
            bar[1] += ind[k].masse*j0
            mtot += ind[k].masse
        elif ind[k] == "R":
            bar[0] += ind[k].masse*(i0 + 1/2)
            bar[1] += ind[k].masse*(j0 + 1/2)
            mtot += ind[k].masse
        else:
            bar[0] += ind[k].masse*(i0 + 3/2)
            bar[1] += ind[k].masse*(j0 + 1)
            mtot += ind[k].masse"""
    bar[0] /= mtot
    bar[1] /= mtot

    C1 = m.addConstr(bar[0] <= max_bar_i, name="Cbar1")
    C2 = m.addConstr(bar[1] <= max_bar_j, name="Cbar2")
    C3 = m.addConstr(bar[0] >= min_bar_i, name="Cbar3")
    C4 = m.addConstr(bar[1] >= min_bar_j, name="Cbar4")

    return C1, C2, C3, C4

def ligne(m,X,Xf,N,P,K):
    for k in range(K):
        for p in range(K):
            for i in range(N):
                if sum([X[i,j,k] for j in range(6)])==sum([X[i,j,p] for j in range(6)]):
                    m.addConstr(sum([Xf[i,j,k] for j in range(6)])==sum([Xf[i,j,p] for j in range(6)]))

def unicite_personne(m, X, N, P, K):
    """
    Ajoute la contrainte voulant que chaque passager ait une et une seule place.
    """
    contraintes = []
    for k in range(K):
        s = 0
        for i in range(N):
            for j in range(P):
                s += X[i, j, k]
        contraintes.append(m.addConstr(s == 1, name="Cuni" + str(k)))
    return contraintes


def unicite_siege(m, X, N, P, K):
    """
    Ajoute la contrainte voulant que chaque place ne puisse acceuilir plusieurs passagers.
    """
    contraintes = []
    for i in range(N):
        for j in range(P):
            s = 0
            for k in range(K):
                s += X[i, j, k]
            contraintes.append(m.addConstr(s <= 1, name="Cuni" + str(i)+','+str(j)))
    return contraintes


def symetrie(m, X, ind, N, P, K):
    """
    Avorton de fonction visant à briser certaines symétries du problème.
    """
    place_min = {'H': -1, 'F': -1}
    for k in range(K):
        if ind[k].groupe == [] and ind[k].transit > 90 and place_min[ind[k].categorie] >= 0:
            for i_tot in range(N):
                m.addConstr(sum([sum([X[i][j][k] for i in range(i_tot)]) for j in range(P)]) <= sum(
                    [sum([X[i][j][place_min[ind[k].categorie]] for i in range(i_tot)]) for j in range(P)]))
            place_min[ind[k].categorie] = k
        elif ind[k].groupe == [] and ind[k].transit > 90:
            place_min[ind[k].categorie] = k


def chef_de_groupe(model, X, ind):
    """
    Impose au premier membre de chaque groupe d'être le plus à l'avant de l'avion, nécessaire pour bonus_groupe2.
    """
    (N, P, K) = np.shape(X)
    lien = [[] for _ in range(K)]
    for k in range(K):
        for l in range(K):
            if ind[l] in ind[k].groupe:
                lien[k].append(l)
    vus = []
    for k in range(K):
        b = True
        for l in lien[k]:
            if l in vus:
                b = False
        if b:
            vus.append(k)
            for l in lien[k]:
                model.addConstr(sum([i*X[i, j, k] for i in range(N) for j in range(P)])
                                <= sum([i*X[i, j, l] for i in range(N) for j in range(P)]))
                #model.addConstr(sum([j*X[i,j,k] for j in range(P) for i in range(N)]) <= sum([j*X[i,j,l] for j in range(P) for i in range(N)]))

def chaises_roulantes(model, X, ind):
    """
    S'assure que les chaises roulantes occupent un carré 2x2 le long de l'allée centrale.
    """
    (N, P, K) = np.shape(X)
    for k in range(K):
        if ind[k].categorie == "R":
            model.addConstr(sum([X[i, 3, k] + X[i, 2, k] for i in range(N)]) == 1)
            model.addConstr(sum([X[0, j, k] for j in range(P)]) == 0)
            for i in range(1,N):
                model.addConstr(4*X[i, 3, k] + sum([X[i, 4, l] for l in range(K)])
                                + sum([X[i-1, 3, l] for l in range(K)]) + sum([X[i-1, 4, l] for l in range(K)]) <= 4)
                model.addConstr(4*X[i, 2, k] + sum([X[i, 1, l] for l in range(K)])
                                + sum([X[i-1, 1, l] for l in range(K)]) + sum([X[i-1, 2, l] for l in range(K)]) <= 4)

def civieres(model, X, ind):
    """
    S'assure que les civières occupent un rectangle 4x3.
    """
    (N, P, K) = np.shape(X)
    for k in range(K):
        if ind[k].categorie == "B":
            model.addConstr(sum([X[i,3,k] + X[i,2,k] for i in range(N)]) == 1)
            model.addConstr(sum([X[i,j,k] for i in range(3) for j in range(P)]) == 0)
            for i in range(3,N):
                model.addConstr(12*X[i,3,k] + sum([X[i,4,l] for l in range(K)])  
                + sum([X[i,5,l] for l in range(K)]) 
                + sum([X[i-a,3,l] for l in range(K) for a in range(1,4)]) 
                + sum([X[i-a,4,l] for l in range(K) for a in range(1,4)])
                + sum([X[i-a,5,l] for l in range(K) for a in range(1,4)]) <= 12)
                model.addConstr(12*X[i,2,k] + sum([X[i,0,l] for l in range(K)])  
                + sum([X[i,1,l] for l in range(K)]) 
                + sum([X[i-a,0,l] for l in range(K) for a in range(1,4)]) 
                + sum([X[i-a,1,l] for l in range(K) for a in range(1,4)])
                + sum([X[i-a,2,l] for l in range(K) for a in range(1,4)]) <= 12)

def lutte_des_classes(model, X, ind):
    """
    Ajoute les contraintes sur la classe business.
    taille_bourgeois est le nombre de rangée de siège affecté en classe business.
    """
    (N, P, K) = np.shape(X)
    taille_bourgeois = model.addVar(vtype=GRB.INTEGER, name="taille_business")
    for k in range(K):
        if ind[k].classe == 1:
            model.addConstr(taille_bourgeois -
                            sum([sum([i*X[i, j, k] for i in range(N)]) for j in range(P)]) >= 0.1)
            model.addConstr(sum([X[i, 1, k]+X[i, 4, k] for i in range(N)]) == 0)
        else:
            model.addConstr(taille_bourgeois-sum([sum([i*X[i,j,k] for i in range(N)]) for j in range(P)])<=0)
    return taille_bourgeois
            
def enfant_issue_secours(model, X, ind):
    """
    Impose aux enfants de ne pas se situer devant les issues de secours.
    """
    (_,_,K) = X.shape
    for k in range(K):    
        if ind[k].categorie == 'E':
            for j in range(1, 7):
                model.addConstr(X[11, j-1, k] == 0, name="C_enf_sec"+str(j))

def nenfants(model, X, ind, b = False):
    """
    Garantie que les nenfants ne soient pas seuls ༼ つ ◕_◕ ༽つ  o(一︿一+)o
    Par défaut, on veut un adulte sur une demie-rangée s'il y a un enfant.
    Si b, on impose que l'adulte soit immédiatement à côté du mioche.
    S'il y a trop d'enfants, on se contente de placer un adulte sur un carré 3*3.
    S'il y en a vraiment trop, on ne fait rien.
    """
    (N,P,K) = np.shape(X)
    pop = [0,0]
    for k in range(K):
        if ind[k].categorie in ['H', 'F']:
            pop[0] += 1
        elif ind[k].categorie == 'E':
            pop[1] += 1
    if b and pop[1] <= pop[0]: # On choisit d'abandonner la contrainte si il y a plus d'enfants que d'adultes.
        for i in range(N):
            model.addConstr(sum([ind[k].age*X[i,j,k] for j in range(P-2,P) for k in range(K)]) >= 0)
            model.addConstr(sum([ind[k].age*X[i,j,k] for j in range(P-3,P-1) for k in range(K)]) >= 0)
            model.addConstr(sum([ind[k].age*X[i,j,k] for j in range(2) for k in range(K)]) >= 0)
            model.addConstr(sum([ind[k].age*X[i,j,k] for j in range(1,3) for k in range(K)]) >= 0)
    elif not b and pop[1] <= pop[0]:    
        for i in range(N):
            model.addConstr(sum([ind[k].age*X[i,j,k] for j in range(3,P) for k in range(K)]) >= 0)
            model.addConstr(sum([ind[k].age*X[i,j,k] for j in range(3) for k in range(K)]) >= 0)
    elif pop[1] <= 9*pop[0]:
        for i in range(0, N-2, 3):
            model.addConstr(sum([ind[k].age**3 * X[x,j,k] for j in range(3) for x in [i,i+1,i+2] for k in range(K)]) >= 0)
            model.addConstr(sum([ind[k].age**3 * X[x,j,k] for j in range(3,P) for x in [i,i+1,i+2] for k in range(K)]) >= 0)
    else:
        print("Trop d'enfants, contraintes correspondantes ignorées.")
