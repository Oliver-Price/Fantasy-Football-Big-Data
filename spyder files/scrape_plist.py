# -*- coding: utf-8 -*-
start = 7032
end = 7685

pllist = []

ubase = r'http://ff.bluebones.net/players.php?p='

for x in range(start,end+1):
    
    url = ubase + str(x)
    
    ru = requests.get(url)

    soupa = BeautifulSoup(ru.content, "lxml")
    
    if not soupa.find_all('h1')[0].text=='All Players':
        pllist.append(x)
    print(x)
    
save = r"C:\PhD\Python\FF codes\save\19\plist.pickle"

with open (save, 'wb') as f:
    pickle.dump(pllist, f)
