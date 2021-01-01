# -*- coding: utf-8 -*-
from flask import Flask , request , jsonify
import json
from flask import render_template
import os
import model.main as m
import core.core as c
import torch
# 創建一個falsk對象(建立類別實體app)
app = Flask(__name__)

global config, ws, pos, ner

# 跳轉首頁
@app.route("/")
def index():
    return render_template('index.html')

# 跳轉預測犯罪人頁面
@app.route("/crimePeoples")
def crimePeoples():
    return render_template('crimePeoples.html')

# 跳轉犯罪圖頁面
@app.route("/crimeGraph")
def crimeGraph():
    return render_template('crimeGraph.html')

# 犯罪分類API
@app.route("/PreditIsCrime" , methods=['POST'])
def preditIsCrime():
    content = request.json
    inputold = content['NewsContext']
    return m.getCrimeFlag(inputold)

# 文章找犯罪人API
@app.route("/PreditCrimePeoples" , methods=['POST'])
def preditCrimePeoples():
    content = request.json
    inputold = content['NewsContext']
    response=m.getCrimeFlag(inputold)
    return_json=json.loads(response.data)
    flag=return_json['ResRedict']
    if flag == 1:
        return jsonify( { "people":c.get_person_str(ws,pos,ner,inputold)} )
    else:
        return jsonify( { "people":'非犯罪文章或無犯罪人名' } )
    
# 找犯罪關係人API
@app.route("/FindPeoples" , methods=['POST'])
def findPeoples():
    content = request.json
    peopleOld = content['people']
    peopleList=c.findPeople(peopleOld)
    return jsonify( { "people":peopleList } )

if __name__ == "__main__":

    print(torch.__version__)
    print(torch.cuda.is_available())
    print('載入ckip資源,這將會花一點時間')
    ws, pos, ner = c.load_data()
    
    port = int(os.environ.get('PORT', 9453))
    app.run(host='0.0.0.0', port=port)