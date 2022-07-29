import pandas as pd
import difflib
import xlwings as xw
from icecream import ic
import diagnostic_functions


def fuzzy_merge(df1, df2, left_on, right_on, how='inner', cutoff=0.6):
    df_other = df2.copy()
    df_other[left_on] = [get_closest_match(x, df1[left_on], cutoff) for x in df_other[right_on]]
    # return df1.merge(df_other, on=left_on, how=how)
    # return df1.merge(df_other, left_on=['Track Name', 'Artist Name(s)'], right_on=['Title', 'Artist'], how=how)
    # left.merge(right3[['key', 'newcol']], on='key')
    return pd.merge(df1, df_other, left_on=['Track Name', 'Artist Name(s)'], right_on=['Title', 'Artist'], how=how)


def get_closest_match(x, other, cutoff):
    #print('x: ' + x, 'other: ' + other, 'cutoff: ' + str(cutoff))
    #print('x: ' + x, 'cutoff: ' + str(cutoff))
    #diagnostic_functions.isolate_NO_tracks(x)
    #matches = difflib.get_close_matches(x, other, cutoff=cutoff)

    print(x)
    try:
        matches = difflib.get_close_matches(x, other, cutoff=cutoff)
        return matches[0] if matches else None
    except:
        print(x)
    #return matches[0] if matches else None


wb = xw.Book('DJ Interface.xlsx')
ws = wb.sheets['Sheet1']


df1 = pd.read_csv('dj-practice-v5.csv')
print('df1 pre: ', len(df1.index))
df1 = df1.drop_duplicates(subset=['Track Name', 'Artist Name(s)'], keep='first') # Perhaps add/keep track of original place/index of track down the line. Could be useful for keeping parity w/ Spotify
print('df1 post: ', len(df1.index))
#df2 = pd.read_csv('iTunes Catalog Export v2.csv', delimiter='^', names=['Title', 'Artist', 'Album Artist', 'Album', 'Year', 'Track'])
df2 = pd.read_csv('iTunes Catalog Export v3.csv', delimiter='^', names=['Title', 'Artist'])
print('df2 len: ', len(df2.index))

load = fuzzy_merge(df1, df2, left_on='Track Name', right_on='Title', how='inner')
loaded = load[['Track Name', 'Artist Name(s)', 'Title', 'Artist']].copy()
# left.merge(right3[['key', 'newcol']], on='key')

# print(load.columns)



xw.view(loaded)