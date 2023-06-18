from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
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

if __name__=="__main__":
    db.drop_all()
    db.create_all()