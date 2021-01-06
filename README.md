# 犯罪雷達

使用python為開發語言，加上深度學習中預訓練的[Bert](https://huggingface.co/transformers/model_doc/bert.html)模型fine tune一個犯罪分類器並利用[中央研究院CkipTagger model](https://github.com/ckiplab/ckiptagger/wiki/Chinese-README)萃取犯罪人名，Database 為 Sql Server 2019，以 Flask 為應用程式開發基礎框架。

主要概念為兩項功能:
1. 輸入犯罪文章 > 輸出「犯罪關係人」 ( 輸入不是犯罪文章 > 「輸出非犯罪文章或無犯罪人名」 )
![image](https://github.com/Edward83528/offender-radar/blob/master/static/img/info1.jpg)
2. 輸入犯罪人 > 輸出犯罪關係圖
![image](https://github.com/Edward83528/offender-radar/blob/master/static/img/info2.jpg)

專案目前分成7個 目錄夾：

1. core：共用函式庫。
2. dataset：bert犯罪分類使用資料集。
3. db : 資料庫sql。
4. model：提供bert深度學習模型。
5. static：靜態資源存放。
6. task：排程的程式。
7. templates：存放網頁模板。

### 後端主要使用的組件

1. [Bert](https://huggingface.co/transformers/model_doc/bert.html)
2. [Pytorch](https://pytorch.org)
3. [CkipTagger model](https://github.com/ckiplab/ckiptagger/wiki/Chinese-README)
4. [snownlp](https://github.com/isnowfy/snownlp)

### 前端主要使用的組件

以現代的瀏覽器為主， IE11以下不考慮支援

1. [jQuery 3](https://jquery.com)
2. [D3js](https://d3js.org)
3. [Lodash](https://lodash.com)
4. [Parsley](https://parsleyjs.org) client form validate

### 犯罪雷達的樣式

SB Admin 2 (https://github.com/StartBootstrap/startbootstrap-sb-admin-2)

## 資料庫設定

db/schema.sql 和 db/data.sql，請先匯入此script，建立table
data.sql 是手動寫的 insert script，建置起始資料