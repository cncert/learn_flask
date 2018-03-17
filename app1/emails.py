# encoding: utf-8

# encoding: utf-8

import requests
from flask import g,render_template,jsonify, url_for
from flask_mail import Message
from config import config
from app1 import mail
import time


def send_mail(date, classes, on_watch):
    """邮件发送
    """
    ret = {}
    try:
        flag = True
        # 拼装为字典，渲染到前段页面
        service_data = requests.get(
            url_for('servicecheckapi', _external=True, date=date, on_watch=on_watch)).json()
        if service_data[0]['response']=='not found':
            while flag:  # 该循环是为了解决多线程运行时，从前端获取数据的线程未执行完，发送邮件的线程就执行了，导致发送的邮件数据为空问题
                service_data = requests.get(
                    url_for('servicecheckapi', _external=True, date=date,
                            on_watch=on_watch)).json()
                time.sleep(0.5)
                if service_data[0]['response'] != 'not found':
                    flag = False

        idc_data = requests.get(
            url_for('idccheckapi', _external=True, date=date, on_watch=on_watch)).json()
        detail_data = requests.get(
            url_for('checkdetailapi', _external=True, date=date, on_watch=on_watch)).json()
        content = {
            'service_data': [item for item in service_data[0]['response']],
            'idc_data': [item for item in idc_data[0]['response']],
            'detail_data': [item for item in detail_data[0]['response']]
        } # 从数据库获取到当天值班数据
        mail_content = render_template('report_template.html', message=content, date=date, classes=classes)
        msg = Message(subject=date + ' ' + classes + ' 交班记录', recipients=['xx@xx.cn'])
        # 邮件内容会以文本和html两种格式呈现，而你能看到哪种格式取决于你的邮件客户端。
        msg.body = '交班成功'
        msg.html = mail_content
        mail.send(msg)
        ret['massage'] = "email send successful"

    except (IOError,Exception) as e:
        ret['massage'] = "email send exception"
    return jsonify(ret)

