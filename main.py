from initialisation import initialise
from gurobipy import *
import numpy as np
from contraintes import *
from objectif import *
from lirexcel import lirexcel, lirexcel2
from affichage import affiche_texte, affiche_avion
from tk_ffichage import new_aff


N = 30
P = 6
scenario = 7



if __name__ == '__main__':
    m=Model()
    ind=lirexcel2(scenario)
    K=len(ind)
    print(K)
    X=initialise(m,N,P,K)
    m.update()
    barycentre(m,X,ind,N,P,K)
    unicite_personne(m,X,N,P,K)
    unicite_siege(m,X,N,P,K)
    chef_de_groupe(m, X, ind)
    #symetrie(m,X,ind,N,P,K)
    chaises_roulantes(m, X, ind)
    civieres(m, X, ind)
    taille=lutte_des_classes(m,X,ind)
    fct_objectif(m, X, ind)
    m.update()
    m.optimize()
    affiche_texte(X.x,ind,m)
    affiche_avion(X.x,ind,m)
    new_aff(N, P, X.x, ind, m)
    print(taille.x)