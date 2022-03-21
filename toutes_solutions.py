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
scenario = 5


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
nb_group = nb_groupes(ind)
print(nb_group)
fct_objectif(m, X, ind_reduit, [0,0,2], 1, 1) # Voir objectif.py. Ici, on omet le rapprochement sur une rangée des couples.
m.update()
m.optimize()

optimum = m.objVal
lst_solutions = []
a = 0
while optimum == m.objVal and a < 3:     #not m.status == GRB.INFEASIBLE: 
    a += 1
    sol = np.array([[[X[i,j,k].x == 1 for k in range(K)] for j in range(P)] for  i in range(N)])
    print(np.shape(sol))
    lst_solutions.append(sol)
    for s in lst_solutions:    
        m.addConstr(sum(X[i,j,k]*s[i,j,k] for i in range(N) for j in range(P) for k in range(K)) <= K-1 )
    m.update()
    m.optimize()

t = []
for i in range(len(lst_solutions)):
    def aff():
        new_aff(N, P, lst_solutions[i], ind, m)
    t.append(threading.Thread(target=aff))
    t[-1].start()

for i in range(len(lst_solutions)):
    t[i].join()