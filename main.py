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
    barycentre(m,ind,N,P,K)
    unicite(m,N,P,K)
