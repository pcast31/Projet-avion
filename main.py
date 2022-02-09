from initialisation import initialise
from gurobipy import * 
import numpy as np
from contraintes import barycentre,unicite
from lirexcel import lirexcel


N=30
P=6
scenario=0


if __name__ == '__main__':
    m=Model()
    ind=lirexcel(scenario)
    K=len(ind)
    X=initialise(m,N,P,K)
    m.update()
    print('coucou')
    barycentre(m,X,ind,N,P,K)
    unicite(m,X,N,P,K)
