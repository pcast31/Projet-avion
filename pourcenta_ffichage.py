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
import time
from postprocessing import *
from dyna_ffichage import dyna_ffichage

scenario = 5

def main():
    # Dimensions de l'avion
    N = 30
    P = 6
    # Instance
    scenario = 7

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

def main2():
    global N
    global P
    global K
    global X
    global ind

    
    X_post,ind,ind_reduit,best_score,_,_=meilleure_sol_statique(scenario,60, [0], [0])
    (N,P,K)=X_post.shape
    X = X_post

N = None
P = None
K = None
X = None
ind = None
m = None
t = None
f = None
b = False
start = None

root = tk.Tk()
root.title('Groubi dodo')
root.iconbitmap('data/navion.ico')


lab = tk.Label(root, text='༼ つ -_- ༽つ')
lab.config(font=('Helvetica bold', 20))
lab.pack()

bar = ttk.Progressbar(root, length=300)
bar.pack()

def lezgongue_command():
    global t

    lezgongue['state'] = 'disabled'

    bar['value'] = 100
    lab['text'] = '༼ つ ◕_◕ ༽つ'
    root.title('Groubi se réveille')

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
                root.title(f'Groubi travaille : {lf}%')

                
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

        main2()

        sys.stdout = base_stdout

    t = threading.Thread(target=tf)
    t.start()

lezgongue = tk.Button(root, text='Lancer Groubi', command=lezgongue_command)
lezgongue.config(font=('Helvetica bold', 20))
lezgongue.pack()

score = tk.Label(root, text='Score : 0')
score.config(font=('Helvetica bold', 20))
score.pack()

def task():
    global f
    global t
    global b
    global start

    if not b and f == 0:
        t.join()
        b = True
        start = time.time()
        lab['text'] = '༼ つ ◕◡◕ ༽つ'
        root.title('Groubi content')

    if b and (time.time() - start) > 1:
        root.destroy()
    
    root.after(1, task)

root.after(1, task)
root.mainloop()

#new_aff(N, P, X, ind)

nombre_choix=dyna_ffichage(N,P,K,X,ind,scenario)