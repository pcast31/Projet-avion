import tkinter as tk
from PIL import Image, ImageTk
from lirexcel import lirexcel


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

def new_aff(tab, ind, m):
    global etat_couleurs

    print('Début affichage')

    # Fenêtre
    root = tk.Tk()
    root.title('Navion')

    # Canvas
    canvas = tk.Canvas(root, width=1130, height=290)
    canvas.pack()

    # Sol
    canvas.create_rectangle(0, 0, 1130, 290, fill='#3C3C4B', width=0)

    # Places
    places = [[None for j in range(6)] for i in range(28)]
    textes = [[None for j in range(6)] for i in range(28)]
    couleurs = [[None for j in range(6)] for i in range(28)]

    for i in range(28):
        for j in range(6):
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
    transits = []
    K = len(ind)
    for k in range(K):
        for i in range(len(tab)):
            for j in range(len(tab[0])):
                if tab[i, j, k] == 1:
                    x = 10 + i * (30 + 10) + 15
                    y = 10 + (j + j // 3) * (30 + 10) + 15
                    x_barycentre += x
                    y_barycentre += y
                    textes[i][j] = canvas.create_text(x, y, text=str(ind[k].idgroupe), fill='#FFFFFF')
                    if ind[k].transit > 0 and ind[k].transit not in transits:
                        transits.append(ind[k].transit)
    x_barycentre = x_barycentre / K
    y_barycentre = y_barycentre / K
    transits.sort()


    # Barycentre
    zone_barycentre = canvas.create_rectangle(10 + 12 * (30 + 10), 3 * (30 + 10), 10 + 16 * (30 + 10) + 30, 10 + 4 * (30 + 10), outline='#FF0000', width=2)
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
        if etat_couleurs == 'occupees':
            etat_couleurs = 'base'
        else:
            etat_couleurs = 'occupees'

    places_occupees_bouton = tk.Button(root, text='Places occupées', command=places_occupees_command)
    places_occupees_bouton.pack()

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
                        else:
                            canvas.itemconfig(places[i][j], fill='#FF7F00')
        if etat_couleurs == 'categories':
            etat_couleurs = 'base'
        else:
            etat_couleurs = 'categories'

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
        if etat_couleurs == 'transit':
            etat_couleurs = 'base'
        else:
            etat_couleurs = 'transit'

    transit_bouton = tk.Button(root, text='Transit', command=transit_command)
    transit_bouton.pack()

    # Main loop
    root.mainloop()