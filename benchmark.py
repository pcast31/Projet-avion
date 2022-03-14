from individu import *
from contraintes import *
from lirexcel import lirexcel2
from objectif import *
from affichage import *
from tk_ffichage import new_aff
from gurobipy import *
from initialisation import *
import time
from random import randint

N = 30
P = 6
K = 100
ind = []
grp = [10]

for k in range(K):
    if randint(0,1) == 0:
        s = 'H'
    else:
        s = 'F'
    if k < 2*grp[0]:
        ind.append(Individu(k, s, randint(0,300), k//2, 0))
    else:
        ind.append(Individu(k, s, randint(0,300), k-grp[0], 0))

for k in range(0,2*grp[0],2):
    ind[k].ajout_au_groupe(ind[k+1])
    ind[k+1].ajout_au_groupe(ind[k])

m=Model()
X=initialise(m,N,P,K)
m.update()
barycentre(m,X,ind,N,P,K)
unicite_personne(m,X,N,P,K)
unicite_siege(m,X,N,P,K)
chef_de_groupe(m, X, ind)
symetrie(m,X,ind,N,P,K)
chaises_roulantes(m, X, ind)
civieres(m, X, ind)
taille=lutte_des_classes(m,X,ind)
fct_objectif(m, X, ind, [0.1,2,2])
m.update()
m.optimize()
affiche_texte(X.x,ind,m)
affiche_avion(X.x,ind,m)
new_aff(N, P, X.x, ind, m)
print(taille.x)