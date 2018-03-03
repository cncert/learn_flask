# encoding: utf-8

from flask import request,abort, make_response, jsonify, g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from werkzeug.security import check_password_hash
from ..models import User
from flask_jwt_extended import get_jwt_identity,jwt_required

auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth(scheme='Bearer')
# 初始化HTTPTokenAuth对象时，我们传入了”scheme=’Bearer'”。这个scheme，就是我们在发送请求时，在HTTP头”Authorization”中要用的scheme字段。
# 如： curl -X GET -H "Authorization: Bearer secret-token-1" http://localhost:5000/
multi_auth = MultiAuth(auth, token_auth)  # 多重验证
# 给其他路由添加验证
# @main.route('/')
# @multi_auth.login_required
# def index():
#     return 'Hello, %s!' % g.user


# 重写验证方法

# 发送用户名密码认证 curl -u Tom:111111 -i -X GET http://localhost:5000/api/s
@auth.verify_password
def verify_password(username,password):
    try:
        if username is None:
            abort(400)
        user = User.query.filter_by(username=username).first()
        if not user:
            return False
        password_hash = user.password_hash
        if not password_hash:
            return False
        if check_password_hash(password_hash,password):
            g.user = username
            return True
        return False
        # if username:  # 测试
        #     g.user = username
        #     return True
    except:
        return False


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access,error'}), 401)


# 发送令牌 curl -X GET -H "Authorization: Bearer secret-token-1" http://localhost:5000/api/s
@token_auth.verify_token
@jwt_required  # 使用flask_jwt_extended中的token验证，jwt_required也可以以装饰器的形式，直接加到路由函数上
def verify_token(token):
    g.user = None
    # user = User.verify_auth_token()
    # if user:
    #     g.user = user
    #     return True

    data = get_jwt_identity()  # 测试使用
    print(data,u'验证通过')
    if data:
        return True
    return False


@token_auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)
