import os
import sys
from datetime import datetime
sys.path.append("./BertSentiment")
sys.path.append("./WordCloud")
from BertSentiment import BertAPI
text="test"
path=os.path.dirname(__file__)
path=os.path.join(path,"BertSentiment")
result=BertAPI.predictAPI(text,path)
print(result)
create_time=str(datetime.now().year)+str(datetime.now().month)+str(datetime.now().day)
print(create_time)
