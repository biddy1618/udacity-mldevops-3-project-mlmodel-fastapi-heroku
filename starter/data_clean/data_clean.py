import pandas as pd

PATH_DATA_RAW = '../data/census.csv'
PATH_DATA_CLEAN = '../data/census_clean.csv'


df = pd.read_csv(PATH_DATA_RAW)
df.head()

print(f'Trailing spaces: \n{df.columns.tolist()[:5]} ...')
def trim(dataset):
    trim = lambda x: x.strip() if type(x) is str else x
    dataset.columns = [trim(col) for col in dataset.columns]
    return dataset.applymap(trim)

df = trim(df)
print(f'Removing spaces: \n{df.columns.tolist()[:5]} ...')


search_func_tmp = lambda row: row.astype(str).str.contains('?', regex = False).any()
df.loc[df.apply(search_func_tmp, axis=1)].head()


print(f'Number of rows containing `?`: {df.apply(search_func_tmp, axis=1).sum()}')
df.replace({'?': 'Unknown'}, inplace = True)
print(f'Number of rows containing `?` after replacement: {df.apply(search_func_tmp, axis=1).sum()}')

print(f'Number of rows: {df.shape[0]}')
df.drop_duplicates(inplace = True)
print(f'Number of rows after duplicates drop: {df.shape[0]}')

df.to_csv()