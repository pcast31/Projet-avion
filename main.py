from postprocessing import *
from dyna_ffichage import dyna_ffichage


# Instance
scenario = 7



if __name__ == '__main__':

    X_post,ind,ind_reduit,best_score,_,_=meilleure_sol_statique(scenario,30)
    (N,P,K)=X_post.shape
    nombre_choix=dyna_ffichage(N,P,K,X_post,ind)
