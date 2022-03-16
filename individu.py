dic_masse={'H':85,'F':70,'E':35,'R':85,'B':85}
dic_age={'H':2,'F':2,'E':-1,'R':2,'B':2}

class Individu:

    def __init__(self,i,cat,t, idgroupe, classe):
        self.id=i
        self.categorie=cat
        self.idgroupe = idgroupe
        self.groupe=[]
        self.masse=dic_masse[cat]
        self.transit=t
        self.classe=classe
        self.age=dic_age[cat]

    def ajout_au_groupe(self,ind):
        self.groupe.append(ind)

def nb_groupes(ind):
    lst = [0,0,0]
    for e in ind:
        if len(e.groupe) == 0:
            lst[0] += 1
        elif len(e.groupe) == 1:
            lst[1] += 1
        elif len(e.groupe) == 2:
            lst[2] += 1
    return [lst[0],lst[1]/2,lst[2]/3]


