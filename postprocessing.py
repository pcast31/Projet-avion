from initialisation import initialise
from gurobipy import *
import numpy as np
from contraintes import *
from objectif import *
from lirexcel import lirexcel, lirexcel2, reduction
from affichage import affiche_texte, affiche_avion
from tk_ffichage import new_aff
from comparaison import *
import time

def post_traitement(m, X, ind, lst = [False, False, True]):
    """
    On fixe la position des groupes bien placés.
    On fixe les rangées de tout le monde.
    lst[k] indique si on fixe les groupes de taille k+1 ou non.
    """
    (N,P,K) = np.shape(X)

    lien = [[] for _ in range(K)] # On crée la liste des amis d'un individu donné
    for k in range(K):
        for l in range(K):
            if ind[l] in ind[k].groupe:    
                lien[k].append(l) 

    # On fixe tout le monde sauf les groupes espacés sur une même rangée dont on fixe ladite rangée
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


def statique(m, ind, ind_reduit, t_max, a = False, b = True,  P = 6):
    """
    Renvoie une solution statique avec post-traitement.
    a resp b indique si on prend en compte les groupes de taille 2 resp 3 dans la première optimisation.
    Sinon, on les prend en compte dans la seconde.
    """

    if dimension(ind) > 180: # On commence par choisir l'avion de taille adaptée
        N = 35
    else:
        N = 29

    # On ajoute toutes les contraintes
    K=len(ind)
    X=initialise(m,N,P,K)
    m.update()
    barycentre_restreint(m,X,ind_reduit,N,P,K)
    unicite_personne(m,X,N,P,K)
    unicite_siege(m,X,N,P,K)
    chef_de_groupe(m, X, ind_reduit)
    chaises_roulantes(m, X, ind_reduit)
    enfant_issue_secours(m, X ,ind_reduit)
    civieres(m, X, ind_reduit)
    nenfants(m,X,ind_reduit)
    taille=lutte_des_classes(m,X,ind_reduit)
    
    m.update()

    # On ajoute l'objectif linéaire
    fct_objectif(m, X, ind_reduit, [0,2*a,2*b]) 

    m.setParam('Timelimit', t_max)
    m.update()
    
    start_time = time.time()

    m.optimize()

    # On regarde si Gurobi a bien trouvé une solution optimale
    if time.time() - start_time > t_max:
        return None

    # On effectue le post-traitement, avec un objectif quadratique qui gère les groupes ignorés précedemment
    post_traitement(m, X, ind_reduit, [False, a, b])
    m.setObjective(bonus_groupe3(m, X, ind_reduit, [1-a, 1-b]), GRB.MINIMIZE) 
    m.update()
    
    start_time = time.time()

    m.optimize()

    t = time.time() - start_time

    if t > t_max:
        return None

    # Si Gurobi a terminé, on renvoie le score et le placement correspondant
    if t <= t_max:
        return (score(X.x, ind)[0], X.x)

def meilleure_sol_statique(scenario, t_max = 100, lst_a = [0,1], lst_b = [0,1]):
    """
    Renvoie une solution optimale en testant les 4 possibilités de prises en compte des groupes.
    t_max correspond au temps maximal accordé à Gurobi.
    lst_a et lst_b permettent d'indiquer quelles façons de prendre en compte les groupes on souhaite essayer.
    """
    ind=lirexcel2(scenario)
    ind_reduit= reduction(scenario, ind) # Scinde les groupes de 4 et plus en petits groupes
    
    # On essaye de résoudre l'instance avec les différentes façons de prendre en compte les groupes.
    dic_score = [[0,0],[0,0]]
    placement = [[0,0],[0,0]]
    for a in lst_a:
        for b in lst_b:
            m = Model()
            
            resultat = statique(m, ind, ind_reduit, t_max, a, b)
            if resultat != None:
                dic_score[a][b], placement[a][b] = resultat

    # Si aucune instance n'a terminé dans le temps imparti
    if sum([dic_score[a][b] for a in range(2) for b in range(2)]) == 0:
        print("Rien ne termine ! Il faut augmenter t_max.")
        return(None)

    # Sinon, on renvoie la meilleure solution obtenue
    best = 0
    a_best, b_best = -1,-1
    for a in range(2):
        for b in range(2):
            if dic_score[a][b] > best:
                a_best, b_best = a, b
                best = dic_score[a][b]
        
    X = placement[a_best][b_best]
    
    return X, ind, ind_reduit, best, a_best, b_best

# scenario = 8
# t_max = 2000

# X, ind, ind_reduit, best, a_best, b_best = meilleure_sol_statique(scenario, t_max, [0], [0])
# (N,P,_) = X.shape
# new_aff(N, P, X, ind)

# if barycentre2(X, ind):
#     print("Barycentre bien placé.")
# else:
#     print("Problème de barycentre !")

# verif_enfants(X, ind)
# print(f"Le placement des groupes est bon à {best}. On l'obtient pour {a_best, b_best}")
