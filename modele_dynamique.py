from individu import *
from initialisation import initialise
from gurobipy import *
import numpy as np
from contraintes import *
from objectif import *
from lirexcel import lirexcel, lirexcel2, reduction
from affichage import affiche_texte, affiche_avion
from tk_ffichage import new_aff
import threading

# Taille de l'avion. Une des instance nécessite d'augmenter N
N = 30
P = 6
# Choix de l'instance
scenario = 0

m=Model()
ind=lirexcel2(scenario)
ind_reduit= ind #reduction(scenario, ind) # Scinde les groupes de 4 et plus en petits groupes
K=len(ind)
X=initialise(m,N,P,K)
m.update()
barycentre(m,X,ind_reduit,N,P,K)
unicite_personne(m,X,N,P,K)
unicite_siege(m,X,N,P,K)
chef_de_groupe(m, X, ind_reduit)
chaises_roulantes(m, X, ind_reduit)
civieres(m, X, ind_reduit)
nenfants(m,X,ind_reduit)
taille=lutte_des_classes(m,X,ind_reduit) 
#nb_group = nb_groupes(ind)
fct_objectif(m, X, ind_reduit, [0,0,2], 1, 1) # Voir objectif.py. Ici, on omet le rapprochement sur une rangée des couples.
m.params.outputflag = 0
m.update()
m.optimize()

optimum = m.objVal

lst_choix = [[] for k in range(K)]
lst_choix[0] = [(i,j) for i in range(N) for j in range(P)]
"""
for i in range(N):
    for j in range(P):
        c = m.addConstr(X[i,j,0] == 1)
        m.update()
        m.optimize()
        if not m.status == GRB.INFEASIBLE and m.objVal == optimum:
            lst_choix[0] += (i,j)
        m.remove(c)
        """

for k in range(1,K):
    print(len(lst_choix[k-1]))
    if len(lst_choix[k-1]) == 0:
        print("ça bloque")
        break
    e = randint(0,len(lst_choix[k-1])-1)
    a,b = lst_choix[k-1][e][0],lst_choix[k-1][e][1]
    print(f"Le passager {k} est à la place {a,b}.")
    m.addConstr(X[a,b,k-1] == 1)
    for i in range(N):
        for j in range(P):
            c = m.addConstr(X[i,j,k] == 1)
            m.update()
            m.optimize()
            if not m.status == GRB.INFEASIBLE and m.objVal == optimum:
                lst_choix[k].append(tuple((i,j)))
            m.remove(c)

print(lst_choix)