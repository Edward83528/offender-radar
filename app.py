# -*- coding: utf-8 -*-
from flask import Flask , request
from flask import render_template
import os
import model.main as m
import core.core as c

# 創建一個falsk對象(建立類別實體app)
app = Flask(__name__)

global config, ws, pos, ner

# 跳轉首頁
@app.route("/")
def index():
    return render_template('index.html')

# 犯罪分類API
@app.route("/PreditIsCrime" , methods=['POST'])
def preditIsCrime():
    content = request.json
    inputold = content['NewsContext']
    return m.getCrimeFlag(inputold)

# 犯罪分類API
@app.route("/PreditCrimePeoples" , methods=['POST'])
def preditCrimePeoples():
    content = request.json
    inputold = content['NewsContext']
    return_json=m.getCrimeFlag(inputold)
    flag=return_json['ResRedict']
    if flag=='1':
        return c.get_person_str(ws,pos,ner,inputold)
    else:
        return '[]'
    
if __name__ == "__main__":
    
    print('載入ckip資源,這將會花一點時間')
    ws, pos, ner = c.load_data()
    
    port = int(os.environ.get('PORT', 9453))
    app.run(host='0.0.0.0', port=port)