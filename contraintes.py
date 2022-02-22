import numpy as np

def barycentre(m, X, ind, N, P, K):
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
                j0 += j*X[i, j, k]

        bar[0] += ind[k].masse*i0
        bar[1] += ind[k].masse*j0
        mtot += ind[k].masse
    
    bar[0] /= mtot
    bar[1] /= mtot
    

    C1 = m.addConstr(bar[0] <= max_bar_i, name = "Cbar1")
    C2 = m.addConstr(bar[1] <= max_bar_j, name = "Cbar2")
    C3 = m.addConstr(bar[0] >= min_bar_i, name = "Cbar3")
    C4 = m.addConstr(bar[1] >= min_bar_j, name = "Cbar4")

    return C1, C2, C3, C4


def unicite_personne(m, X, N, P, K):
    contraintes = []
    for k in range(K):
        s = 0
        for i in range(N):
            for j in range(P):
                s += X[i, j, k]
        contraintes.append(m.addConstr(s == 1, name = "Cuni" + str(k)))
    return contraintes



def unicite_siege(m, X, N, P, K):
    contraintes = []
    for i in range(N):
        for j in range(P):
            s=0
            for k in range(K):
                s += X[i, j, k]
            contraintes.append(m.addConstr(s <= 1, name = "Cuni" + str(i)+','+str(j)))
    return contraintes



def symetrie(m,X,ind,N,P,K):
    place_min={'H':-1,'F':-1}
    for k in range(K):
        if ind[k].groupe==[] and ind[k].transit>90 and place_min[ind[k].categorie]>=0:
            for i_tot in range(N):
                m.addConstr(sum([sum([X[i][j][k] for i in range(i_tot)]) for j in range(P)])<=sum([sum([X[i][j][place_min[ind[k].categorie]] for i in range(i_tot)]) for j in range(P)]))
            place_min[ind[k].categorie]=k
        elif ind[k].groupe==[] and ind[k].transit>90:
            place_min[ind[k].categorie]=k


