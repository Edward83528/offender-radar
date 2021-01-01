# 犯罪雷達

使用python為開發語言，加上深度學習中預訓練的Bert模型訓練一個犯罪分類器與犯罪關鍵人找尋模型，Database 為 Sql Server 2012 以上，以 Flask 為應用程式開發基礎框架。

主要概念為兩項功能:
1. 輸入犯罪文章 > 輸出「犯罪關係人」 ( 輸入不是犯罪文章 > 「輸出非犯罪文章或無犯罪人名」 )
![image](https://github.com/harry83528/taskQALineBot/blob/master/messageImage_1578628507824.jpg)
2. 輸入犯罪人 > 輸出犯罪關係圖
![image](https://github.com/harry83528/taskQALineBot/blob/master/messageImage_1578628507824.jpg)

專案目前分成5個 目錄夾：

1. db : 資料庫sql。
2. core：共用函式庫。
3. model：提供bert深度學習模型。
4. static：靜態資源存放。
5. task：排程的程式。
6. templates：存放網頁模板。

### 後端主要使用的組件

1. [Bert](https://huggingface.co/transformers/model_doc/bert.html)
2. [Pytorch](https://pytorch.org)
3. [ckip](https://github.com/ckiplab/ckiptagger/wiki/Chinese-README)
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