# -*- coding: utf-8 -*-
"""
API集
@author: Zhong-wei
"""
import configparser # 讀取設定檔
import pymssql
from snownlp import SnowNLP
from ckiptagger import data_utils, construct_dictionary, WS, POS, NER
global config, ws, pos, ner

config = configparser.ConfigParser()    
config.read('config.ini')
    
server=config['Pymssqlsql']['server']
database=config['Pymssqlsql']['database']
user=config['Pymssqlsql']['user']
password=config['Pymssqlsql']['password']

def load_data():
    # 使用 GPU：
    #    1. 安裝 tensorflow-gpu (請見安裝說明)
    #    2. 設定 CUDA_VISIBLE_DEVICES 環境變數，例如：os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    #    3. 設定 disable_cuda=False，例如：ws = WS("./data", disable_cuda=False)
    # 使用 CPU：
    ws_ = WS("./core/data")
    pos_ = POS("./core/data")
    ner_ = NER("./core/data")
    return ws_,pos_,ner_

def get_person_str(ws,pos,ner,old_q_input):
    
    snow_nlp = SnowNLP(old_q_input)
    snow_summer_list=snow_nlp.summary(10)
    context = ",".join(snow_summer_list)  
    

    sentence_list = [context]

    word_sentence_list = ws(
        sentence_list,
        # sentence_segmentation = True, # To consider delimiters
        # segment_delimiter_set = {",", "。", ":", "?", "!", ";"}), # This is the defualt set of delimiters
        # recommend_dictionary = dictionary1, # words in this dictionary are encouraged
        # coerce_dictionary = dictionary2, # words in this dictionary are forced
    )

    pos_sentence_list = pos(word_sentence_list)
    entity_sentence_list = ner(word_sentence_list, pos_sentence_list)
    #print(entity_sentence_list)

    set_entity=set()    
    for i, sentence in enumerate(sentence_list):
        #print()
        #print(f"'{sentence}'")
        #print_word_pos_sentence(word_sentence_list[i],  pos_sentence_list[i])
        for entity in sorted(entity_sentence_list[i]):
              if entity[2] == 'PERSON':
                #print(entity[3])
                set_entity.add(entity[3].replace(" ", ""))
    str_entity = ','.join(set_entity)
    #print(str_entity)
    return str_entity.split(",")

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
            people=get_person_str(ws, pos, ner,body);
            cursor.execute("INSERT INTO News(title,link,[content],criminal,people,postdate,updatetime) VALUES ('"+title+"', '"+link+"', '"+body+"','"+criminal+"','"+people+"','"+postdate+"','"+updatetime+"')")
            conn.commit()
    
        cursor.close()
        conn.close()
        return True;
    except:
        return False;
def findPeople(people):
    list_temp = []
    try:
        conn = pymssql.connect(server, user, password, database)
        cursor=getCursor(conn)
        cursor.execute("SELECT people FROM News where people like N'%"+people+"%'")
        row = cursor.fetchone() 
        while row:
            if row[0]!=None:
                temp=row[0].split(",")
                list_temp.extend(temp)
            row = cursor.fetchone()
            
        cursor.close()
        conn.close()
        return list_temp;
    except:
        return list_temp;