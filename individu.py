dic_masse={'H':85,'F':70,'E':35,'R':85,'B':85}

class Individu:

    def __init__(self,i,cat,t, idgroupe, classe):
        self.id=i
        self.categorie=cat
        self.idgroupe = idgroupe
        self.groupe=[]
        self.masse=dic_masse[cat]
        self.transit=t
        self.classe=classe

    def ajout_au_groupe(self,ind):
        self.groupe.append(ind)



