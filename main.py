from initialisation import initialise
from gurobipy import *
import numpy as np
from contraintes import barycentre, unicite_personne,unicite_siege,symetrie
from objectif import *
from lirexcel import lirexcel
from affichage import affiche_texte


N = 30
P = 6
scenario = 0


if __name__ == '__main__':
    m=Model()
    ind=lirexcel(scenario)
    K=len(ind)
    X=initialise(m,N,P,K)
    m.update()
    barycentre(m,X,ind,N,P,K)
    unicite_personne(m,X,N,P,K)
    unicite_siege(m,X,N,P,K)
    symetrie(m,X,ind,N,P,K)
    fct_objectif(m, X, ind)
    m.update()
    m.optimize()
    affiche_texte(X.x,ind)