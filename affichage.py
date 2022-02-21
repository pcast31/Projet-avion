import numpy as np
     
def affiche_texte(tab,ind,m):
    bar_x=0
    bar_y=0
    K=len(tab[0][0])
    for k in range(K):
        for i in range(len(tab)):
            for j in range(len(tab[0])):
                if tab[i,j,k]==1:
                    bar_x+=i
                    bar_y+=j
                    print("L'individu ",k,"en groupe avec",[indiv.id for indiv in ind[k].groupe],"est à la place",i,j)
    print("barycentre en ligne:" ,bar_x/K,"barycentre en rangée:",bar_y/K)
    print("score :",m.objVal)

def affiche_avion(tab,ind,m):
    (N,P,K) = np.shape(tab)
    avion = -1*np.ones((N,P))
    g = 1
    lien = [[] for _ in range(K)]
    for k in range(K):
        for l in range(K):
            if ind[l] in ind[k].groupe:    
                lien[k].append(l) 
    for k in range(K):
        for i in range(N):
            for j in range(P):
                if tab[i,j,k] == 1:    
                    if len(lien[k]) == 0:
                        avion[i,j] = 0
                    else :
                        avion[i,j] = g
                        if k+1 not in lien[k]:
                            g += 1
    print(avion)
                       