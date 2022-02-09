import pandas as pd
from individu import Individu


def lirexcel(scenario, chemin='DataSeating.xlsx', n=9):
    df = pd.read_excel(chemin, sheet_name=scenario)
    df = df.fillna(0)
    df['Femmes'] = df['Femmes'].apply(lambda x: int(x))
    df['Hommes'] = df['Hommes'].apply(lambda x: int(x))
    df['Enfants'] = df['Enfants'].apply(lambda x: int(x))
    df['WCHR'] = df['WCHR'].apply(lambda x: int(x))
    df['WCHB'] = df['WCHB'].apply(lambda x: int(x))
    df['TransitTime'] = df['TransitTime'].apply(lambda x: 0 if type(x) == int else 60 * x.hour + x.minute)

    l = []
    id = 0
    for index, row in df.iterrows():
        groupe = []

        for k in range(row['Femmes']):
            l.append(Individu(id, 'F', row['TransitTime']))
            groupe.append(l[-1])
            id += 1

        for k in range(row['Hommes']):
            l.append(Individu(id, 'H', row['TransitTime']))
            groupe.append(l[-1])
            id += 1

        for k in range(row['Enfants']):
            l.append(Individu(id, 'E', row['TransitTime']))
            groupe.append(l[-1])
            id += 1

        for k in range(row['WCHR']):
            l.append(Individu(id, 'H', row['TransitTime']))
            groupe.append(l[-1])
            id += 1

        for k in range(row['WCHB']):
            l.append(Individu(id, 'H', row['TransitTime']))
            groupe.append(l[-1])
            id += 1

        for n in range(len(groupe)):
            for k in range(len(groupe)):
                if k != n:
                    groupe[n].ajout_au_groupe(groupe[k])

    return l

if __name__ == '__main__':
    l = lirexcel(0)

    print('# 23')
    for x in l[23].group:
        print(x.id)

    print('# 24')
    for x in l[24].group:
        print(x.id)

    print('# 25')
    for x in l[25].group:
        print(x.id)

    print('# 26')
    for x in l[26].group:
        print(x.id)