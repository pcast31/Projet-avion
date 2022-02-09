dic_masse={'H':85,'F':70,'E':35}

class Individu:

    def __init__(self,i,cat,t):
        self.id=i
        self.categorie=cat
        self.groupe=[]
        self.masse=dic_masse[cat]
        self.transit=t

    def ajout_au_groupe(self,ind):
        self.groupe.append(ind)



