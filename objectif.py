def correspondance(model, X, ind):
    (N,P,K) = np.shape(X)
    lst = []
    for k in range(K):
        if ind[k].transit <= 90:
            lst.append(k)
    corres = sum([[[X[i,j,k] for j in range(P)] for i in range(N/3)] for k in lst])
    return corres

def bonus_groupe(model, X, ind):
    (N,P,K) = np.shape(X)
    lien = [[] for _ in range(K)]
    for k in range(K):
        for l in ind[k].groupe:
            lien[k].append(l)
    group = sum([[[[X[i+1,j,l] + X[i-1,j,l] + X[i,j+1,l] + X[i,j-1,l] for l in lien[k]]
             for j in range(1,P-1)] for i in range(1,N-1)] for k in range(K)])
    return group

def fct_objectif(model, X, ind):
    model.addConstr(correspondance(model, X, ind) + bonus_groupe(model, X, ind))