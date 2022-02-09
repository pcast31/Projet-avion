from gurobipy import *


def initialise(model,N,P,K):
    return model.addMVar(shape=(N,P,K),vtype = GRB.BINARY, name = "tab")

