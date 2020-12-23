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

def insertNews(items,isCriminal):
    try:
        conn = pymssql.connect(server, user, password, database)
        cursor=getCursor(conn)
    
        for item in items:
            title=item['title']
            link=item['link']
            body=item['body']
            postdate=item['postdate']
            updatetime=item['updatetime']
            criminal=str(isCriminal);
            cursor.execute("INSERT INTO News(title,link,[content],criminal,postdate,updatetime) VALUES ('"+title+"', '"+link+"', '"+body+"','"+criminal+"',' "+postdate+"','"+updatetime+"')")
            conn.commit()
    
        cursor.close()
        conn.close()
        return True;
    except:
        return False;
