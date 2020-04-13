# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import pickle

url_manlist = r'http://ff.bluebones.net/teams.php'

ra_manlist = requests.get(url_manlist)
soup_manlist = BeautifulSoup(ra_manlist.content, "lxml")
table_manlist = soup_manlist.find_all('table')[0]

table_rows = table_manlist.find_all('tr')

divs = []
teams = []
managers = []

for t in range(1,len(table_rows)):
    row = table_rows[t].text.split("\n")
    divs.append(row[1].strip(" "))
    teams.append(row[2].strip(" "))
    managers.append(row[3].strip(" "))
    
df = pd.DataFrame({'Manager': managers, 'Team': teams, 'Division': divs})

save = r'C:\PhD\Python\FF codes\save\19\manlist.pickle'

with open (save, 'wb') as f:
    pickle.dump(df, f)