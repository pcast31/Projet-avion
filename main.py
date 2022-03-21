from individu import *
from initialisation import initialise
from gurobipy import *
import numpy as np
from contraintes import *
from objectif import *
from lirexcel import lirexcel, lirexcel2, reduction
from affichage import affiche_texte, affiche_avion
from tk_ffichage import new_aff

# Taille de l'avion. Une des instance nécessite d'augmenter N
N = 30
P = 6
# Choix de l'instance
scenario = 5



if __name__ == '__main__':
    m=Model()
    ind=lirexcel2(scenario)
    ind_reduit= ind #reduction(scenario, ind) # Scinde les groupes de 4 et plus en petits groupes
    K=len(ind)
    X=initialise(m,N,P,K)
    m.update()
    barycentre(m,X,ind_reduit,N,P,K)
    unicite_personne(m,X,N,P,K)
    unicite_siege(m,X,N,P,K)
    chef_de_groupe(m, X, ind_reduit)
    chaises_roulantes(m, X, ind_reduit)
    civieres(m, X, ind_reduit)
    nenfants(m,X,ind_reduit)
    taille=lutte_des_classes(m,X,ind_reduit) 
    nb_group = nb_groupes(ind)
    print(nb_group)
    fct_objectif(m, X, ind_reduit, [0,0,2], 1, 1) # Voir objectif.py. Ici, on omet le rapprochement sur une rangée des couples.
    m.update()
    m.optimize()
    affiche_texte(X.x,ind,m)
    affiche_avion(X.x,ind,m)
    new_aff(N, P, X.x, ind, m)
