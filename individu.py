dic_masse={'H':85,'F':70,'E':35,'R':85,'B':85}
dic_age={'H':2,'F':2,'E':-1,'R':2,'B':2}

class Individu:

    def __init__(self,i,cat,t, idgroupe, classe):
        self.id=i # numéro de l'individu
        self.categorie=cat # homme, femme, enfant, mobilité réduite
        self.idgroupe = idgroupe # numéro du groupe
        self.groupe=[] # camarades de groupe
        self.masse=dic_masse[cat] # masse
        self.transit=t # temps de transit
        self.classe=classe # buisness ou non            
        self.age=dic_age[cat] # âge, -1 pour un enfant et +2 pour un adulte

    def ajout_au_groupe(self,ind):
        self.groupe.append(ind)

def nb_groupes(ind):
    """
    Compte le nombre de groupe de taille 1,2 et 3. 
    """
    lst = [0,0,0]
    K = len(ind)
    lien = [[] for _ in range(K)]
    for k in range(K):
        for l in range(K):
            if ind[l] in ind[k].groupe:
                lien[k].append(l)
    for k in range(K):
        if len(lien[k]) == 0:
            lst[0] += 1
        elif len(lien[k]) == 1:
            lst[1] += 1
        elif len(lien[k]) == 2:
            lst[2] += 1
    return [lst[0],lst[1]/2,lst[2]/3]