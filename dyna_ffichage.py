import tkinter as tk
from random import randrange
from initialisation import initialise
from gurobipy import *
import numpy as np
from contraintes import *
from objectif import *
from lirexcel import lirexcel, lirexcel2, reduction
from affichage import affiche_texte, affiche_avion
from tk_ffichage import new_aff



N = 30
P = 6
scenario = 0



def dyna_ffichage(N, P,K,tab, ind):
    
    groupes={}
    for indiv in ind:
        if indiv.idgroupe not in groupes:
            groupes[indiv.idgroupe]=[indiv]
        else :
            groupes[indiv.idgroupe].append(indiv)
        
    place_ind={}
    for i in range(N):
        for j in range(N):
            if sum([k*tab[i][j][k] for k in range(K)])>0:
                place_ind[sum([k*tab[i][j][k] for k in range(K)])]=(i,j)


    def calculer(g):
        places = []

        if 'R' not in [individu.categorie for individu in groupes[g]] and 'B' not in [individu.categorie for individu in groupes[g]]:
            return [place_ind[individu] for individu in groupes[g]]
        
        for gr in groupes:
            if len(groupes[gr])==len(groupes[g]) and groupes[g][0].classe==groupes[gr][0].classe and 'R' not in [individu.categorie for individu in groupes[gr]] and 'B' not in [individu.categorie for individu in groupes[gr]]:
                places.append([place_ind[individu] for individu in groupes[gr]])

        print(places)

        return places

    root = tk.Tk()

    canvas = tk.Canvas(root, width=30 * N + 10 * (N + 1), height=30 * (P + 1) + 10 * (P + 2))
    canvas.pack()

    canvas.create_rectangle(0, 0, 30 * N + 10 * (N + 1), 30 * (P + 1) + 10 * (P + 2), fill='#3C3C4B')

    places = [[canvas.create_rectangle(10 + i * 40, 10 + (j + j // 3) * 40, 10 + i * 40 + 30, 10 + (j + j // 3) * 40 + 30, width=0, fill='#465582') for j in range(P)] for i in range(N)]

    tailles_groupes = [0] * ind[-1].idgroupe
    ind_repr=[0]*ind[-1].idgroupe
    for i in ind:
        tailles_groupes[i.idgroupe - 1] = len(i.groupe) + 1
        ind_repr[i.idgroupe-1]=i
    places_proposees = calculer(tailles_groupes[0])
    for i, j in places_proposees:
        canvas.itemconfig(places[i][j], fill='#FF0000')

    groupe_compteur = 1

    groupe_label = tk.Label(root, text=f'Groupe {groupe_compteur}')
    groupe_label.pack()


    def aleatoire_command():
        nonlocal groupe_compteur
        nonlocal places_proposees
        nonlocal places_selectionnees

        places_selectionnees = []

        if groupe_compteur == len(tailles_groupes):
            aleatoire_button['state'] = 'disabled'
            opti_button['state'] = 'disabled'

        else:
            groupe_compteur += 1
            groupe_label['text'] = f'Groupe {groupe_compteur}'

            places_proposees = calculer(tailles_groupes[groupe_compteur - 1])

            for i in range(N):
                for j in range(P):
                    if (i, j) in [i for i in places for places in places_proposees]:
                        canvas.itemconfig(places[i][j], fill='#FF0000')
                    else:
                        canvas.itemconfig(places[i][j], fill='#465582')


    aleatoire_button = tk.Button(root, text='Choix aléatoire', command=aleatoire_command)
    aleatoire_button.pack()

    
    def opti_command():
        nonlocal groupe_compteur

        if groupe_compteur == len(tailles_groupes):
            aleatoire_button['state'] = 'disabled'
            opti_button['state'] = 'disabled'

        else:
            groupe_compteur += 1
            groupe_label['text'] = f'Groupe {groupe_compteur}'

            places = calculer()
    

    opti_button = tk.Button(root, text='Choix optimal', command=opti_command)
    opti_button.pack()


    places_selectionnees = []

    def onclick(event):
        print('==========')

        i = -1
        j = -1

        if event.x % 40 <= 10:
            print('x en dehors d\'une place')
        else:
            i = event.x // 40
            print(f'i = {i}')

        if event.y % 40 <= 10 or 120 <= event.y <= 170:
            print('y en dehors d\'une place')
        else:
            j = event.y // 40
            if j >= 3:
                j -= 1
            print(f'j = {j}')
        
        if i >= 0 and j >= 0:
            if (i, j) in places_proposees and (i, j) not in places_selectionnees:
                places_selectionnees.append((i, j))
                canvas.itemconfig(places[i][j], fill='#00FF00')

            elif (i, j) in places_proposees:
                places_selectionnees.remove((i, j))
                canvas.itemconfig(places[i][j], fill='#FF0000')


    canvas.bind('<Button-1>', onclick)

    root.mainloop()


if __name__ == '__main__':
    from lirexcel import lirexcel2

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





    dyna_ffichage(30, 6, 0, X.x, lirexcel2(scenario))