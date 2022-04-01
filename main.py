from postprocessing import *
from dyna_ffichage import dyna_ffichage
import matplotlib.pyplot as plt

# Instance
scenario = 5



if __name__ == '__main__':
    # Renseigner le scénario, le temps maximal pour Gurobi, et les choix désirés pour le traitement des groupes.
    X_post,ind,ind_reduit,best_score,a_best,b_best = meilleure_sol_statique(scenario, 60)
    (N,P,K)=X_post.shape

    # Affichage de la solution statique
    new_aff(N, P, X_post, ind)
    print(f"Le placement des groupes est bon à {best_score}. On l'obtient pour {a_best, b_best}")

    # Version dynamique
    nombre_choix=dyna_ffichage(N,P,K,X_post,ind,scenario)

    # Permet d'afficher les nombres de choix. Attention, ne fonctionne que pour les premières instances
    #x = [k for k in range(K)]
    #y = [nombre_choix[k] for k in range(K)]
    # plt.plot(x,y)
    # plt.show()