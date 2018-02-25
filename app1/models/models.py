# encoding: utf-8
from app1 import db

# # 该db用于创建表的类, 如：
# class Art(db.Model):
#     __tablename__ = 'artile'  在数据库中显示的表名
#     id = db.Column(db.Integer,primary_key=True,autoincrement=True)
#     title = db.Column(db.String(100),nullable=False)


class Art(db.Model):
    __tablename__ = 'artile'  #在数据库中显示的表名
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
