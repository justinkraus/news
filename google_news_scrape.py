from bs4 import BeautifulSoup, SoupStrainer
import requests
import pandas as pd
import numpy as np

# df = pd.DataFrame(columns=['activity', 'timestamp'])
ls = []

soup = BeautifulSoup(open("/Downloads/Takeout2/My_Activity/Google_News/MyActivity.html"), "html.parser")

delimiter = '|'                           # unambiguous string
for line_break in soup.findAll('br'):       # loop through line break tags
    line_break.replaceWith(delimiter)

# for link in soup.find_all("div", {"class": "content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1"}):
text_string = [link.text for link in soup.find_all("div", {"class": "content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1"})]
df = pd.DataFrame({'activity': text_string})
print(df)
# df.column = ['activity']
# df[['action', 'timestamp']] = df.activity.str.split(pat=delimiter, expand=True)
df['action'] = df.activity.str.split(pat=delimiter, expand=True)[0]
df['timestamp'] = df.activity.str.split(pat=delimiter, expand=True)[1]
# df = df[df.timestamp != 'EST']

# convert timestamp to datetime type and specific formats
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%b %d, %Y, %I:%M:%S %p %Z', errors='coerce')
df = df.dropna(subset=['timestamp'])
df['dayofweek'] = df['timestamp'].dt.day_name()
df['calendar'] = df['timestamp'].dt.date
df = df[df['calendar'] > pd.to_datetime('2018-12-31')]

# count scores of read vs clicks
# https://stackoverflow.com/questions/43905930/conditional-if-statement-if-value-in-row-contains-string-set-another-column
df['read_watch'] = pd.np.where(df['action'].str.contains("Read"), 1,
                   pd.np.where(df['action'].str.contains("Watched"), 1, 0))

df['saw'] = pd.np.where(df['action'].str.contains("Saw"), 1, 0)

df = df[~df.action.str.contains("For You")]

df.to_csv('google_news_activity_all1.csv', index=False)
print("done!")

reps = [10 if val == 1 else 1 for val in df['saw']]
df = df.loc[np.repeat(df.index.values, reps)]

df.to_csv('google_news_activity_all3.csv', index=False)
print("done!")

# # original heatmap visual grouping with aggregated engagement scores

# # grouped by date dataframe
# df1 = df.groupby(['calendar']).agg(sum_rw =('read_watch', 'sum'), sum_saw=('saw', 'sum')).reset_index()
# df1['ratio'] = df1['sum_rw'] / (df1['sum_saw'] * 10)

# df1 = df1.drop(columns=[
# 	'sum_rw',
# 	'sum_saw'
# 	])

# df1 = df1.rename(columns={"calendar": "date"})

# out = df1.to_json(orient= "records")

# with open('news_engagement.txt', 'w') as f:
#     f.write(out)