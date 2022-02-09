from gurobipy import *

def initialise(model,n_individu,n_colonne):
    return [[[model.addVar(vtype = GRB.BINARY, name = "col{}, ligne{}, ind{}".format(i,j,k), lb = 0) for k in range(n_individu)]for j in range(6)]for i in range(n_colonne)]
