import pandas as pd
import xlwings as xw
import difflib

df1 = pd.read_csv('dj-practice-v5.csv')
df2 = pd.read_csv('iTunes Catalog Export v2.csv', delimiter='^', names=['Title', 'Artist'])

df2['Title'] = df2.apply(lambda x: difflib.get_close_matches(x, df1['Track Name'])[0])

t = df1.merge(df2)

xw.view(t)

