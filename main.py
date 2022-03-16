from initialisation import initialise
from gurobipy import *
import numpy as np
from contraintes import *
from objectif import *
from lirexcel import lirexcel, lirexcel2, reduction
from affichage import affiche_texte, affiche_avion
from tk_ffichage import new_aff


N = 30
P = 6
scenario = 2



if __name__ == '__main__':
    m=Model()
    ind=lirexcel2(scenario)
    ind_reduit=reduction(scenario, ind)
    K=len(ind)
    X=initialise(m,N,P,K)
    m.update()
    barycentre(m,X,ind_reduit,N,P,K)
    unicite_personne(m,X,N,P,K)
    unicite_siege(m,X,N,P,K)
    chef_de_groupe(m, X, ind_reduit)
    #symetrie(m,X,ind,N,P,K)
    chaises_roulantes(m, X, ind_reduit)
    civieres(m, X, ind_reduit)
    nenfants(m,X,ind_reduit)
    taille=lutte_des_classes(m,X,ind_reduit)
    fct_objectif(m, X, ind_reduit, [0,0,0])
    m.update()
    m.optimize()


    X_res=X.x


    m2=Model()
    Xbis=initialise(m2,N,P,K)
    m2.update()
    barycentre(m2,Xbis,ind_reduit,N,P,K)
    unicite_personne(m2,Xbis,N,P,K)
    unicite_siege(m2,Xbis,N,P,K)
    chef_de_groupe(m2, Xbis, ind_reduit)
    #symetrie(m,X,ind,N,P,K)
    chaises_roulantes(m2, Xbis, ind_reduit)
    civieres(m2, Xbis, ind_reduit)
    nenfants(m2,Xbis,ind_reduit)
    ligne(m2,X_res,Xbis,N,P,K)
    taille2=lutte_des_classes(m2,Xbis,ind_reduit)
    objectif_ligne(m2,X_res, Xbis, ind_reduit,N,P,K)

    m2.update()
    m2.optimize()
    affiche_texte(X.x,ind,m)
    affiche_avion(X.x,ind,m)
    new_aff(N, P, X.x, ind, m)
    affiche_texte(Xbis.x,ind,m2)
    affiche_avion(Xbis.x,ind,m2)
    new_aff(N, P, Xbis.x, ind, m2)
    #print(taille2.x)