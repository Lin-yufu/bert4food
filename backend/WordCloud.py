import jieba
from wordcloud import WordCloud
import pymysql
from PIL import Image
import numpy as np
import time
def wordcloudAPI():
    db = pymysql.connect(
        host="localhost",
        port=3306,
        user='root',
        password='',
        charset='utf8mb4',
        database='bert'
        )
    cursor = db.cursor() #创建游标对象


    query_negative='SELECT COMMENT FROM feedback WHERE sentiment=0'
    query_positive='SELECT COMMENT FROM feedback WHERE sentiment=1'

    cursor.execute(query_negative)
    negative_comments=cursor.fetchall()
    cursor.execute(query_positive)
    positive_comments=cursor.fetchall()
    cursor.close()
    db.close()
    negative_text=""
    positive_text=""
    for comment in negative_comments:
        negative_text+=comment[0]
    for comment in positive_comments:
        positive_text+=comment[0]
    print(negative_text)
    print(positive_text)
    #jieba
    stopwords = [line.rstrip() for line in open(r'./resource/哈工大停用词表.txt', encoding='utf-8')]
    #jieba分词+去除停用词
    positive_words=[word for word in jieba.cut(positive_text) if word not in stopwords]
    negative_words=[word for word in jieba.cut(negative_text) if word not in stopwords]
    positive=' '.join(positive_words)
    negative=' '.join(negative_words)
    #生成积极和消极词汇词云
    bg1=np.array(Image.open("./resource/back1.jpg"))
    bg2=np.array(Image.open("./resource/back2.jpg"))
    wc1=WordCloud(width=512,
                 height=512,
                 scale=2,
                 mask=bg1,
                 background_color='white',
                 max_words=500,
                 repeat=True,
                 font_path="./resource/msyhbd.ttc")
    wc1.generate(positive)
    wc2=WordCloud(width=512,
                 height=512,
                 scale=2,
                 mask=bg2,
                 background_color='white',
                 max_words=500,
                 repeat=True,
                 font_path="./resource/msyhbd.ttc")
    wc2.generate(negative)
    positive_name="positive"+str(int(time.time()))+".jpg"
    negative_name="negative"+str(int(time.time()))+".jpg"
    positive_dir="./static/"+positive_name
    negative_dir="./static/"+negative_name

    wc1.to_file(positive_dir)
    wc2.to_file(negative_dir)
    positive_service_dir="http://127.0.0.1:5000/static/"+positive_name
    negative_service_dir = "http://127.0.0.1:5000/static/" + negative_name
    result_dir=[positive_dir,negative_dir]
    service_result_dir={"positive":positive_service_dir,"negative":negative_service_dir}
    return service_result_dir


if __name__ =="__main__":
    result=wordcloudAPI()
    print(result)
