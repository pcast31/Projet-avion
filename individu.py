dic_masse={'M':85,'F':70,'E':35}

class Individu:

    def __init__(self,i,cat,t):
        self.id=i
        self.group=[]
        self.categorie=cat
        self.masse=dic_masse[cat]
        self.transit=t

    def ajout_au_groupe(self,ind):
        self.group.append(ind)



