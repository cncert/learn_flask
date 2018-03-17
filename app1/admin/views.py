# encoding: utf-8

from . import admin
from flask import request,abort,jsonify,g,url_for,make_response, render_template
from flask_restful import Resource, reqparse, fields, marshal_with
from app1.auth.auth_exts import multi_auth
from app1 import db
from app1.models import *
from app1.utils import query_set_to_json
from flask import request,abort,jsonify,g,url_for,make_response, redirect
from flask_restful import Resource, reqparse, fields, marshal_with,marshal
from app1.models import ServiceCheckResult, IdcCheckResult, CheckDetails
from app1.emails import send_mail


class FormatDate(object):
    """
        api返回数据的字段
        """
    idc_resource_fields = {
        # 机房检查信息
        'id': fields.Integer,
        'ca_temperature': fields.Integer,
        'ca_humidity': fields.Integer,
        'two_temperature': fields.Integer,
        'two_humidity': fields.Integer,
        'five_temperature': fields.Integer,
        'five_humidity': fields.Integer,
        'check_user': fields.String,
        'on_watch': fields.String,
        'check_time': fields.String,
        'date': fields.String
    }

    service_resource_fields = {
        # 服务检查信息
        'id': fields.Integer,
        'service_name': fields.String,
        'service_state': fields.String,
        'image_url': fields.String,
        'classes': fields.String,
        'on_watch': fields.String,
        'date': fields.String
    }

    detail_resource_fields = {
        # 检查详细信息
        'id': fields.Integer,
        'hardware': fields.String,
        'system': fields.String,
        'network': fields.String,
        'service': fields.String,
        'is_handle': fields.Integer,
        'trouble_report': fields.Integer,
        'alert_source': fields.String,
        'on_watch': fields.String,
        'date': fields.String
    }


# 处理用户增删改查操作


class ServiceCheckApi(Resource):
    decorators = [multi_auth.login_required]  # 添加验证,不能放在__init__函数中
    def __init__(self):
        self.reqparse = reqparse.RequestParser()  # 获取传过来的参数
        self.reqparse.add_argument('id', type=int, location=['json', 'args', 'headers'])
        self.reqparse.add_argument('service_name', type=str, location=['json', 'args', 'headers'])
        self.reqparse.add_argument('service_state', type=str, location=['json', 'args', 'headers'])
        self.reqparse.add_argument('image_url', type=str, location=['json', 'args', 'headers'])
        self.reqparse.add_argument('classes', type=str, location=['json', 'args', 'headers'])
        self.reqparse.add_argument('on_watch', type=str, location=['json', 'args', 'headers'])
        self.reqparse.add_argument('date', location=['json', 'args', 'headers'])
        self.args = self.reqparse.parse_args()    # 前端传过来的参数全在self.args里 将获取到的参数转换为字典
        super(ServiceCheckApi, self).__init__()

    def get(self):
        data = 'no source found'
        query_data = None
        try:
            on_watch = self.args.get('on_watch', '')
            date = self.args.get('date', '')
            if not (on_watch or date) :
                query_data = ServiceCheckResult.query.all()
            if not date:
                if on_watch:
                    query_data = ServiceCheckResult.query.filter(ServiceCheckResult.on_watch.like('%%%s%%' % on_watch)).all()
            elif not on_watch:
                if date:
                    query_data = ServiceCheckResult.query.filter_by(date=date).all()

            else:
                query_data = ServiceCheckResult.query.filter_by(date=date).\
                    filter(ServiceCheckResult.on_watch.like('%%%s%%' % on_watch)).all()
            data = query_set_to_json(query_data,FormatDate.service_resource_fields)
        except Exception as e:
            data = 'search faild'
            return jsonify({'response': data}, 500)
        if not data:
            return jsonify({'response':'not found'},404)
        return jsonify({'response':data},200)


    def post(self):
        res = request.json.get('data', [])
        if len(res) == 1:
            try:
                service_check = ServiceCheckResult.from_json(res[0])
                db.session.add(service_check)
                db.session.commit()
                return {'status': 'post successful'}, 200
            except Exception as e:
                db.session.rollback()
                return {'status': 'post failed'}, 400
        elif len(res) > 1:
            try:
                service_checks = [ServiceCheckResult.from_json(item) for item in res]
                db.session.add_all(service_checks)
                db.session.commit()
                return {'status': 'post successful'}, 200
            except Exception as e:
                db.session.rollback()
                return {'status': 'post failed'}, 400
        elif len(res) == 0:
            pass
        else:
            try:
                service_check = ServiceCheckResult.from_json(self.args)
                db.session.add(service_check)
                db.session.commit()
                return {'status': 'post successful'}, 200
            except Exception as e:
                db.session.rollback()
                return {'status': 'post failed'}, 400


