from initialisation import initialise
from gurobipy import *
import numpy as np
from contraintes import *
from objectif import *
from lirexcel import lirexcel, lirexcel2, reduction
from affichage import affiche_texte, affiche_avion
from tk_ffichage import new_aff
from comparaison import *

# Dimensions de l'avion
N = 29
P = 6
# Instance
scenario = 5

def post_traitement(m, X, ind, lst = [False, False, True]):
    (N,P,K) = np.shape(X)
    lien = [[] for _ in range(K)] # On crée la liste des amis d'un individu donné
    for k in range(K):
        for l in range(K):
            if ind[l] in ind[k].groupe:    
                lien[k].append(l) 

    # On fixe tout le monde sauf les couples espacés sur une même rangée dont on fixe ladite rangée
    for k in range(K): 
        if len(lien[k]) > 2:
            for i in range(N):
                for j in range(P):
                    m.addConstr(X[i,j,k] == X[i,j,k].x)
        elif len(lien[k]) == 2:
            if lst[2] or sum([i*X[i,j,k].x for i in range(N) for j in range(P)]) != sum([i*X[i,j,lien[k][0]].x for i in range(N) for j in range(P)]) or sum([i*X[i,j,k].x for i in range(N) for j in range(P)]) != sum([i*X[i,j,lien[k][1]].x for i in range(N) for j in range(P)]):
                for i in range(N):
                    for j in range(P):
                        m.addConstr(X[i,j,k] == X[i,j,k].x)
            else:
                for i in range(N):
                    m.addConstr(sum([X[i,j,k] for j in range(P)]) == sum(X[i,j,k].x for j in range(P)))
        elif len(lien[k]) == 1:
            if lst[1] or sum([i*X[i,j,k].x for i in range(N) for j in range(P)]) != sum([i*X[i,j,lien[k][0]].x for i in range(N) for j in range(P)]):
                for i in range(N):
                    for j in range(P):
                       m.addConstr(X[i,j,k] == X[i,j,k].x)
            else:
                for i in range(N):    
                    m.addConstr(sum([X[i,j,k] for j in range(P)]) == sum(X[i,j,k].x for j in range(P)))
        else:
            for i in range(N):    
                m.addConstr(sum([X[i,j,k] for j in range(P)]) == sum(X[i,j,k].x for j in range(P)))

def dimension(ind):
    """
    Indique le nombre de places minimal pour une instance donnée.
    """
    nb = 0
    buis = 1
    for e in ind:
        if e.categorie == 'R':
            nb += 4
        elif e.categorie == 'B':
            nb += 12
        else:
            nb += 1
        if e.classe == 1:
            buis += 1
    return nb + buis//2

# Ici, on détermine une solution sans chercher à placer les couples à côté pour alléger les calculs.
# On ré-optimise ensuite en fixant les groupes déjà bien placés.


if __name__ == '__main__':
    m=Model()
    ind=lirexcel2(scenario)

    if dimension(ind) > 180:
        N = 35

    ind_reduit= reduction(scenario, ind) # Scinde les groupes de 4 et plus en petits groupes

    nb = nb_groupes(ind_reduit)
    print(nb)

    a, b = False, False # si a, on gère les groupes de 2 dans le modèle linéaire, sinon dans le postprocessing
    # idem pour b et les groupes de 3


    K=len(ind)
    X=initialise(m,N,P,K)
    m.update()
    barycentre(m,X,ind_reduit,N,P,K)
    unicite_personne(m,X,N,P,K)
    unicite_siege(m,X,N,P,K)
    chef_de_groupe(m, X, ind_reduit)
    #symetrie(m,X,ind,N,P,K)
    chaises_roulantes(m, X, ind_reduit)
    enfant_issue_secours(m, X ,ind_reduit)
    civieres(m, X, ind_reduit)
    nenfants(m,X,ind_reduit)
    taille=lutte_des_classes(m,X,ind_reduit)
    fct_objectif(m, X, ind_reduit, [0,2*a,2*b])
    m.update()
    m.optimize()
    new_aff(N, P, X.x, ind, m)

    print(score(X.x, ind))

    post_traitement(m, X, ind_reduit, [False, a, b])
    m.setObjective(bonus_groupe3(m, X, ind_reduit, [1-a, 1-b]), GRB.MINIMIZE) # bonus_groupe3 quadratique
    m.update()
    m.optimize()
    new_aff(N, P, X.x, ind, m)

    if barycentre2(X.x, ind):
        print("Barycentre bien placé.")
    else:
        print("Problème de barycentre !")

    verif_enfants(X.x, ind)

    print(score(X.x, ind))
