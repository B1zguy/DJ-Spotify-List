from thefuzz import fuzz
from thefuzz import process
import pandas as pd
import xlwings as xw


def fuzzy_merge(df_1, df_2, key1, key2, threshold=90, limit=2):
    """
    :param df_1: the left table to join
    :param df_2: the right table to join
    :param key1: key column of the left table
    :param key2: key column of the right table
    :param threshold: how close the matches should be to return a match, based on Levenshtein distance
    :param limit: the amount of matches that will get returned, these are sorted high to low
    :return: dataframe with boths keys and matches
    """
    s = df_2[key2].tolist()

    m = df_1[key1].apply(lambda x: process.extract(x, s, limit=limit))
    df_1['matches'] = m

    m2 = df_1['matches'].apply(lambda x: ', '.join([i[0] for i in x if i[1] >= threshold]))
    df_1['matches'] = m2

    return df_1


df1 = pd.read_csv('dj-practice-v5.csv')
print('df1 pre: ', len(df1.index))
df1 = df1.drop_duplicates(subset=['Track Name', 'Artist Name(s)'], keep='first') # Perhaps add/keep track of original place/index of track down the line. Could be useful for keeping parity w/ Spotify
print('df1 post: ', len(df1.index))
#df2 = pd.read_csv('iTunes Catalog Export v2.csv', delimiter='^', names=['Title', 'Artist', 'Album Artist', 'Album', 'Year', 'Track'])
df2 = pd.read_csv('iTunes Catalog Export v3.csv', delimiter='^', names=['Title', 'Artist'])
print('df2 len: ', len(df2.index))


load = fuzzy_merge(df1, df2, 'Track Name', 'Title', threshold=80)


loaded = load[['Track Name', 'Artist Name(s)', 'matches']].copy()

xw.view(loaded)