class IdcCheckApi(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()  # 获取传过来的参数
        self.reqparse.add_argument('id', type=int, location=['json', 'args', 'headers'])
        self.reqparse.add_argument('ca_temperature', type=str, location=['json', 'args', 'headers'])
        self.reqparse.add_argument('ca_humidity', type=str, location=['json', 'args', 'headers'])
        self.reqparse.add_argument('two_temperature', type=str, location=['json', 'args', 'headers'])
        self.reqparse.add_argument('two_humidity', type=str, location=['json', 'args', 'headers'])
        self.reqparse.add_argument('five_temperature', type=str, location=['json', 'args', 'headers'])
        self.reqparse.add_argument('five_humidity', type=str, location=['json', 'args', 'headers'])
        self.reqparse.add_argument('check_user', type=str, location=['json', 'args', 'headers'])
        self.reqparse.add_argument('check_time', type=str, location=['json', 'args', 'headers'])
        self.reqparse.add_argument('on_watch', type=str, location=['json', 'args', 'headers'])
        self.reqparse.add_argument('date', location=['json', 'args', 'headers'])
        self.reqparse.add_argument('classes', type=str,
                                   location=['json', 'args', 'headers'])
        self.args = self.reqparse.parse_args()    # 将获取到的参数转换为字典
        super(IdcCheckApi, self).__init__()

    def get(self):
        data = 'no source found'
        query_data = None
        try:
            on_watch = self.args.get('on_watch', '')
            date = self.args.get('date', '')
            if not (on_watch or date) :
                query_data = IdcCheckResult.query.all()
            if not date:
                if on_watch:
                    query_data = IdcCheckResult.query.filter(IdcCheckResult.on_watch.like('%%%s%%' % on_watch)).all()
            elif not on_watch:
                if date:
                    query_data = IdcCheckResult.query.filter_by(date=date).all()

            else:
                query_data = IdcCheckResult.query.filter_by(date=date).\
                    filter(IdcCheckResult.on_watch.like('%%%s%%' % on_watch)).all()
            data = query_set_to_json(query_data,FormatDate.idc_resource_fields)
        except Exception as e:
            data = 'search faild'
            return jsonify({'response': data}, 500)
        if not data:
            return jsonify({'response':'not found'},404)
        return jsonify({'response':data},200)


    def post(self):
        res = request.json.get('data',[])
        if len(res) == 1:
            try:
                idc_check_result = IdcCheckResult.from_json(res[0])
                db.session.add(idc_check_result)
                db.session.commit()
                return {'status': 'post successful'}, 200
            except Exception as e:
                db.session.rollback()
                return {'status': 'post failed'}, 400
        elif len(res) > 1:
            try:
                idc_check_results = [IdcCheckResult.from_json(item) for item in res]
                db.session.add_all(idc_check_results)
                db.session.commit()
                return {'status': 'post successful'}, 200
            except Exception as e:
                db.session.rollback()
                return {'status': 'post failed'}, 400
        elif len(res) == 0:
            pass
        else:
            try:
                idc_check_result = IdcCheckResult.from_json(self.args)
                db.session.add(idc_check_result)
                db.session.commit()
                return {'status': 'post successful'}, 200
            except Exception as e:
                db.session.rollback()
                return {'status': 'post failed'}, 400



class CheckDetailApi(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()  # 获取传过来的参数
        self.reqparse.add_argument('id', type=int, location=['json', 'args', 'headers'])
        self.reqparse.add_argument('hardware', type=str, location=['json', 'args', 'headers'])
        self.reqparse.add_argument('system', type=str, location=['json', 'args', 'headers'])
        self.reqparse.add_argument('network', type=str, location=['json', 'args', 'headers'])
        self.reqparse.add_argument('service', type=str, location=['json', 'args', 'headers'])
        self.reqparse.add_argument('is_handle', type=int, location=['json', 'args', 'headers'])
        self.reqparse.add_argument('is_report', type=int, location=['json', 'args', 'headers'])
        self.reqparse.add_argument('alert_source', type=int, location=['json', 'args', 'headers'])
        self.reqparse.add_argument('on_watch', type=str, location=['json', 'args', 'headers'])
        self.reqparse.add_argument('date', type=str, location=['json', 'args', 'headers'])
        self.reqparse.add_argument('classes', type=str,
                                   location=['json', 'args', 'headers'])
        self.args = self.reqparse.parse_args()    # 将获取到的参数转换为字典
        super(CheckDetailApi, self).__init__()

    def get(self):
        data = 'no source found'
        query_data = None
        try:
            on_watch = self.args.get('on_watch', '')
            date = self.args.get('date', '')
            if not (on_watch or date) :
                query_data = CheckDetails.query.all()
            if not date:
                if on_watch:
                    query_data = CheckDetails.query.filter(CheckDetails.on_watch.like('%%%s%%' % on_watch)).all()
            elif not on_watch:
                if date:
                    query_data = CheckDetails.query.filter_by(date=date).all()

            else:
                query_data = CheckDetails.query.filter_by(date=date).\
                    filter(CheckDetails.on_watch.like('%%%s%%' % on_watch)).all()
            data = query_set_to_json(query_data,FormatDate.detail_resource_fields)
        except Exception as e:
            data = 'search faild'
            return jsonify({'response': data}, 500)
        if not data:
            return jsonify({'response':'not found'},404)
        return jsonify({'response':data},200)


    def post(self):
        res = request.json.get('data', [])
        if len(res) == 1:
            try:
                check_detail = CheckDetails.from_json(res[0])
                db.session.add(check_detail)
                db.session.commit()
                return {'status': 'post successful'}, 200
            except Exception as e:
                db.session.rollback()
                return {'status': 'post failed'}, 400
        elif len(res) > 1:
            try:
                check_details = [CheckDetails.from_json(item) for item in res]
                db.session.add_all(check_details)
                db.session.commit()
                return {'status': 'post successful'}, 200
            except Exception as e:
                db.session.rollback()
                return {'status': 'post failed'}, 400
        elif len(res) == 0:
            pass
        else:
            try:
                check_detail = CheckDetails.from_json(self.args)
                db.session.add(check_detail)
                db.session.commit()
                return {'status': 'post successful'}, 200
            except Exception as e:
                db.session.rollback()
                return {'status': 'post failed'}, 400


class SendEmailApi(Resource): # 发送邮件调用接口
    def __init__(self):
        self.reqparse = reqparse.RequestParser()  # 获取传过来的参数
        self.reqparse.add_argument('date', type=str, location=['json', 'args', 'headers'])
        self.reqparse.add_argument('classes', type=str, location=['json', 'args', 'headers'])
        self.reqparse.add_argument('on_watch', type=str, location=['json', 'args', 'headers'])
        self.args = self.reqparse.parse_args()    # 将获取到的参数转换为字典
        super(SendEmailApi, self).__init__()
    def get(self):
        try:
            date = self.args.get('date','')
            classes = self.args.get('classes','')
            on_watch = self.args.get('on_watch','')
            send_mail(date,classes,on_watch)
            return jsonify({'status':200})
        except Exception as e:
            return jsonify({'status': 500})




















