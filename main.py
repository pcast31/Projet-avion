from initialisation import initialise
from gurobipy import *
import numpy as np
from contraintes import barycentre, unicite_personne,unicite_siege,symetrie,chef_de_groupe
from objectif import *
from lirexcel import lirexcel
from affichage import affiche_texte, affiche_avion


N = 30
P = 3
scenario = 0


if __name__ == '__main__':
    m=Model()
    id_ind=60
    ind_local=lirexcel(scenario)
    groupe=ind_local[id_ind].groupe
    id_ind+=1
    while ind_local[id_ind] in groupe:
        id_ind+=1
    ind=ind_local[0:id_ind]
    K=len(ind)
    print(K)
    X=initialise(m,N,P,K)
    m.update()
    barycentre(m,X,ind,N,P,K)
    unicite_personne(m,X,N,P,K)
    unicite_siege(m,X,N,P,K)
    chef_de_groupe(m, X, ind)
    #symetrie(m,X,ind,N,P,K)
    fct_objectif(m, X, ind)
    m.update()
    m.optimize()
    affiche_texte(X.x,ind,m)
    affiche_avion(X.x,ind,m)
