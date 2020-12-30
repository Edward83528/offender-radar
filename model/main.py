from flask import Flask , request , jsonify
import os
import pickle
import torch
from transformers import BertConfig, BertTokenizer, BertForSequenceClassification, AdamW
from torch.utils.data import DataLoader, TensorDataset
from IPython.display import clear_output
import torch.nn.functional as F # 激勵函數
import configparser #讀取設定檔

config = configparser.ConfigParser()    
config.read('config.ini')
model_path=config['Model']['path']

def fillZero( tokens , max_len ) :  
  while len(tokens)<max_len:
    tokens.append(0)
  return tokens

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

def getCrimeFlag(content):
    
     # 取得此預訓練模型所使用的 tokenizer
    PRETRAINED_MODEL_NAME = "bert-base-chinese"  # 指定繁簡中文 BERT-BASE 預訓練模型
    tokenizer = BertTokenizer.from_pretrained(PRETRAINED_MODEL_NAME)
    
    device = torch.device("cuda")
    bert_config, bert_class, bert_tokenizer = (BertConfig, BertForSequenceClassification, BertTokenizer)
    config_LayerOne = bert_config.from_pretrained(model_path+'config.json')
    model_LayerOne = bert_class.from_pretrained(model_path+'pytorch_model.bin', from_tf=bool('.ckpt' in 'bert-base-chinese'), config=config_LayerOne )
    model_LayerOne.to(device)
    model_LayerOne.eval()   
    
    testStr = content['NewsContext']
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