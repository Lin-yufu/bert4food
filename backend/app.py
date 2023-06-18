from flask import Flask, request,jsonify,current_app
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pymysql
import os
from datetime import datetime
#线程池实现异步任务
from concurrent.futures import ThreadPoolExecutor
#一定要添加路径，不然找不到包
import sys
sys.path.append("./BertSentiment")
from BertSentiment import BertAPI
from WordCloud import wordcloudAPI
#线程池用于异步处理前端请求及模型推理
executor = ThreadPoolExecutor(2)
app = Flask(__name__)
CORS(app)

# 连接数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/bert?charset=utf8mb4'
# 设置是否跟踪数据库的修改情
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 数据库操作时是否显示原始SQL语句
app.config['SQLALCHEMY_ECHO'] = True

# 实例化orm框架的操作对象，后续数据库操作，都要基于操作对象来完成
db = SQLAlchemy(app)
class Feedback(db.Model):
    __tablename__="feedback"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True,nullable=False)  # 主键
    create_time=db.Column(db.String(100),nullable=False)
    comment=db.Column(db.String(100),nullable=False)
    sentiment=db.Column(db.Integer,nullable=False)
    # 该方法便于序列化对象
    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/get_feedback_list',methods=['GET'])
def getFeedbackList():
    if request.method=='GET':
        feedbackQuery=Feedback.query.all()
        feedback_list=[]
        for feedback in feedbackQuery:
            feedback_data={"id":feedback.id,"create_time":feedback.create_time,"comment":feedback.comment,"sentiment":feedback.sentiment}
            feedback_list.append(feedback_data)
        return jsonify(feedback_list)
@app.route('/get_feedback_num',methods=['GET'])
def getFeedbackNum():
    if request.method=='GET':
        negative_num=len(Feedback.query.filter_by(sentiment=0).all())
        positive_num=len(Feedback.query.filter_by(sentiment=1).all())
        feedback_num={"total":negative_num+positive_num,"negative":negative_num,"positive":positive_num}
        return jsonify(feedback_num)
@app.route('/submit_feedback',methods=['POST'])
def submitFeedback():
    if request.method=='POST':
        post_data = request.get_json()
        feedback = post_data.get('feedback')
        executor.submit(sentimentAnalysis,feedback)
        return "ok"
@app.route('/get_wordcloud',methods=['GET'])
def getWordcloud():
    if request.method=='GET':
        result_dir=wordcloudAPI()

        return jsonify(result_dir)
def sentimentAnalysis(feedback):
    #获取绝对路径，以便找到模型路径
    path = os.path.dirname(__file__)
    path = os.path.join(path, "BertSentiment")
    sentiment = BertAPI.predictAPI(feedback, path)
    print(sentiment)
    mysql = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        port=3306,
        charset='utf8mb4',
        database='bert'
    )
    db=mysql.cursor()
    time=str(datetime.now().year)+"年"+str(datetime.now().month)+"月"+str(datetime.now().day)+"日"
    comment=feedback
    sql = 'INSERT INTO feedback(create_time,comment,sentiment) values("%s","%s",%d) '%(time,comment,sentiment)
    print(sql)
    try:
        db.execute(sql)
        mysql.commit()
        print("ok")
    except Exception as e:
        print("error:",e)
        mysql.rollback()
    db.close()
    mysql.close()
if __name__ == '__main__':
    app.run()
