# -*- coding: utf-8 -*-
"""
scrape all player costs to array
"""

import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import pickle

#%%

save = r"C:\PhD\Python\FF codes\save\19\plist.pickle"
        
with open (save, 'rb') as f:
    plist = pickle.load(f)
    
#%% GET PLAYER NAMES
    
ubase = r'http://ff.bluebones.net/players.php?p='
names = []

for x in range(0,len(plist)):
    
    url = ubase + str(plist[x])
    
    ra = requests.get(url)
    soupa = BeautifulSoup(ra.content, "lxml")
    
    names.append(soupa.find_all('h1')[0].text)
    
    if x%10 == 0:
        print(float(x)*100/len(plist))
        
names = [x.strip() for x in names]
df = pd.DataFrame({'Name':names})     

#%% GET PLAYER TEAMS/POSITIONS

ubase = r'http://ff.bluebones.net/players.php?p='
clubs = []
positions = []

for x in range(0,len(plist)):
    
    url = ubase + str(plist[x])
    
    ra = requests.get(url)
    soupa = BeautifulSoup(ra.content, "lxml")
    
    positions.append(soupa.find_all('table')[0].find_all("td")[1].text)
    clubs.append(soupa.find_all('table')[0].find_all("td")[3].text)
    
    if x%10 == 0:
        print(float(x)*100/len(plist))
        
dfc = pd.DataFrame({'club':clubs})     
dfp = pd.DataFrame({'position':positions})  

#%% GET BASIC PLAYER STATS

ubase = r'http://ff.bluebones.net/players.php?p='
mainstats = ['Played', 'Goals', 'Assists', 'Clean Sheets', 'Conceded', 'Points', 'Points Last Season']

dfs = pd.DataFrame(columns = mainstats)

for x in range(0,len(plist)):
    
    url = ubase + str(plist[x])
    
    ra = requests.get(url)
    soupa = BeautifulSoup(ra.content, "lxml")
    
    sl = soupa.find_all('table')[0].find_all("td")[13:27:2]

    st = [s.text for s in sl]
    st = [np.nan if x=='-' else x for x in st]
    st = [np.nan if x=='' else x for x in st]
    st = [float(s) for s in st]

    df_current = pd.DataFrame([st],columns = mainstats)
    
    dfs = pd.concat([dfs,df_current])
    
    if x%10 == 0:
        print(float(x)*100/len(plist))

#%% GET AUCTION STATS

ubase = r'http://ff.bluebones.net/players.php?p='

df_bids = None
for x in range(0,len(plist)):
    
    url = ubase + str(plist[x])
    
    ra = requests.get(url)
    soupa = BeautifulSoup(ra.content, "lxml")
    
    try:
        table = soupa.find_all('table')[3]
    except:
        try:
            table = soupa.find_all('table')[2]
        except:
            table = soupa.find_all('table')[1]
    
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
    ny = [m - 7 for m in months]
    years = [2019 if n >= 0 else 2020 if n < 0 else np.nan for n in ny]
    
    df_dummy = pd.DataFrame({'name': hdates, 'year': years, 'month': months, 'day': days})
    df_dummy = df_dummy.set_index('name')
    
    df_dummy = pd.to_datetime(df_dummy)
    
    df_dates = pd.DataFrame([df_dummy.values],columns = df_dummy.index)
    
    df_bids_current = pd.concat([df_costs, df_dates], axis=1, sort=False)
    
    try:
        df_bids = pd.concat([df_bids,df_bids_current])
    except:
        df_bids = df_bids_current
        
    if x%10 == 0:
        print(float(x)*100/len(plist))
        
#%% Put it all together again

df = pd.concat([df_names, df_clubs], axis=1, sort=False)
df = pd.concat([df, df_positions], axis=1, sort=False)
df = pd.concat([df, df_stats.reset_index(drop=True)], axis=1, sort=False)
df = pd.concat([df, df_bids.reset_index(drop=True)], axis=1, sort=False)

#%%
save = r'C:\PhD\Python\FF codes\save\19\df.pickle'

with open (save, 'wb') as f:
    pickle.dump(df, f)

#%% FOR WILL
    
import pickle
import pandas as pd

save = r'C:\PhD\Python\FF codes\save\19\df.pickle'
  
with open(save, 'rb') as f:
    df = pickle.load(f)

#%%
    
save = r'C:\PhD\Python\FF codes\save\19\df_names.pickle'
  
with open(save, 'rb') as f:
    df_names = pickle.load(f)
    
save = r'C:\PhD\Python\FF codes\save\19\df_positions.pickle'
  
with open(save, 'rb') as f:
    df_positions = pickle.load(f)
    
save = r'C:\PhD\Python\FF codes\save\19\df_clubs.pickle'
  
with open(save, 'rb') as f:
    df_clubs = pickle.load(f)
    
save = r'C:\PhD\Python\FF codes\save\19\df_stats.pickle'
  
with open(save, 'rb') as f:
    df_stats = pickle.load(f)
    
'''
save = r'C:\PhD\Python\FF codes\save\19\df_bids.pickle'
  
with open(save, 'rb') as f:
    df_bids = pickle.load(f)
'''

#%%

save = r'C:\PhD\Python\FF codes\save\19\df_names.pickle'
  
with open (save, 'wb') as f:
    pickle.dump(df_names, f)
    
save = r'C:\PhD\Python\FF codes\save\19\df_positions.pickle'
  
with open (save, 'wb') as f:
    pickle.dump(df_positions, f)
    
save = r'C:\PhD\Python\FF codes\save\19\df_clubs.pickle'
  
with open (save, 'wb') as f:
    pickle.dump(df_teams, f)
    
save = r'C:\PhD\Python\FF codes\save\19\df_stats.pickle'
  
with open (save, 'wb') as f:
    pickle.dump(df_stats, f)
    
save = r'C:\PhD\Python\FF codes\save\19\df_bids.pickle'
  
with open (save, 'wb') as f:
    pickle.dump(df_bids, f)