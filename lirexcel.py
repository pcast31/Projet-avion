import pandas as pd
from individu import Individu


def lirexcel(scenario, chemin='DataSeating.xlsx'):
    df = pd.read_excel(chemin, sheet_name=scenario)
    df = df.drop(df.tail(2).index)
    df = df.fillna(0)
    df['Numéro du groupe'] = df['Numéro du groupe'].apply(lambda x: int(x))
    df['Femmes'] = df['Femmes'].apply(lambda x: int(x))
    df['Hommes'] = df['Hommes'].apply(lambda x: int(x))
    df['Enfants'] = df['Enfants'].apply(lambda x: int(x))
    df['WCHR'] = df['WCHR'].apply(lambda x: int(x))
    df['WCHB'] = df['WCHB'].apply(lambda x: int(x))
    df['TransitTime'] = df['TransitTime'].apply(
        lambda x: 0 if type(x) == int else 60 * x.hour + x.minute)

    l = []
    id = 0
    for index, row in df.iterrows():
        groupe = []

        for k in range(row['Femmes']):
            l.append(Individu(id, 'F', row['TransitTime'], row['Numéro du groupe']))
            groupe.append(l[-1])
            id += 1

        for k in range(row['Hommes']):
            l.append(Individu(id, 'H', row['TransitTime'], row['Numéro du groupe']))
            groupe.append(l[-1])
            id += 1

        for k in range(row['Enfants']):
            l.append(Individu(id, 'E', row['TransitTime'], row['Numéro du groupe']))
            groupe.append(l[-1])
            id += 1

        for k in range(row['WCHR']):
            l.append(Individu(id, 'H', row['TransitTime'], row['Numéro du groupe']))
            groupe.append(l[-1])
            id += 1

        for k in range(row['WCHB']):
            l.append(Individu(id, 'H', row['TransitTime'], row['Numéro du groupe']))
            groupe.append(l[-1])
            id += 1

        for n in range(len(groupe)):
            for k in range(len(groupe)):
                if k != n:
                    groupe[n].ajout_au_groupe(groupe[k])

    return l


def lirexcel2(scenario, chemin='DataSeating.xlsx'):
    df = pd.read_excel(chemin, sheet_name=scenario)
    df = df.drop(df.tail(2).index)
    df = df.fillna(0)
    df['Numéro du groupe'] = df['Numéro du groupe'].apply(lambda x: int(x))
    df['Femmes'] = df['Femmes'].apply(lambda x: int(x))
    df['Hommes'] = df['Hommes'].apply(lambda x: int(x))
    df['Enfants'] = df['Enfants'].apply(lambda x: int(x))
    df['WCHR'] = df['WCHR'].apply(lambda x: int(x))
    df['WCHB'] = df['WCHB'].apply(lambda x: int(x))
    df['Classe'] = df['Classe'].apply(lambda x: 0 if x == 'Y' else 1)
    df['TransitTime'] = df['TransitTime'].apply(lambda x: 0 if type(x) == int else 60 * x.hour + x.minute)

    l = []
    id = 0
    for index, row in df.iterrows():
        groupe = []

        for k in range(row['Femmes']):
            l.append(Individu(id, 'F', row['TransitTime'], row['Numéro du groupe'], row['Classe']))
            groupe.append(l[-1])
            id += 1

        for k in range(row['Hommes']):
            l.append(Individu(id, 'H', row['TransitTime'], row['Numéro du groupe'], row['Classe']))
            groupe.append(l[-1])
            id += 1

        for k in range(row['Enfants']):
            l.append(Individu(id, 'E', row['TransitTime'], row['Numéro du groupe'], row['Classe']))
            groupe.append(l[-1])
            id += 1

        for k in range(row['WCHR']):
            l.append(Individu(id, 'R', row['TransitTime'], row['Numéro du groupe'], row['Classe']))
            groupe.append(l[-1])
            id += 1

        for k in range(row['WCHB']):
            l.append(Individu(id, 'B', row['TransitTime'], row['Numéro du groupe'], row['Classe']))
            groupe.append(l[-1])
            id += 1

        for n in range(len(groupe)):
            for k in range(len(groupe)):
                if k != n:
                    groupe[n].ajout_au_groupe(groupe[k])

    return l


def reduction(scenario,ind, chemin='DataSeating.xlsx'):
    df = pd.read_excel(chemin, sheet_name=scenario)
    df = df.drop(df.tail(2).index)
    df = df.fillna(0)
    df['Numéro du groupe'] = df['Numéro du groupe'].apply(lambda x: int(x))
    df['Femmes'] = df['Femmes'].apply(lambda x: int(x))
    df['Hommes'] = df['Hommes'].apply(lambda x: int(x))
    df['Enfants'] = df['Enfants'].apply(lambda x: int(x))
    df['WCHR'] = df['WCHR'].apply(lambda x: int(x))
    df['WCHB'] = df['WCHB'].apply(lambda x: int(x))
    df['Classe'] = df['Classe'].apply(lambda x: 0 if x == 'Y' else 1)
    df['TransitTime'] = df['TransitTime'].apply(lambda x: 0 if type(x) == int else 60 * x.hour + x.minute)

    l = []
    id = 0
    taille_groupe={}
    for individu in ind:
        if individu.idgroupe not in taille_groupe:
            taille_groupe[individu.idgroupe]=0
            
        taille=len(individu.groupe)+1
        if taille<=3 or taille==6:
            l.append(individu)

        elif taille%3==1:
            l.append(Individu(individu.id,individu.categorie,individu.transit,individu.idgroupe+200*((taille_groupe[individu.idgroupe]+1)//3),individu.classe))
            taille_groupe[individu.idgroupe]+=1

        else :
            l.append(Individu(individu.id,individu.categorie,individu.transit,individu.idgroupe+200*(taille_groupe[individu.idgroupe]//3),individu.classe))
            taille_groupe[individu.idgroupe]+=1
            
    groupe={}
    for indi in l:
        if indi.idgroupe not in groupe :
            groupe[indi.idgroupe]=[]
        groupe[indi.idgroupe].append(indi)
    for id_petit_groupe in groupe:
        petit_groupe=groupe[id_petit_groupe]
        for ind1 in petit_groupe:
                for ind2 in petit_groupe:
                    if ind1 != ind2 and not ind2 in ind1.groupe:
                        ind1.ajout_au_groupe(ind2)

    return l

if __name__ == '__main__':
    l = lirexcel2(0)

    for i in l:
        print(i.id, i.categorie, len(i.groupe), i.transit)
