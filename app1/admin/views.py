# encoding: utf-8

from . import admin
from flask import request,abort,jsonify,g,url_for,make_response
from flask_restful import Resource, reqparse, fields, marshal_with
from app1.auth.auth_exts import multi_auth
from app1 import db
from app1.models import *


@admin.route('/c', methods=['GET', 'POST'])
def ad():
    return 'yes'


@admin.route('/adduser', methods = ['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments
    if User.query.filter_by(username = username).first() is not None:
        abort(400) # existing user
    user = User(username = username)
    user.hash_password(password)
    user.generate_auth_token(username)
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'username': user.username }), 201, {'Location': url_for('get_user', id = user.id, _external = True)}


# 格式化返回的数据
class Response(object):
    def __init__(self,args):
        self.id = args.get('id','')
        self.title = args.get('title','')
        self.description = args.get('description','')
        self.done = args.get('done','')
        self.status = args.get('status',200)


# 处理用户增删改查操作
class UserApi(Resource):
    decorators = [multi_auth.login_required]  # 添加验证,不能放在__init__函数中
    response = {
        'id': fields.Integer,
        'title': fields.String,
        'description': fields.String,
        'done': fields.String,
        'status': fields.Integer
    }

    def __init__(self):
        self.reqparse = reqparse.RequestParser()  # 获取传过来的参数
        # 以下是对获取到的参数进行验证，type=str,表明期望得到的参数是整数类型，如果不是则会返回
        # 错误信息{'message': {'id': "invalid literal for int() with base 10: '
        self.reqparse.add_argument('id', type=int, location=['json', 'args', 'headers'])
        self.reqparse.add_argument('title', type=str, location=['json', 'args', 'headers'])
        self.reqparse.add_argument('description', type=str, location=['json', 'args', 'headers'])
        self.reqparse.add_argument('done', type=bool, location=['json', 'args', 'headers'])
        self.args = self.reqparse.parse_args()  # # 将获取到的参数转换为字典

        super(UserApi, self).__init__()

    def get(self, id=None):
        if id:
            return jsonify({"res": id})
        return jsonify({"res": 'hellddosssssss'})

    def post(self,id=None):
        if id:
            return jsonify({"res": 'invalid operate'})
        return jsonify({"res": 'add 1 rows'})

    @marshal_with(response)  # # 格式化返回的数据
    def put(self, **kwargs):
        # 前端传过来的参数全在self.args里
        users = [{'id':1,'title':'put'},{'id':"2",'title':'put2'}]
        user_list = filter(lambda t: t['id'] == self.args['id'], users)
        user_list = list(user_list)
        if len(user_list) == 0:
            abort(404)
        user = user_list[0]
        # self.args为 {'id': 1, 'title': 'ppppppppppp', 'description': None, 'done': None}
        for k, v in self.args.items():  # 执行更新操作
            if v is not None:
                user[k] = v
            else:
                user['ststus'] = 404
        return Response(user)

    def delete(self, id=None):
        if id:
            return jsonify({"res": 'delete %s success' % id})
        abort(404)



