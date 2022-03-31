from postprocessing import *
from dyna_ffichage import dyna_ffichage
import matplotlib.pyplot as plt

# Instance
scenario = 0



if __name__ == '__main__':

    X_post,ind,ind_reduit,best_score,_,_=meilleure_sol_statique(scenario,20, [0], [1])
    (N,P,K)=X_post.shape
    nombre_choix=dyna_ffichage(N,P,K,X_post,ind)
    x = [k for k in range(K)]
    y = nombre_choix
    plt.plot(x,y)
    plt.show()