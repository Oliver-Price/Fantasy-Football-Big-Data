# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import pickle

start = 7032
end = 7688

pllist = []

ubase = r'http://ff.bluebones.net/players.php?p='

for x in range(start,end+1):
    
    url = ubase + str(x)
    
    ru = requests.get(url)

    soupa = BeautifulSoup(ru.content, "lxml")
    
    if not soupa.find_all('h1')[0].text=='All Players':
        pllist.append(x)
    print(x)
    
save = r"C:\PhD\Python\notebooks\Fantasy-Football-Big-Data\save\21\plist.pickle"

with open (save, 'wb') as f:
    pickle.dump(pllist, f)
