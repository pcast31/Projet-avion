from initialisation import initialise
from gurobipy import *
import numpy as np
from contraintes import barycentre, unicite
from objectif import *
from lirexcel import lirexcel


N = 30
P = 6
scenario = 0


if __name__ == '__main__':
    m=Model()
    ind=lirexcel(scenario)
    K=len(ind)
    X=initialise(m,N,P,K)
    m.update()
    #barycentre(m,X,ind,N,P,K)
    unicite(m,X,N,P,K)
    fct_objectif(m, X, ind)
    m.update()
    m.optimize()
    print(X.x[0,:,:],m.objVal)