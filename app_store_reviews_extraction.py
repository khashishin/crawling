#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib import request
from bs4 import BeautifulSoup
import json
import csv
import datetime
import lxml.html

app_id = '461736062'
country_code = 'pl'
app_store_url = 'https://itunes.apple.com/{}/rss/customerreviews/id={}/page={}/sortBy=mostRecent/{}'


def request_until_succeed(url):
    '''
    Metoda ktora probuje wykonac zapytanie na danej stronie, dopoki nie otrzyma odpowiedzi z sukcesem
    '''
    req = request.Request(url)
    success = False
    tries_unsuccesfull = 0
    while success is False:
        try: 
            response = request.urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception as err:
            tries_unsuccesfull +=1
            time.sleep(1)
            print ("{}:{} Error for URL {}".format(datetime.datetime.now(), err, url))
    return response.read().decode('utf-8').replace('\n', '').replace('\r', '').replace('/n','')

# def traverse_webpage_json_url(app_url, app_id, page=1):
#     url = app_url.format(country_code, app_id,page,'json')
#     # print (url)
#     app_store_json = json.loads(request_until_succeed(url))
#     list_of_reviews = []
#     for entry in app_store_json['feed']['entry'][1:]:
#         author = entry['author']['name']['label']
#         uri = entry['author']['uri']['label']
#         rating = entry['im:rating']['label']
#         short_msg = entry['title']['label']
#         long_msg = entry['content']['label']
#         voteSum = entry['im:voteSum']['label']
#         voteCount = entry['im:voteCount']['label']
#         encoded_list = [author,uri,rating,short_msg,long_msg,voteSum,voteCount]
#         list_of_reviews.append (encoded_list)
#     try:
#         next_link = app_store_json['feed']['link'][-1]['attributes']['href']
#         next_link = next_link.replace("xml",'json')
#         if url != next_link:
#             list_of_reviews.extend(traverse_webpage_json_url(next_link,app_id,page+1))
#     except KeyError:
#         pass
#     return list_of_reviews

def traverse_webpage_xml_url(app_url, app_id, page=1):
    from lxml import etree
    url = app_url.format(country_code,app_id,page,'xml')
    # print (url)
    xml = request_until_succeed(url)
    reviews_tree = lxml.html.fromstring(xml.encode('utf-8','ignore'))
    list_of_reviews = []
    entries = reviews_tree.findall('.//entry')
    for entry in entries:
        try:
            author, uri = entry.find('author/').text_content().split('https://') #Due to the weird bug with /name traversing returning both values
        except AttributeError:
            continue
        rating = entry.find('rating').text_content()
        short_msg = entry.find('title').text_content()
        long_msg = entry.find('content[@type="text"]').text_content()
        voteSum = entry.find('votesum').text_content()
        voteCount = entry.find('votecount').text_content()
        date = entry.find('updated').text_content()    
        encoded_list = [author,uri,rating,short_msg,long_msg,voteSum,voteCount,date]
        list_of_reviews.append(encoded_list)
    try:
        next_link = reviews_tree.find('.//link[@rel="next"]').get("href")
        print ("LINK: ",next_link)
        if url != next_link:
            list_of_reviews.extend(traverse_webpage_xml_url(next_link,app_id,page+1))
    except KeyError:
        pass
    return list_of_reviews

def extract_reviews():
    # list_of_reviews =  traverse_webpage_json_url(app_store_url, app_id)
    list_of_reviews = traverse_webpage_xml_url(app_store_url,app_id)
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    with open('reviews_{}_{}_{}.csv'.format(app_id,country_code,date), 'w', encoding = 'utf-8') as file:
        mywriter = csv.writer(file, delimiter=',',
                            quotechar='|')
        mywriter.writerow(['author','uri','rating','short_msg','long_msg','voteSum','voteCount','date'])
        for line in list_of_reviews:
            mywriter.writerow(line)

extract_reviews()