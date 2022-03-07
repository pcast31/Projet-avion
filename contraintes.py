import numpy as np
from gurobipy import *

def barycentre(m, X, ind, N, P, K):
    """
    Calcule le barycentre et le contraint à rester dans une zone donnée.
    """
    max_bar_j = 4
    max_bar_i = 17
    min_bar_j = 2
    min_bar_i = 13

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
            mtot += ind[k].masse
    bar[0] /= mtot
    bar[1] /= mtot

    C1 = m.addConstr(bar[0] <= max_bar_i, name="Cbar1")
    C2 = m.addConstr(bar[1] <= max_bar_j, name="Cbar2")
    C3 = m.addConstr(bar[0] >= min_bar_i, name="Cbar3")
    C4 = m.addConstr(bar[1] >= min_bar_j, name="Cbar4")

    return C1, C2, C3, C4


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
            model.addConstr(sum([X[i,3,k] + X[i,1,k] for i in range(N)]) == 1)
            model.addConstr(sum([X[N-1,j,k] for j in range(P)]) == 0 )
            for i in range(N-1):
                model.addConstr(4*X[i,3,k] + sum([X[i,4,l] for l in range(K)]) 
                + sum([X[i+1,3,l] for l in range(K)]) + sum([X[i+1,4,l] for l in range(K)]) <= 4)
                model.addConstr(4*X[i,1,k] + sum([X[i,2,l] for l in range(K)]) 
                + sum([X[i+1,1,l] for l in range(K)]) + sum([X[i+1,2,l] for l in range(K)]) <= 4)


def lutte_des_classes(model, X, ind):
    """
    ajoute les contraintes sur la classe business
    taille_bourgeois est le nombre de rangée de siège affecté en classe business
    """
    (N, P, K) = np.shape(X)
    taille_bourgeois=model.addVar(vtype=GRB.INTEGER,name="taille_business")
    for k in range(K):
        if ind[k].classe==1:
            model.addConstr(taille_bourgeois-sum([sum([i*X[i,j,k] for i in range(N)]) for j in range(P)])>=0)
            model.addConstr(sum([X[i,1,k]+X[i,4,k] for i in range(N)])==0)
        else:
            model.addConstr(taille_bourgeois-sum([sum([i*X[i,j,k] for i in range(N)]) for j in range(P)])<=-0.1)
    return taille_bourgeois