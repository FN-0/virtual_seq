import pandas as pd

df = pd.read_excel('data/normal_jinshan.xlsx', header=0)
gid = df.iloc[:, 0]
content = df.iloc[:, 1:]
for i in range(len(content.columns)):
  path = 'data/normal/%s.csv' % str(content.columns[i])
  pd.concat([gid,content.iloc[:, i]], axis=1).to_csv(path, index=False)
