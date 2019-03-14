from urllib import request
from bs4 import BeautifulSoup

start_website = "http://www.gazeta.pl/0,0.html"
site = BeautifulSoup(request.urlopen(start_website).read(), "html.parser")

daty = site.findAll('div', {'class': 'c-article'} )
daty = set(daty)

for data in daty:
    print (data.text)