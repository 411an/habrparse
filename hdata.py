import pandas
import pandas as pd

df = pd.DataFrame

colnames=['id', 'nick', 'score']
df = pd.read_csv(r'files\habrbase.csv', sep=',', encoding="ANSI", names = colnames, header = None)

df['digScore'] = df['score'].str.replace('+', '')
df['digScore'] = df['score'].str.replace('–', '-')
df['digScore'] = pd.to_numeric(df['digScore'], downcast='integer')

df1 = df.groupby('nick')['digScore'].sum()

print(df1.head(25))

df1.to_csv('files\habrauthors.csv')