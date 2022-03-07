import numpy as np

def barycentre(m, X, ind, N, P, K):
    """
    Calcule le barycentre et le constraint à rester dans une zone donnée.
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
                    j0 += (j+1)*X[i, j, k] #on compte la largeur du couloir

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
    """
    Ajoute la contrainte voulant que chaque passager ait une et une seule place.
    """
    contraintes = []
    for k in range(K):
        s = 0
        for i in range(N):
            for j in range(P):
                s += X[i, j, k]
        contraintes.append(m.addConstr(s == 1, name = "Cuni" + str(k)))
    return contraintes



def unicite_siege(m, X, N, P, K):
    """
    Ajoute la contrainte voulant que chaque place ne puisse acceuilir plusieurs passagers.
    """
    contraintes = []
    for i in range(N):
        for j in range(P):
            s=0
            for k in range(K):
                s += X[i, j, k]
            contraintes.append(m.addConstr(s <= 1, name = "Cuni" + str(i)+','+str(j)))
    return contraintes



def symetrie(m,X,ind,N,P,K):
    """
    Avorton de fonction visant à briser certaines symétries du problème. 
    """
    place_min={'H':-1,'F':-1}
    for k in range(K):
        if ind[k].groupe==[] and ind[k].transit>90 and place_min[ind[k].categorie]>=0:
            for i_tot in range(N):
                m.addConstr(sum([sum([X[i][j][k] for i in range(i_tot)]) for j in range(P)])<=sum([sum([X[i][j][place_min[ind[k].categorie]] for i in range(i_tot)]) for j in range(P)]))
            place_min[ind[k].categorie]=k
        elif ind[k].groupe==[] and ind[k].transit>90:
            place_min[ind[k].categorie]=k

def chef_de_groupe(model, X, ind):
    """
    Impose au premier membre de chaque groupe d'être le plus à l'avant de l'avion, nécessaire pour bonus_groupe2.
    """
    (N,P,K) = np.shape(X)
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
                model.addConstr(sum([i*X[i,j,k] for i in range(N) for j in range(P)]) <= sum([i*X[i,j,l] for i in range(N) for j in range(P)]))
                #model.addConstr(sum([j*X[i,j,k] for j in range(P) for i in range(N)]) <= sum([j*X[i,j,l] for j in range(P) for i in range(N)]))


def enfants(m, X,ind, N, P, K):
    adulte=[]
    for k in range(K):
        if ind[k].masse>40:
            adulte.append(k)
    for k in range(K):
        if ind[k].masse==35:
            for i in range(N):
                for j in range(P):
                    

