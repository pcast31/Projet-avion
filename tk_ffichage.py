import tkinter as tk
from PIL import Image, ImageTk
from matplotlib.pyplot import legend
from lirexcel import lirexcel
from random import *


def nombre2hexa(n):
    d = {0: '0', 1 : '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F'}

    a = n // 16
    b = n % 16

    return d[a] + d[b]


canvas = None
barycentre = None
shown = 'hidden'


def afficher_barycentre():
    global shown

    if shown == 'hidden':
        shown = 'normal'
    else:
        shown = 'hidden'
    canvas.itemconfigure(barycentre, state=shown)


def aff(tab, l, m):
    global canvas
    global barycentre

    print('Début affichage')

    # Correspondances
    lcorr = []
    for ind in l:
        if ind.transit not in lcorr:
            lcorr.append(ind.transit)
    # corr = {c: f'#{nombre2hexa(255 - c * 255 // max(lcorr))}FF{nombre2hexa(255 - c * 255 // max(lcorr))}' for c in lcorr}
    corr = {c: '#00FF00' if 0 < c <= 90 else '#FFFFFF' for c in lcorr}

    root = tk.Tk()
    root.title('Navion')

    canvas = tk.Canvas(root, width=1368, height=230)
    canvas.pack()

    bouton_barycentre = tk.Button(root, text='Barycentre', command=afficher_barycentre)
    bouton_barycentre.pack()

    img = ImageTk.PhotoImage(Image.open('navion.jpg'))
    canvas.create_image(0, 0, anchor=tk.NW, image=img)

    bar_x = 0
    bar_y = 0
    K=len(tab[0][0])
    for k in range(K):
        for i in range(len(tab)):
            for j in range(len(tab[0])):
                if tab[i,j,k]==1:
                    x = i * (30 + 13)
                    y = j * 30 + (j // 3) * 40
                    bar_x += x
                    bar_y += y
                    canvas.create_rectangle(x, y, x + 32, y + 30, fill=corr[l[k].transit])
                    canvas.create_text(x + 15, y + 15, text=str(l[k].idgroupe))

    barycentre = canvas.create_rectangle(bar_x / K - 3, bar_y / K - 3, bar_x / K + 3, bar_y / K + 3, fill='#FF0000')
    canvas.itemconfigure(barycentre, state=shown)


    root.mainloop()


etat_couleurs = 'base'

def new_aff(N, P, tab, ind, m):
    global etat_couleurs

    print('Début affichage')

    # Fenêtre
    root = tk.Tk()
    root.title('Navion')

    # Canvas
    canvas = tk.Canvas(root, width=N * 30 + (N + 1) * 10, height=290)
    canvas.pack()

    # Sol
    canvas.create_rectangle(0, 0, N * 30 + (N + 1) * 10, 290, fill='#3C3C4B', width=0)

    # Places
    places = [[None for j in range(P)] for i in range(N)]
    textes = [[None for j in range(P)] for i in range(N)]
    couleurs = [[None for j in range(P)] for i in range(N)]

    legendes = []

    for i in range(N):
        for j in range(P):
            if i == 11:
                couleurs[i][j] = '#E63232'
            
            elif i >= 9 or j == 1 or j == 4:
                couleurs[i][j] = '#465582'
            
            else:
                couleurs[i][j] = '#B9AFAA'
            
            x = 10 + i * (30 + 10)
            y = 10 + (j + j // 3) * (30 + 10)
            places[i][j] = canvas.create_rectangle(x, y, x + 30, y + 30, fill=couleurs[i][j], width=0)

    # Passagers
    x_barycentre = 0
    y_barycentre = 0
    poids_total = 0
    transits = []
    groupe_max = ind[-1].idgroupe
    K = len(ind)
    for k in range(K):
        for i in range(len(tab)):
            for j in range(len(tab[0])):
                if tab[i, j, k] == 1:
                    x = 10 + i * (30 + 10) + 15
                    y = 10 + (j + j // 3) * (30 + 10) + 15

                    if ind[k].categorie == 'R':
                        if j < 3:
                            canvas.delete(places[i - 1][j])
                            canvas.delete(places[i][j - 1])
                            canvas.delete(places[i - 1][j - 1])

                            canvas.coords(places[i][j], x - 15 - 10 - 30, y - 15 - 10 - 30, x + 15, y + 15)

                        else:
                            canvas.delete(places[i - 1][j])
                            canvas.delete(places[i][j + 1])
                            canvas.delete(places[i - 1][j + 1])

                            canvas.coords(places[i][j], x - 15 - 10 - 30, y - 15, x + 15, y + 15 + 10 + 30)

                    elif ind[k].categorie == 'B':
                        if j < 3:
                            canvas.delete(places[i - 1][j])
                            canvas.delete(places[i - 2][j])
                            canvas.delete(places[i - 3][j])
                            canvas.delete(places[i][j - 1])
                            canvas.delete(places[i - 1][j - 1])
                            canvas.delete(places[i - 2][j - 1])
                            canvas.delete(places[i - 3][j - 1])
                            canvas.delete(places[i][j - 2])
                            canvas.delete(places[i - 1][j - 2])
                            canvas.delete(places[i - 2][j - 2])
                            canvas.delete(places[i - 3][j - 2])

                            canvas.coords(places[i][j], x - 15 - 3 * (10 + 30), y - 15 - 2 * (10 + 30), x + 15, y + 15)

                        else:
                            canvas.delete(places[i - 1][j])
                            canvas.delete(places[i - 2][j])
                            canvas.delete(places[i - 3][j])
                            canvas.delete(places[i][j + 1])
                            canvas.delete(places[i - 1][j + 1])
                            canvas.delete(places[i - 2][j + 1])
                            canvas.delete(places[i - 3][j + 1])
                            canvas.delete(places[i][j + 2])
                            canvas.delete(places[i - 1][j + 2])
                            canvas.delete(places[i - 2][j + 2])
                            canvas.delete(places[i - 3][j + 2])

                            canvas.coords(places[i][j], x - 15 - 3 * (10 + 30), y - 15, x + 15, y + 15 + 2 * (10 + 30))

                    x_barycentre += x * ind[k].masse
                    y_barycentre += y * ind[k].masse
                    poids_total += ind[k].masse
                    textes[i][j] = canvas.create_text(x, y, text=str(ind[k].idgroupe), fill='#FFFFFF')

                    if ind[k].transit > 0 and ind[k].transit not in transits:
                        transits.append(ind[k].transit)
    x_barycentre = x_barycentre / poids_total
    y_barycentre = y_barycentre / poids_total
    transits.sort()


    # Barycentre
    if N == 30:
        zone_barycentre = canvas.create_rectangle(10 + 13 * (30 + 10), 3 * (30 + 10), 10 + 17 * (30 + 10) + 30, 10 + 4 * (30 + 10), outline='#FF0000', width=2)
    else:
        zone_barycentre = canvas.create_rectangle(10 + 16.5 * (30 + 10), 3 * (30 + 10), 10 + 20.5 * (30 + 10) + 30, 10 + 4 * (30 + 10), outline='#FF0000', width=2)
    barycentre = canvas.create_rectangle(x_barycentre - 5, y_barycentre - 5, x_barycentre + 5, y_barycentre + 5, fill='#00FF00', width=0)
    canvas.itemconfig(zone_barycentre, state='hidden')
    canvas.itemconfig(barycentre, state='hidden')


    def barycentre_command():
        state = canvas.itemcget(zone_barycentre, 'state')
        if state == 'hidden':
            canvas.itemconfig(zone_barycentre, state='normal')
            canvas.itemconfig(barycentre, state='normal')
        else:
            canvas.itemconfig(zone_barycentre, state='hidden')
            canvas.itemconfig(barycentre, state='hidden')


    barycentre_bouton = tk.Button(root, text='Barycentre', command=barycentre_command)
    barycentre_bouton.pack()


    # Places occupées
    def places_occupees_command():
        global etat_couleurs

        for k in range(K):
            for i in range(len(tab)):
                for j in range(len(tab[0])):
                    if tab[i, j, k] == 1:
                        if etat_couleurs == 'occupees':
                            canvas.itemconfig(places[i][j], fill=couleurs[i][j])
                        else:
                            canvas.itemconfig(places[i][j], fill='#00A000')

        for legende in legendes:
                canvas.delete(legende)

        if etat_couleurs == 'occupees':
            etat_couleurs = 'base'
        else:
            etat_couleurs = 'occupees'

            legendes.append(canvas.create_rectangle(10, 130, 10 + 30, 130 + 30, fill='#00A000', width=0))
            legendes.append(canvas.create_text(100, 145, text='Place occupée', fill="#FFFFFF"))

    places_occupees_bouton = tk.Button(root, text='Places occupées', command=places_occupees_command)
    places_occupees_bouton.pack()

    ######################################

    # Pour colorer les groupes de différentes couleurs

    def gencolor():
        L_id_grp = []
        for k in range(K):
            if not (ind[k].idgroupe in L_id_grp):
                L_id_grp.append(ind[k].idgroupe)
        L_color = []
        rndHex = '0123456789ABCDEF'
        for g in range(len(L_id_grp)):
            hexChar = ''
            for i in range(6):
                hexChar = hexChar+str(rndHex[randint(0, 15)])
            L_color.append(str(hexChar))
        return(L_color)

    # Affichage de tous les groupes
    def all_groupes_command():
        global etat_couleurs

        L = gencolor()

        for k in range(K):
            for i in range(len(tab)):
                for j in range(len(tab[0])):
                    if tab[i, j, k] == 1:
                        if etat_couleurs == 'groupes_couleur':
                            canvas.itemconfig(places[i][j], fill=couleurs[i][j])
                        else:
                            if len(ind[k].groupe) > 0:
                                canvas.itemconfig(places[i][j], fill='#'+str(L[ind[k].idgroupe - 1]))
                            else:
                                canvas.itemconfig(places[i][j], fill='#00008b')

        for legende in legendes:
            canvas.delete(legende)

        if etat_couleurs == 'groupes_couleur':
            etat_couleurs = 'base'
        else:
            etat_couleurs = 'groupes_couleur'

            # legendes.append(canvas.create_rectangle(
            #    10, 130, 10 + 30, 130 + 30, fill='#00A000', width=0))
            # legendes.append(canvas.create_text(100, 145, text='Place occupée', fill="#FFFFFF"))

    all_groupes_bouton = tk.Button(root, text='Tous les groupes', command=all_groupes_command)
    all_groupes_bouton.pack()

    ######################################

    # Catégories de passagers
    def categories_command():
        global etat_couleurs

        for k in range(K):
            for i in range(len(tab)):
                for j in range(len(tab[0])):
                    if tab[i, j, k] == 1:
                        if etat_couleurs == 'categories':
                            canvas.itemconfig(places[i][j], fill=couleurs[i][j])
                        elif ind[k].categorie == 'H':
                            canvas.itemconfig(places[i][j], fill='#0095FF')
                        elif ind[k].categorie == 'F':
                            canvas.itemconfig(places[i][j], fill='#c800FF')
                        elif ind[k].categorie == 'R':
                            canvas.itemconfig(places[i][j], fill='#00A000')
                        elif ind[k].categorie == 'B':
                            canvas.itemconfig(places[i][j], fill='#A0A000')
                        else:
                            canvas.itemconfig(places[i][j], fill='#FF7F00')
                            
        for legende in legendes:
                canvas.delete(legende)

        if etat_couleurs == 'categories':
            etat_couleurs = 'base'
        else:
            etat_couleurs = 'categories'

            legendes.append(canvas.create_rectangle(10, 130, 10 + 30, 130 + 30, fill='#0095FF', width=0))
            legendes.append(canvas.create_text(80, 145, text='Homme', fill="#FFFFFF"))

            legendes.append(canvas.create_rectangle(120, 130, 120 + 30, 130 + 30, fill="#c800FF", width=0))
            legendes.append(canvas.create_text(190, 145, text='Femme', fill="#FFFFFF"))

            legendes.append(canvas.create_rectangle(230, 130, 230 + 30, 130 + 30, fill="#FF7F00", width=0))
            legendes.append(canvas.create_text(300, 145, text="Enfant", fill="#FFFFFF"))

            legendes.append(canvas.create_rectangle(340, 130, 340 + 30, 130 + 30, fill="#00A000", width=0))
            legendes.append(canvas.create_text(410, 145, text="Chaise roulante", fill="#FFFFFF"))

            legendes.append(canvas.create_rectangle(450, 130, 450 + 30, 130 + 30, fill="#A0A000", width=0))
            legendes.append(canvas.create_text(520, 145, text="Civière", fill="#FFFFFF"))

    categories_bouton = tk.Button(root, text='Catégories de personnes', command=categories_command)
    categories_bouton.pack()

    # Transit
    def transit_command():
        global etat_couleurs

        for k in range(K):
            for i in range(len(tab)):
                for j in range(len(tab[0])):
                    if tab[i, j, k] == 1:
                        if etat_couleurs == 'transit':
                            canvas.itemconfig(places[i][j], fill=couleurs[i][j])
                        elif ind[k].transit == 0 or ind[k].transit > 90:
                            canvas.itemconfig(places[i][j], fill='#000000')
                        else :
                            canvas.itemconfig(places[i][j], fill='#00A000')

        for legende in legendes:
            canvas.delete(legende)

        if etat_couleurs == 'transit':
            etat_couleurs = 'base'
        else:
            etat_couleurs = 'transit'

            legendes.append(canvas.create_rectangle(10, 130, 10 + 30, 130 + 30, fill='#00A000', width=0))
            legendes.append(canvas.create_text(130, 145, text='Transit inférieur à 90 minutes', fill="#FFFFFF"))

    transit_bouton = tk.Button(root, text='Transit', command=transit_command)
    transit_bouton.pack()

    # Billets
    def billets_command():
        global etat_couleurs

        for k in range(K):
            for i in range(len(tab)):
                for j in range(len(tab[0])):
                    if tab[i, j, k] == 1:
                        if etat_couleurs == 'billets':
                            canvas.itemconfig(places[i][j], fill=couleurs[i][j])
                        elif ind[k].classe == 0:
                            canvas.itemconfig(places[i][j], fill='#0095FF')
                        else:
                            canvas.itemconfig(places[i][j], fill='#FF00FF')
        
        for legende in legendes:
            canvas.delete(legende)

        if etat_couleurs == 'billets':
            etat_couleurs = 'base'
        else:
            etat_couleurs = 'billets'

            legendes.append(canvas.create_rectangle(10, 130, 10 + 30, 130 + 30, fill='#FF00FF', width=0))
            legendes.append(canvas.create_text(100, 145, text='Billet business', fill="#FFFFFF"))

            legendes.append(canvas.create_rectangle(160, 130, 160 + 30, 130 + 30, fill='#0095FF', width=0))
            legendes.append(canvas.create_text(250, 145, text='Billet standard', fill="#FFFFFF"))


    
    billets_bouton = tk.Button(root, text='Billets', command=billets_command)
    billets_bouton.pack()

    # Groupes
    def groupes_command():
        global etat_couleurs
        etat_couleurs = 'groupes'

        for k in range(K):
            for i in range(len(tab)):
                for j in range(len(tab[0])):
                    if tab[i, j, k] == 1:
                        if ind[k].idgroupe == int(groupes_spinbox.get()):
                            canvas.itemconfig(places[i][j], fill='#00A000')
                        else:
                            canvas.itemconfig(places[i][j], fill='#000000')
        
        for legende in legendes:
            canvas.delete(legende)

        legendes.append(canvas.create_rectangle(10, 130, 10 + 30, 130 + 30, fill='#00A000', width=0))
        legendes.append(canvas.create_text(110, 145, text=f'Membre du groupe {int(groupes_spinbox.get())}', fill="#FFFFFF"))


    groupes_spinbox = tk.Spinbox(root, from_=1, to=groupe_max, command=groupes_command)
    groupes_spinbox.pack()

    # Main loop
    root.mainloop()