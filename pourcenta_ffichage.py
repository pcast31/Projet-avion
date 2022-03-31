import sys
from io import StringIO
import tkinter as tk
import tkinter.ttk as ttk
import re
import threading
from initialisation import initialise
from gurobipy import *
import numpy as np
from contraintes import *
from objectif import *
from lirexcel import lirexcel, lirexcel2, reduction
from affichage import affiche_texte, affiche_avion
from tk_ffichage import new_aff

def main():
    # Dimensions de l'avion
    N = 30
    P = 6
    # Instance
    scenario = 5

    m=Model()
    ind=lirexcel2(scenario)
    ind_reduit= reduction(scenario, ind) # Scinde les groupes de 4 et plus en petits groupes
    K=len(ind)
    X=initialise(m,N,P,K)
    m.update()
    barycentre(m,X,ind_reduit,N,P,K)
    unicite_personne(m,X,N,P,K)
    unicite_siege(m,X,N,P,K)
    chef_de_groupe(m, X, ind_reduit)
    enfant_issue_secours(m, X, ind_reduit)
    #symetrie(m,X,ind,N,P,K)
    chaises_roulantes(m, X, ind_reduit)
    civieres(m, X, ind_reduit)
    nenfants(m,X,ind_reduit)
    taille=lutte_des_classes(m,X,ind_reduit)
    fct_objectif(m, X, ind_reduit, [0,0,2]) # Ici, on néglige les couples. Voir postprocessing
    m.update()
    m.optimize()



    affiche_texte(X.x,ind,m)
    affiche_avion(X.x,ind,m)
    #print(taille2.x)

    return N, P, X, ind, m

N = None
P = None
X = None
ind = None
m = None
t = None
f = None

root = tk.Tk()
root.title('Navion')
root.iconbitmap('data/navion.ico')

lab = tk.Label(root, text='༼ つ -_- ༽つ')
lab.pack()

bar = ttk.Progressbar(root, length=300)
bar.pack()

def lezgongue_command():
    global t

    lezgongue['state'] = 'disabled'

    bar['value'] = 100
    lab['text'] = '༼ つ ◕_◕ ༽つ'

    base_stdout = sys.stdout

    class GroubiIO(StringIO):
        def __init__(self):
            super(GroubiIO, self).__init__()

        def write(self, s):
            global f
            if '%' in s and f != 0:
                m = re.search(r'-?\d*\.?\d+(?=%)', s)
                lf = abs(float(m.group(0)))
                bar['value'] = lf
                lab['text'] = '༼ つ >_< ༽つ'

                
                m = re.search(r'-?\d*\.?\d+(?=\s+-?\d*\.?\d+\s+-?\d*\.?\d+%)', s)
                if m is not None:
                    score['text'] = f'Score : {float(m.group(0))}'

                f = lf
            
            base_stdout.write(s)


    def tf():
        global N
        global P
        global X
        global ind
        global m

        output = GroubiIO()
        sys.stdout = output

        (N, P, X, ind, m) = main()

        sys.stdout = base_stdout

    t = threading.Thread(target=tf)
    t.start()

lezgongue = tk.Button(root, text='Lezgongue', command=lezgongue_command)
lezgongue.pack()

score = tk.Label(root, text='Score : 0')
score.pack()

def task():
    global f
    global t

    if f == 0:
        t.join()
        root.destroy()
    else:
        root.after(1, task)

root.after(1, task)
root.mainloop()

new_aff(N, P, X.x, ind, m)