   
   
   
   
def affiche_texte(tab,ind):
    bar_x=0
    bar_y=0
    K=len(tab[0][0])
    for k in range(K):
        for i in range(len(tab)):
            for j in range(len(tab[0])):
                if tab[i,j,k]==1:
                    bar_x+=i
                    bar_y+=j
                    print("L'individu ",k,"en groupe avec",[indiv.id for indiv in ind[k].groupe],"est à la place",i,j)
    print("barycentre en ligne:" ,bar_x/K,"barycentre en rangée:",bar_y/K)