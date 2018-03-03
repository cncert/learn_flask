# encoding: utf-8
from app1 import db
import datetime

# # 该db用于创建表的类, 如：
# class Art(db.Model):
#     __tablename__ = 'artile'  在数据库中显示的表名
#     id = db.Column(db.Integer,primary_key=True,autoincrement=True)
#     title = db.Column(db.String(100),nullable=False)

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from flask_jwt_extended import (
    JWTManager, jwt_optional, create_access_token,
    get_jwt_identity
)


class User(UserMixin, db.Model):
    # User继承UserMixin和db.Model类的功能属性
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    ###加入email属性，用来储存用户的email
    username = db.Column(db.String(64),unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    token = db.Column(db.String(256))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        # 生成密码的哈希值
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 一般token是存放到redis里的，这里没有装Redis
    # 注意 ：存到redis里要设置过期时间：
    def generate_auth_token(self,username, uid):  # 生成token
        payload = {'username': username, 'id': uid}
        expires = datetime.timedelta(days=365)
        access_token = create_access_token(identity=payload, fresh=False, expires_delta=False)  # 生成token,关闭过期时间
        return access_token

    @staticmethod
    def verify_auth_token():  # 验证token
        try:
            data = get_jwt_identity()  # 解析token
        except :
            return None  # valid token, but expired
        user = User.query.get(data['username'])
        return user

    def __repr__(self):
        return '<User %r>' % self.username


class Art(db.Model):
    __tablename__ = 'artile'  #在数据库中显示的表名
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(100),nullable=False)


