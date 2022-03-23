from initialisation import initialise
from gurobipy import *
import numpy as np
from contraintes import *
from objectif import *
from lirexcel import lirexcel, lirexcel2, reduction
from affichage import affiche_texte, affiche_avion
from tk_ffichage import new_aff
from random import choice


N = 30
P = 6
scenario = 0


def choix_possible(k,X_taille,X_inter,taille,place_associe):
    place_possible=[]
    groupe=[ind[k]]+ind[k].groupe
    debut=0
    if ind[k].categorie==0:
        debut=taille
    for i in range(debut,N):
        for j in range(P):
            if X_taille[i][j]==len(groupe) and X_inter[i][j]==0:
                place_possible.append(place_associe[(i,j)])
    return place_possible




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
    fct_objectif(m, X, ind_reduit, [0,2,2])
    m.update()
    m.optimize()
    print("fini")
    Xsol=X.x
    X_res=[[int(sum([ind_reduit[k].id*Xsol[i][j][k] for k in range(K)]))for j in range(P)] for i in range(N)]
    X_taille=[[0 for j in range(P)] for i in range(N)]
    places_par_groupe={}
    print(1)
    for i in range(N):
        for j in range(P):
            if X_res[i][j]>0:
                X_taille[i][j]=len(ind[X_res[i][j]].groupe)+1
                if ind[X_res[i][j]].idgroupe in places_par_groupe:
                    places_par_groupe[ind[X_res[i][j]].idgroupe].append((i,j))
                else:
                    places_par_groupe[ind[X_res[i][j]].idgroupe]=[(i,j)]
    print(2)
    places_associes={}
    for k in places_par_groupe:
        for elt in places_par_groupe[k]:
            places_associes[elt]=places_par_groupe[k]

    groupe_deja_place=[]
    X_courant=[[0 for j in range(P)]for i in range(N)]
    for k in range(K):
        if ind[k].idgroupe not in groupe_deja_place:
            groupe_deja_place.append(ind[k].idgroupe)
            possibilites=choix_possible(k,X_taille,X_courant,taille.x,places_associes)
            positions=choice(possibilites)
            groupe=[ind[k]]+ind[k].groupe
            for id in range(len(groupe)):
                X_courant[positions[id][0]][positions[id][1]]=groupe[id].id
    
    X_final=np.array([[[0 for k in range(K)] for j in range(P)]for i in range(N)])
    for i in range(N):
        for j in range(P):
            if X_courant[i][j]!=0:
                X_final[i][j][X_courant[i][j]]=1
    
    print(X_final)
        

    affiche_texte(X_final,ind,m)
    affiche_avion(X_final,ind,m)
    new_aff(N, P, X_final, ind, m)
    #print(taille2.x)