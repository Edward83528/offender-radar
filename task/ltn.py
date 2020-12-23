#coding:utf-8
#65001
import urllib.request
import json
import codecs
import sys
import argparse as ap
import time
import datetime
import requests
import random
from bs4 import BeautifulSoup as bs
from urllib.parse import quote
from core.core import insertNews

keyword = quote('犯罪')
start_date = datetime.datetime.now().strftime('%Y-%m-%d')
end_date = datetime.datetime.now().strftime('%Y-%m-%d')
pages = '3'


def start_requests():
    if( len(start_date.split("-"))==3 and len(end_date.split("-"))==3) :
        SYear = start_date.split("-")[0]
        SMonth = start_date.split("-")[1]
        SDay = start_date.split("-")[2]
        EYear = end_date.split("-")[0]
        EMonth = end_date.split("-")[1]
        EDay = end_date.split("-")[2]
        urls = []
        for i in range(1,int(pages)+1):
            str_idx = ''+('%s' % i)
            urls.append('http://search.ltn.com.tw/list?keyword='+keyword+'&type=all&sort=date&start_time='+SYear+SMonth+SDay+'&end_time='+EYear+EMonth+EDay+'&page='+str_idx+'')

        for url in urls:
            print ('url:',url)
            parseLtnNews(url)
            time.sleep(0.5)
    else:
        print ("Data format error.")


def request_uri(uri):
    header = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    rs = requests.session()
    res = rs.get(uri, headers=header)
    html_data =  res.text
    #r = requests.post(url=uri, headers={'Connection':'close'})
    return html_data

def parseLtnNews(uri):
    html_data =  request_uri(uri)
    soup = bs(html_data,'html.parser')
    postdate = []
    link = []
    title = []
    body = []
    for ul_soup in soup.findAll('ul',attrs={"class":"list boxTitle"}):
        for span_soup in ul_soup.findAll('span'):
            pd = span_soup.string.replace("&nbsp;","")[:10]
            postdate.append(pd)
        for a_soup in ul_soup.findAll('a',attrs={"class":"tit"}):
            tle = a_soup.getText()
            lnk = a_soup.get('href')
            print(lnk)
            title.append(tle.strip())
            link.append(lnk)
            html_data = request_uri(lnk)
        for newslistul_soup in ul_soup.findAll('div',attrs={"class":"cont"}):
            tmp_body = ''
            for p_soup in newslistul_soup.findAll('p'):
                tmp_body += p_soup.getText()
            body.append(tmp_body)
            
    current = 0
    while current < len(postdate):
        print(title[current])
        items.append({
            "title": title[current],
            "link":link[current],
            "body":body[current],
            "postdate":postdate[current],
            #"updatetime":datetime.datetime.now(),  # MongoDB
            "updatetime":datetime.datetime.now().strftime('%Y-%m-%d')
          })
        current+=1


if __name__ == '__main__':
    items = []
    start_requests();
    #row_json = json.dumps(items, ensure_ascii=False)
    #file = codecs.open(urllib.parse.unquote(keyword)+'.json', 'w', encoding='utf-8')
    #file.write(row_json)
    #file.close()
    
    insertNews(items,True)
  
    print("Done")