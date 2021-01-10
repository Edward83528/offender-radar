# 犯罪雷達

使用python 3.7.9為開發語言，加上深度學習中預訓練的[Bert](https://huggingface.co/transformers/model_doc/bert.html)模型訓練一個犯罪分類器並利用[中央研究院CkipTagger model](https://github.com/ckiplab/ckiptagger/wiki/Chinese-README)萃取犯罪人名，Database 使用 Sql Server 2019，以 Flask 為應用程式開發基礎框架。

犯罪雷達主要概念與貢獻為以下兩項功能:
1. 輸入犯罪文章 > 輸出「犯罪關係人」 ( 輸入不是犯罪文章 > 「輸出非犯罪文章或無犯罪人名」 )
![image](https://github.com/Edward83528/offender-radar/blob/master/static/img/info1.jpg)
2. 輸入犯罪人 > 輸出犯罪關係圖
![image](https://github.com/Edward83528/offender-radar/blob/master/static/img/info2.jpg)

此專案使用方式:
1. git clone下來。
2. 用requirements.txt安裝此專案套件(另外memo.txt提到的也需要安裝)。
3. 更改config.ini設定檔參數(當中有mssql連線參數與bert模型存放路徑參數)。
4. run app.py 則成功啟動專案(往下看會有關鍵程式碼解說)。

專案目前分成7個 目錄夾：

1. core：共用函式庫。
2. dataset：bert訓練犯罪分類器使用之資料集。
3. db : 資料庫sql。
4. model：提供bert深度學習模型函式與模型連結。
5. static：靜態資源存放。
6. task：排程的程式。
7. templates：存放網頁模板。

### 後端主要使用的組件

1. [Bert](https://huggingface.co/transformers/model_doc/bert.html)
2. [Pytorch](https://pytorch.org)
3. [CkipTagger model](https://github.com/ckiplab/ckiptagger/wiki/Chinese-README) (使用方式依照此github連結教學)
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

# 重要程式碼解說
## bert模型訓練
    輸入的文章要組成bert的input格式
```python
def ToBertFormat( title , label ) :
  # From makeDataset : TensorDataset(all_input_ids, all_input_segment_ids, all_input_masks, all_answer_lables)
  selLen = -1 
  # [0] : id
  tokens = tokenizer.tokenize( title )
  content_id = tokenizer.build_inputs_with_special_tokens(tokenizer.convert_tokens_to_ids(tokens))
  selLen = len(content_id)
  content_id = fillZero(content_id, max_seq_len)
  # [1] : segment ids
  segment_id = [0]*max_seq_len
  # [2] : mask
  mask_id = [1]*selLen + [0]*(max_seq_len-selLen)
  # [3] : answer label
  label_id = label

  return content_id , segment_id , mask_id , label_id
def makeDataset(data_feature):
    input_ids = data_feature['input_ids']
    input_segment_ids = data_feature['input_segment_ids']
    input_masks = data_feature['input_masks']
    answer_lables = data_feature['answer_lables']

    all_input_ids = torch.tensor([input_id for input_id in input_ids], dtype=torch.long)
    all_input_segment_ids = torch.tensor([input_segment_id for input_segment_id in input_segment_ids], dtype=torch.long)
    all_input_masks = torch.tensor([input_mask for input_mask in input_masks], dtype=torch.long)
    all_answer_lables = torch.tensor([answer_lable for answer_lable in answer_lables], dtype=torch.long)
    dataset = TensorDataset(all_input_ids, all_input_segment_ids, all_input_masks, all_answer_lables)
    return dataset
	
bert_config, bert_class, bert_tokenizer = (BertConfig, BertForSequenceClassification, BertTokenizer)

# Set use gpu
device = torch.device("cuda")

train_dataloader = DataLoader(trainingDataSet ,batch_size=2 ,shuffle=True)
test_dataloader = DataLoader(testingDataSet ,batch_size=2 ,shuffle=True)

config = bert_config.from_pretrained('bert-base-chinese',num_labels = 2)
model = bert_class.from_pretrained('bert-base-chinese', from_tf=bool('.ckpt' in 'bert-base-chinese'), config=config)
model.to(device)

# Prepare optimizer and schedule (linear warmup and decay)
no_decay = ['bias', 'LayerNorm.weight']
optimizer_grouped_parameters = [
    {'params': [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)], 'weight_decay': 0.0},
    {'params': [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}
    ]
Learning_rate = 5e-6       # 學習率
optimizer = AdamW(optimizer_grouped_parameters, lr=Learning_rate, eps=1e-8)
```	
## bert模型預測
    使用已經訓練好bert model,輸入的文章要組成bert的input格式
```python
# bert的input格式
def ToBertFormat(tokenizer , input_content , input_label , input_max_seq_len) :
  # From makeDataset : TensorDataset(all_input_ids, all_input_segment_ids, all_input_masks, all_answer_lables)
  selLen = -1 
  # [0] : id
  tokens = tokenizer.tokenize( input_content )
  content_id = tokenizer.build_inputs_with_special_tokens(tokenizer.convert_tokens_to_ids(tokens))
  selLen = len(content_id)
  content_id = fillZero(content_id, input_max_seq_len)
  # [1] : segment ids
  segment_id = [0]*input_max_seq_len
  # [2] : mask
  mask_id = [1]*selLen + [0]*(input_max_seq_len-selLen)
  # [3] : answer label
  label_id = input_label
  return content_id , segment_id , mask_id , label_id
# 轉成TensorDataset
def makeDataset(data_feature):
    input_ids = data_feature['input_ids']
    input_segment_ids = data_feature['input_segment_ids']
    input_masks = data_feature['input_masks']
      
    all_input_ids = torch.tensor([input_id for input_id in input_ids], dtype=torch.long)
    all_input_segment_ids = torch.tensor([input_segment_id for input_segment_id in input_segment_ids], dtype=torch.long)
    all_input_masks = torch.tensor([input_mask for input_mask in input_masks], dtype=torch.long)
    dataset = TensorDataset(all_input_ids, all_input_segment_ids, all_input_masks)

    return dataset


    cursor = conn.cursor()   
    return cursor
# 使用bert
def getCrimeFlag(testStr):
    
     # 取得此預訓練模型所使用的 tokenizer
    PRETRAINED_MODEL_NAME = "bert-base-chinese"  # 指定繁簡中文 BERT-BASE 預訓練模型
    tokenizer = BertTokenizer.from_pretrained(PRETRAINED_MODEL_NAME)
    
    device = torch.device("cuda")
    bert_config, bert_class, bert_tokenizer = (BertConfig, BertForSequenceClassification, BertTokenizer)
    config_LayerOne = bert_config.from_pretrained(model_path+'config.json')
    model_LayerOne = bert_class.from_pretrained(model_path+'pytorch_model.bin', from_tf=bool('.ckpt' in 'bert-base-chinese'), config=config_LayerOne )
    model_LayerOne.to(device)
    model_LayerOne.eval()   
    
    # testStr = "跨境洗錢集團總裁落跑！身家百億擁海陸空頂級交通工具"
    testStrLen = len(tokenizer.build_inputs_with_special_tokens(tokenizer.convert_tokens_to_ids(tokenizer.tokenize(testStr))))
    testStr_contentId , testStr_seqmentId , testStr_maskId , testStr_labelId = ToBertFormat( tokenizer ,testStr , 0 , testStrLen )

    data_content_ids = [] 
    data_segment_ids =[]
    data_mask_ids = []
    data_label_ids = []
    data_content_ids.append(testStr_contentId) 
    data_segment_ids.append(testStr_seqmentId) 
    data_mask_ids.append(testStr_maskId)
    data_label_ids.append(testStr_labelId)

    testStrData_features = { 'input_ids':data_content_ids,'input_segment_ids':data_segment_ids,'input_masks':data_mask_ids,'answer_lables':data_label_ids }

    testStrData_dataset = makeDataset(testStrData_features)
    testStr_dataloader = DataLoader(testStrData_dataset ,batch_size=1 ,shuffle=False)

    res = -1.0
    for batch_dict in testStr_dataloader:
        batch_dict = tuple(t.to(device) for t in batch_dict)
        outputs = model_LayerOne(
            batch_dict[0],
            token_type_ids = batch_dict[1],
            attention_mask = batch_dict[2]
            )
        
        logits = outputs[0]
        for predicts in logits :
            print(predicts)
            max_val = torch.max(predicts)
            label = (predicts == max_val).nonzero()[0][0]
            res = label.item() 

    return jsonify( { 
        "ResRedict":res,
        "Version":torch.__version__ ,
        "testStr_contentId":testStr_contentId,
        "testStr_seqmentId":testStr_seqmentId,
        "testStr_maskId":testStr_maskId,
        "testStr_labelId":testStr_labelId
    } )
```	