# 犯罪雷達

使用python為開發語言，加上深度學習中預訓練的bert模型訓練一個犯罪分類器與犯罪關鍵人找尋模型，Database 為 Sql Server 2012 以上，以 Flask 為應用程式開發基礎框架。

主要概念為兩項功能:
1. 輸入犯罪文章 > 輸出犯罪關係人 ( 輸入不是犯罪文章 > 輸出空集合 )
2. 輸入犯罪人 > 輸出犯罪關係圖

專案目前分成5個 目錄夾：

1. db : 資料庫sql。
2. core：共用函式庫。
3. model：提供bert深度學習模型。
4. static：靜態資源存放。
5. task：排程的程式。
6. templates：存放網頁模板。

### 後端主要使用的組件

1. bert : https://huggingface.co/transformers/model_doc/bert.html
2. ckip : https://github.com/ckiplab/ckiptagger/wiki/Chinese-README

### 前端主要使用的組件

以現代的瀏覽器為主， IE11以下不考慮支援

1. [jQuery 3](https://jquery.com/)
2. [Lodash](https://lodash.com/)
3. [Parsley](https://parsleyjs.org/) client form validate
5. [Datatables](https://datatables.net/)

### 管理後台的樣式

SB Admin 2 (https://github.com/StartBootstrap/startbootstrap-sb-admin-2)

## 資料庫設定

db/schema.sql 和 db/data.sql，請先匯入此script，建立table
data.sql 是手動寫的 insert script，建置起始資料

