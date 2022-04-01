import tkinter as tk
from random import randrange,choice
from initialisation import initialise
from gurobipy import *
import numpy as np
from contraintes import *
from objectif import *
from lirexcel import lirexcel, lirexcel2, reduction
from affichage import affiche_texte, affiche_avion
from tk_ffichage import new_aff
from postprocessing import post_traitement,dimension
from comparaison import verif_enfants,barycentre2

N = 30
P = 6
scenario = 5



def dyna_ffichage(N, P,K,tab,vrai_ind):
    choix_ind={}
    X_nouveau=[[[0 for k in range(K)]for j in range(P)]for i in range(N)]
    groupes={}
    ind=reduction(scenario, vrai_ind)
    groupe_compteur=1
    for indiv in ind:
        if indiv.idgroupe not in groupes:
            groupes[indiv.idgroupe]=[indiv]
        else :
            groupes[indiv.idgroupe].append(indiv)

    place_ind={}
    for i in range(N):
        for j in range(P):
            if sum([(k+1)*tab[i][j][k] for k in range(K)])>0:
                place_ind[sum([k*tab[i][j][k] for k in range(K)])]=(i,j)
    places_associes={}
    for k in range(K):
            places_associes[place_ind[k]]=list(set([place_ind[l.id] for l in ind[k].groupe]))

    issue_de_secours=list(set([sum([individu.idgroupe*tab[11,j,individu.id] for individu in ind]) for j in range(6) if sum([individu.idgroupe*tab[11,j,individu.id] for individu in ind])>0]))
    nombre_groupe_secours=[sum([1 for gr in issue_de_secours if len(groupes[gr])==card])for card in range(0,4)]

    def enfant(groupe):
        for ind in groupe:
            if ind.categorie=='E':
                return True
        return False

    def dernier_groupe_adulte(g,nb):
        if nb==0:
            return False
        for gr in groupes:
            if gr>g and len(groupes[g])==len(groupes[gr]) and not(enfant(groupes[gr])):
                if nb==1:
                    return False
                else:
                    return dernier_groupe_adulte(gr,nb-1)
        return True


    def calculer(g):
        places = []
        places_enfants = []
        if 'R' in [individu.categorie for individu in groupes[g]] or 'B' in [individu.categorie for individu in groupes[g]]:
            return [[place_ind[individu.id] for individu in groupes[g]]]
        
        for gr in groupes:
            if groupes[gr][0].classe==groupes[g][0].classe and len(groupes[gr])==len(groupes[g]) and groupes[g][0].classe==groupes[gr][0].classe and 'R' not in [individu.categorie for individu in groupes[gr]] and 'B' not in [individu.categorie for individu in groupes[gr]]:
                positions=[place_ind[individu.id] for individu in groupes[gr]]
                if sum([sum([k*X_nouveau[i][j][k] for i,j in positions])for k in range(K)])==0:
                    places.append(positions)
                    if sum([i==11 for (i,j) in positions])==0:
                        places_enfants.append(positions)
        if enfant(groupes[g]):
            return places_enfants
        elif not(dernier_groupe_adulte(g,nombre_groupe_secours[len(groupes[g])])):
            return places
        else:
            return [p for p in places if sum([i==11 for (i,j) in p])>0]
    root = tk.Tk()
    root.title('Navion')
    root.iconbitmap('data/navion.ico')

    canvas = tk.Canvas(root, width=30 * N + 10 * (N + 1), height=30 * (P + 1) + 10 * (P + 2))
    canvas.pack()

    canvas.create_rectangle(0, 0, 30 * N + 10 * (N + 1), 30 * (P + 1) + 10 * (P + 2), fill='#3C3C4B')

    places = [[canvas.create_rectangle(10 + i * 40, 10 + (j + j // 3) * 40, 10 + i * 40 + 30, 10 + (j + j // 3) * 40 + 30, width=0, fill='#465582') for j in range(P)] for i in range(N)]

    #tailles_groupes = [0] * ind[-1].idgroupe#non continuite groupe
    #ind_repr=[0]*ind[-1].idgroupe
    #for i in ind:
    #    tailles_groupes[i.idgroupe - 1] = len(i.groupe) + 1
    #    ind_repr[i.idgroupe-1]=i

    places_proposees = calculer(1)#changer liste de liste
    possibilite=[]
    for sous_groupe in places_proposees:
        for i,j in sous_groupe:
            canvas.itemconfig(places[i][j], fill='#FF0000')
            possibilite.append((i,j))

    groupe_compteur = 1



    def aleatoire_command():
        nonlocal possibilite
        nonlocal places_proposees
        nonlocal X_nouveau
        nonlocal groupe_compteur
        nonlocal places_rempli  

        (i,j)=choice(possibilite)
        places_prises=[(i,j)]+places_associes[(i,j)]
        places_rempli=places_rempli+places_prises
        secours=0 
        if 'R' in [individu.categorie for individu in groupes[groupe_compteur]] or 'B' in [individu.categorie for individu in groupes[groupe_compteur]]:
            for individu in groupes[groupe_compteur]:
                choix_ind[individu]=len(possibilite)
                for i in range(N):
                    for j in range(P):
                        X_nouveau[i][j][individu.id]=tab[i][j][individu.id]
        else:
            for id in range(len(places_prises)):
                choix_ind[groupes[groupe_compteur][id].id]=len(possibilite)
                i2,j2=places_prises[id]
                if i2==11 and secours==0:
                    secours+=1
                    nombre_groupe_secours[len(groupes[groupe_compteur])]=nombre_groupe_secours[len(groupes[groupe_compteur])]-1
                canvas.itemconfig(places[i2][j2], fill='#00FF00')
                X_nouveau[i2][j2][groupes[groupe_compteur][id].id]=1
        groupe_compteur+=1
        while groupe_compteur not in groupes and groupe_compteur<50000:
            groupe_compteur+=1


        if groupe_compteur>=40000:
            root.destroy()
            new_aff(N,P,np.array(X_nouveau),vrai_ind)
            print(barycentre2(np.array(X_nouveau),vrai_ind))
            verif_enfants(np.array(X_nouveau),vrai_ind)
            return choix_ind
        else:
            groupe_label['text'] ='Groupe ' +str(groupe_compteur)+' comprenant '+str(len(groupes[groupe_compteur]))+ ' personnes'


        places_proposees = calculer(groupe_compteur)
        possibilite=[]
        for sous_groupe in places_proposees:
            for i3,j3 in sous_groupe:
                if (i3,j3) not in places_rempli:
                    canvas.itemconfig(places[i3][j3], fill='#FF0000')
                    possibilite.append((i3,j3))
        for i4 in range(N):
            for j4 in range(P):
                if (i4, j4) in possibilite:
                    canvas.itemconfig(places[i4][j4], fill='#FF0000')
                elif (i4, j4) in places_rempli:
                    canvas.itemconfig(places[i4][j4], fill='#00FF00')                                
                else:
                    canvas.itemconfig(places[i4][j4], fill='#465582')




    aleatoire_button = tk.Button(root, text='Choix aléatoire', command=aleatoire_command)
    aleatoire_button.pack()

    
    def opti_command():
        root.destroy()
        nonlocal groupe_compteur
        nonlocal X_nouveau
        m2=Model()
        X_opti=initialise(m2,N,P,K)
        m2.update()
        barycentre(m2,X_opti,ind,N,P,K)
        unicite_personne(m2,X_opti,N,P,K)
        unicite_siege(m2,X_opti,N,P,K)
        chef_de_groupe(m2, X_opti, ind)
        #symetrie(m,X,ind,N,P,K)
        for i in range(N):
            for j in range(P):
                for k in range(K):
                    m2.addConstr(X_opti[i,j,k]>=X_nouveau[i][j][k])
        chaises_roulantes(m2, X_opti, ind)
        civieres(m2, X_opti, ind)
        nenfants(m2,X_opti,ind)
        taille=lutte_des_classes(m2,X_opti,ind)
        fct_objectif(m2, X_opti, ind, [0,2,2])
        m2.update()
        m2.optimize()


        post_traitement(m2, X_opti, ind, [False, False, False])
        m2.setObjective(bonus_groupe3(m2, X_opti, ind, [True, True]), GRB.MINIMIZE) # bonus_groupe3 quadratique
        m2.update()
        m2.optimize()
        new_aff(N,P,X_opti.x,vrai_ind)

    

    opti_button = tk.Button(root, text='Choix optimal', command=opti_command)
    opti_button.pack()


    places_rempli = []


    groupe_label = tk.Label(root, text='Groupe ' +str(groupe_compteur)+' comprenant '+str(len(groupes[groupe_compteur]))+ ' personnes')
    groupe_label.pack()





    def onclick(event):
            nonlocal possibilite
            nonlocal places_proposees
            nonlocal X_nouveau
            nonlocal groupe_compteur
            nonlocal places_rempli



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
                if (i, j) in possibilite:
                    places_prises=[(i,j)]+places_associes[(i,j)]
                    places_rempli=places_rempli+places_prises
                    secours=0
                    if 'R' in [individu.categorie for individu in groupes[groupe_compteur]] or 'B' in [individu.categorie for individu in groupes[groupe_compteur]]:
                        for individu in groupes[groupe_compteur]:
                            choix_ind[individu]=len(possibilite)
                            for i in range(N):
                                for j in range(P):
                                    X_nouveau[i][j][individu.id]=tab[i][j][individu.id]
                    else:

                        for id in range(len(places_prises)):
                            choix_ind[groupes[groupe_compteur][id].id]=len(possibilite)
                            i2,j2=places_prises[id]
                            if i2==11 and secours==0:
                                secours+=1
                                nombre_groupe_secours[len(groupes[groupe_compteur])]=nombre_groupe_secours[len(groupes[groupe_compteur])]-1
                            canvas.itemconfig(places[i2][j2], fill='#00FF00')
                            X_nouveau[i2][j2][groupes[groupe_compteur][id].id]=1
                    groupe_compteur+=1
                    while groupe_compteur not in groupes and groupe_compteur<50000:
                        groupe_compteur+=1


                    if groupe_compteur>=40000:
                        root.destroy()
                        new_aff(N,P,np.array(X_nouveau),vrai_ind)
                        verif_enfants(np.array(X_nouveau),vrai_ind)
                        print(barycentre2(np.array(X_nouveau),vrai_ind))
                        return choix_ind
                    else:
                        groupe_label['text'] ='Groupe ' +str(groupe_compteur)+' comprenant '+str(len(groupes[groupe_compteur]))+ ' personne' + ('s' if len(groupes[groupe_compteur]) > 1 else '')

                        for k in groupes[groupe_compteur]:
                            if k.categorie == 'B':
                                groupe_label['text'] += '(B)'
                                break

                        for k in groupes[groupe_compteur]:
                            if k.categorie == 'R':
                                groupe_label['text'] += '(R)'
                                break

                        for k in groupes[groupe_compteur]:
                            if 0 < k.transit <= 90:
                                groupe_label['text'] += '(t)'
                                break

                        for k in groupes[groupe_compteur]:
                            if k.classe == 1:
                                groupe_label['text'] += '(b)'
                                break




                    places_proposees = calculer(groupe_compteur)
                    possibilite=[]
                    for sous_groupe in places_proposees:
                        for i3,j3 in sous_groupe:
                            if (i3,j3) not in places_rempli:
                                canvas.itemconfig(places[i3][j3], fill='#FF0000')
                                possibilite.append((i3,j3))
                    for i4 in range(N):
                        for j4 in range(P):
                            if (i4, j4) in possibilite:
                                canvas.itemconfig(places[i4][j4], fill='#FF0000')
                            elif (i4, j4) in places_rempli:
                                canvas.itemconfig(places[i4][j4], fill='#00FF00')                                
                            else:
                                canvas.itemconfig(places[i4][j4], fill='#465582')


    def entree(event):
 
            i = -1
            j = -1

            if not(event.x % 40 <= 10):

                i = event.x // 40

            if not(event.y % 40 <= 10 or 120 <= event.y <= 170):

                j = event.y // 40
                if j >= 3:
                    j -= 1
            
            if i>=0 and j>=0 and (i,j) in places_associes.keys():
                places_prises=[(i,j)]+places_associes[(i,j)]
                for i2 in range(N):
                    for j2 in range(P):
                        if (i2,j2) in places_prises and (i2,j2) in possibilite:
                            for (i3,j3) in places_prises:
                                canvas.itemconfig(places[i3][j3], fill='#0000FF')
            
                        elif (i2, j2) in possibilite:
                            canvas.itemconfig(places[i2][j2], fill='#FF0000')
                        elif (i2, j2) in places_rempli:
                            canvas.itemconfig(places[i2][j2], fill='#00FF00')                                
                        else:
                            canvas.itemconfig(places[i2][j2], fill='#465582')


    canvas.bind('<Button-1>', onclick)
    canvas.bind('<Motion>',entree)

    root.mainloop()


if __name__ == '__main__':
    from lirexcel import lirexcel2

    m=Model()
    ind=lirexcel2(scenario)
    ind_reduit=reduction(scenario, ind)
    K=len(ind)
    X=initialise(m,N,P,K)
    m.update()
    barycentre_restreint(m,X,ind_reduit,N,P,K)
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
    tab=X.x


    post_traitement(m, X, ind_reduit, [False, False, False])
    m.setObjective(bonus_groupe3(m, X, ind_reduit, [True, True]), GRB.MINIMIZE) # bonus_groupe3 quadratique
    m.update()
    m.optimize()
    dyna_ffichage(30, 6, K, X.x, ind)