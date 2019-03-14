#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib import request
from bs4 import BeautifulSoup
import json
import csv
import datetime
from lxml import etree
from lxml import html as lhtml


url = "http://www.gazeta.pl/0,0.html"
req = request.Request(url)
# response = request.urlopen(req)
parser = etree.HTMLParser()

with request.urlopen(req) as f:
    tree = etree.parse(f, parser)
    root = tree.getroot()
    # print (etree.tostring(tree, pretty_print=True))
    # for name in root.iter("div"):
    #     etree.dump(name)

    posts = tree.xpath('//*[@id="city_selector_list_src"]/div')
    for entry in posts:
        try:
            print (entry)
        except AttributeError:
            continue

#response = requests.get(link) #get page data from server, block redirects
# sourceCode = response.content #get string of source code from response
# htmlElem = html.document_fromstring(sourceCode) #make HTML element object
