# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import pickle

#%%

save = "C:\PhD\Python\FF codes\save\plist.pickle"
        
with open (save, 'rb') as f:
    plist = pickle.load(f)
    
a = r'http://ff.bluebones.net/players.php?p=6327'

ra = requests.get(a)

soupa = BeautifulSoup(ra.content, "lxml")

    
#%%

dcols = ['D1','D2','D3A','D3B','D4A','D4B','D4C','D4D','D5A','D5B','D5C','D5D','D5E','D5F','D6A','D6B','D6C','D6D','D6E','D6F','D6G','D6H','D6I','D7A','D7B','D7C','D7D','D7E','D7F','D7G','D7H','D7I','D7J','D7K','D7L']

al = soupa.find_all('table')[3].find_all(class_="n")

row = np.empty((35),dtype=float)
row[:] = np.nan

j = 0
for i in al[1:]:
    try:
        row[j] = float(i.contents[0][1:-1])
    except:
        pass
    j += 1

dfa = pd.DataFrame([row],columns = dcols)

#%%

try:
    table = soupa.find_all('table')[3]
except:
    table = soupa.find_all('table')[2]
    
table_rows = table.find_all('tr')

costs = []
times = []
headers = []
for tr in table_rows[1:]:
    td = tr.find_all('td')
    row = [tr.text for tr in td]
    costs.append(row[2])
    times.append(row[3])
    headers.append(row[0])
    
#%%
hsc = [(x + ' Price') for x in headers]
hdates = [(x + ' When') for x in headers]

sc = [x[1:-1] for x in costs]
sc = [np.nan if x == '' else x for x in sc]
sc = [float(s) for s in sc]

df_costs = pd.DataFrame([sc],columns = hsc)

n2m = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
m2n = dict(zip(n2m.values(), n2m.keys()))

days = [int(x[-8:-6]) if x != '' else np.nan for x in times]
months = [m2n[x[-3:]] if x != '' else np.nan for x in times]
years = [2018 for x in times]

df_dummy = pd.DataFrame({'name': hdates, 'year': years, 'month': months, 'day': days})
df_dummy = df_dummy.set_index('name')

df_dummy = pd.to_datetime(df_dummy)

df_dates = pd.DataFrame([df_dummy.values],columns = df_dummy.index)

df_bids = pd.concat([df_costs, df_dates], axis=1, sort=False)

#%%

sl = soupa.find_all('table')[0].find_all("td")[13:27:2]

mainstats = ['Played', 'Goals', 'Assists', 'Clean Sheets', 'Conceded', 'Points Last Season', 'Points']

st = [s.text for s in sl]
st = [np.nan if x=='-' else x for x in st]
st = [float(s) for s in st]

dfb = pd.DataFrame([st],columns = mainstats)

    
#%%

start = 6180
end = 7031

pllist = []

ubase = r'http://ff.bluebones.net/players.php?p='

for x in range(start,end+1):
    
    url = ubase + str(x)
    
    ru = requests.get(url)

    soupa = BeautifulSoup(ru.content, "lxml")
    
    if not soupa.find_all('h1')[0].text=='All Players':
        pllist.append(x)
    print(x)

#%%
        
save = "C:\PhD\Python\FF codes\save\plist.pickle"
        
with open(save, 'wb') as f:
    pickle.dump(pllist, f)