def barycentre(m, ind, N, P, K):
    max_bar_j = 5
    max_bar_i = 5
    min_bar_j = 3
    min_bar_i = 3

    bar = [0, 0]
    mtot = 0

    X = m.getVars()[0]

    for k in range(K):
        i0 = 0
        j0 = 0
        for i in range(N):
            for j in range(P):
                i0 = i*X[i, j, k]
                j0 = j*X[i, j, k]

        bar[0] = ind[k].masse*i0
        bar[1] = ind[k].masse*j0
        mtot += ind[k].masse
    
    bar[0] /= mtot
    bar[1] /= mtot
    

    C1 = m.addConstr(bar[0] <= max_bar_j, name = "Cbar1")
    C2 = m.addConstr(bar[1] <= max_bar_i, name = "Cbar2")
    C3 = m.addConstr(bar[0] >= min_bar_j, name = "Cbar3")
    C4 = m.addConstr(bar[1] >= min_bar_i, name = "Cbar4")

    return C1, C2, C3, C4


def unicite(m, N, P, K):
    contraintes = []
    X = m.getVars()[0]
    for k in range(K):
        s = 0
        for i in range(N):
            for j in range(P):
                s += X[i, j, k]
        contraintes.append(m.addConstr(s == 1, name = "Cuni" + str(k)))
    return contraintes
