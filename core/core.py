# -*- coding: utf-8 -*-
"""
API集
@author: Zhong-wei
"""

import configparser #讀取設定檔
import pymssql

config = configparser.ConfigParser()    
config.read('../config.ini')

server=config['Pymssqlsql']['server']
database=config['Pymssqlsql']['database']
user=config['Pymssqlsql']['user']
password=config['Pymssqlsql']['password']

def getCursor(conn):
    cursor = conn.cursor()   
    return cursor

def insertNews(items):
    conn = pymssql.connect(server, user, password, database)
    cursor=getCursor(conn)
    counts=0
    for item in items:
        title=item['title']
        link=item['link']
        body=item['body']
        postdate=item['postdate']
        updatetime=item['updatetime']
        count=cursor.execute("INSERT INTO News(title,link,[content],postdate,updatetime) VALUES ('"+title+"', '"+link+"', '"+body+"','"+postdate+"','"+updatetime+"')")
        # 如果沒有指定autocommit屬性為True的話就需要呼叫commit()方法
        conn.commit()
    cursor.close()
    conn.close()

    return counts;
