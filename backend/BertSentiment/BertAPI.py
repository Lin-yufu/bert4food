import os.path
import torch
import torch.nn as nn
from pytorch_pretrained import BertModel, BertTokenizer
PAD, CLS = '[PAD]', '[CLS]'  # padding符号, bert中综合信息符号
class Config(object):
    """配置参数"""
    def __init__(self, path,dataset):
        self.model_name = 'bert'
        self.class_list = [x.strip() for x in open(
            path + dataset + '/data/class.txt').readlines()]                                # 类别名单
        self.save_path = path + dataset + '/saved_dict/' + self.model_name + '.ckpt'        # 模型训练结果
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')   # 设备
        self.bert_path = path + '/bert_pretrain'
        self.num_classes = len(self.class_list)
        self.pad_size = 32
        self.tokenizer = BertTokenizer.from_pretrained(self.bert_path)
        self.hidden_size = 768
class Model(nn.Module):

    def __init__(self, config):
        super(Model, self).__init__()
        self.bert = BertModel.from_pretrained(config.bert_path)
        for param in self.bert.parameters():
            param.requires_grad = True
        self.fc = nn.Linear(config.hidden_size, config.num_classes)

    def forward(self, x):
        context = x[0]  # 输入的句子
        mask = x[2]  # 对padding部分进行mask，和句子一个size，padding部分用0表示，如：[1, 1, 1, 1, 0, 0]
        _, pooled = self.bert(context, attention_mask=mask, output_all_encoded_layers=False)
        out = self.fc(pooled)
        return out

def create_dataset(config,data,device,pad_size=32):#读取数据并进行tokenization
    contents=[]
    content=data
    token = config.tokenizer.tokenize(content)
    token = [CLS] + token
    seq_len = len(token)
    mask = []
    token_ids = config.tokenizer.convert_tokens_to_ids(token)

    if pad_size:
        if len(token) < pad_size:
            mask = [1] * len(token_ids) + [0] * (pad_size - len(token))
            token_ids += ([0] * (pad_size - len(token)))
        else:
            mask = [1] * pad_size
            token_ids = token_ids[:pad_size]
            seq_len = pad_size
    x = torch.LongTensor([token_ids]).to(device)

    # pad前的长度(超过pad_size的设为pad_size)
    seq_len = torch.LongTensor([seq_len]).to(device)
    mask = torch.LongTensor([mask]).to(device)
    return (x,seq_len,mask)
def classification(config,data,model):
    model.eval()
    text=create_dataset(config,data,device=config.device)
    output=model(text)
    return output

#必须传入路径，跨文件夹无法找到模型路径
def predictAPI(text,path):
    dataset = '/FoodComment'
    config = Config(path,dataset)
    model = Model(config).to(config.device)
    model.load_state_dict(torch.load(config.save_path))
    output = classification(config, text, model)
    predict = torch.max(output.data, 1)[1].cpu().numpy()
    return predict[0]

def hello():
    return "hello"
if __name__=="__main__":
    path= os.path.dirname(__file__)
    text = "今天的回锅肉非常难吃"
    result=predictAPI(text,path)
    if(result==0):print("消极评价")
    else:print("积极评价")
