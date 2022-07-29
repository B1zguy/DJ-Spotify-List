# https://stackoverflow.com/a/60634160/7923512
import pandas as pd
import fuzzy_pandas as fpd
import xlwings as xw

df1 = pd.read_csv('dj-practice-v5.csv')
print('df1 pre: ', len(df1.index))
df1 = df1.drop_duplicates(subset=['Track Name', 'Artist Name(s)'], keep='first')
print('df1 post: ', len(df1.index))
df2 = pd.read_csv('iTunes Catalog Export v3.csv', delimiter='^', names=['Title', 'Artist'])
print('df2 len: ', len(df2.index))

results = fpd.fuzzy_merge(df1, df2,
                          left_on=['Track Name'],
                          right_on=['Title'],
                          method='levenshtein',
                          # method='jaro',
                          threshold=0.80,
                          keep_left=['Track Name', 'Artist Name(s)'],
                          keep_right=['Title', 'Artist'],
                          # ignore_alpha=True,
                          # ignore_nonlatin=True
                          join=['left-outer']
                          )

xw.view(results)


'''
results = fpd.fuzzy_merge(df1, df2,
                          left_on=['Track Name', 'Artist Name(s)'],
                          right_on=['Title', 'Artist'],
                          method='levenshtein',
                          threshold=0.6,
                          keep='match') # displays shared columns
'''