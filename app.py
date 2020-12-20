from flask import Flask,request
from flask import render_template
import configparser #讀取設定檔
import os
#引入自定義function
import core.core

#創建一個falsk對象(建立類別實體app)
app = Flask(__name__)

#讀取設定檔
config = configparser.ConfigParser()
config.read('config.ini')


#跳轉首頁
@app.route("/")
def index():
    return render_template('index.html')


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9453))
    app.run(host='0.0.0.0', port=port)
