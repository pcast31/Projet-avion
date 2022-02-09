import pandas as pd

def lirexcel(path='DataSeating.xlsl', n=9):
    l = []
    
    for i in range(n):
        l.append(pd.read_excel(path, sheet_name=i))

    return l