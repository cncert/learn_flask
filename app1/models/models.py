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


class ServiceCheckResult(db.Model):
    """
    存储服务监控信息
    service_name：服务名
    service_state：服务状态
    image_url：图片存放路径
    classes：班次（分为‘白班’、‘夜班’）
    on_watch：值班人员
    date：交班时间

    """
    __tablename__ = 'service_check_result'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_name = db.Column(db.String(16))
    service_state = db.Column(db.String(32))
    image_url = db.Column(db.String(256), nullable=True)
    classes = db.Column(db.String(32))
    on_watch = db.Column(db.String(16))
    date = db.Column(db.String(32))

    def __repr__(self):
        return '<ServiceCheckResult %r>' % self.service_name

    @staticmethod
    def from_json(json_post):
        """由用户post的json数据返回ServiceCheckResult对象"""

        service_name = json_post.get('service_name')
        service_state = json_post.get('service_state')
        image_url = json_post.get('image_url')
        classes = json_post.get('classes')
        on_watch = json_post.get('on_watch')
        date = json_post.get('date')
        return ServiceCheckResult(service_name=service_name,
                                  service_state=service_state,
                                  image_url=image_url,
                                  classes=classes,
                                  on_watch=on_watch,
                                  date=date)


class IdcCheckResult(db.Model):
    """
    存储巡检结果:
    temperature:温度
    humidity:湿度
    idc:机房
    check_user:巡检人员
    check_time:巡检时间
    on_watch：值班人员
    date：交班日期
    """
    __tablename__ = 'idc_check_result'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ca_temperature = db.Column(db.String(16))
    ca_humidity = db.Column(db.String(16))
    two_temperature = db.Column(db.String(16))
    two_humidity = db.Column(db.String(16))
    five_temperature = db.Column(db.String(16))
    five_humidity = db.Column(db.String(16))
    check_user = db.Column(db.String(32))
    check_time = db.Column(db.DATETIME())
    classes = db.Column(db.String(32))
    on_watch = db.Column(db.String(16))
    date = db.Column(db.String(32))

    def __repr__(self):
        return '<IdcCheckResult %r>' % self.__tablename__

    @staticmethod
    def from_json(json_post):
        """由用户post的json数据返回IdcCheckResult对象"""

        ca_temperature = json_post.get('ca_temperature')
        ca_humidity = json_post.get('ca_humidity')
        two_temperature = json_post.get('two_temperature')
        two_humidity = json_post.get('two_humidity')
        five_temperature = json_post.get('five_temperature')
        five_humidity = json_post.get('five_humidity')
        check_user = json_post.get('check_user')
        check_time = json_post.get('check_time')
        on_watch = json_post.get('on_watch')
        date = json_post.get('date')
        classes = json_post.get('classes')
        return IdcCheckResult(ca_temperature=ca_temperature,
                              ca_humidity=ca_humidity,
                              two_temperature=two_temperature,
                              two_humidity=two_humidity,
                              five_temperature=five_temperature,
                              five_humidity=five_humidity,
                              check_user=check_user,
                              check_time=check_time,
                              on_watch=on_watch,
                              date=date,
                              classes=classes)


class CheckDetails(db.Model):
    """
    hardware:硬件
    system：系统
    network：网络
    service：服务
    is_handle：是否处理
    is_report：故障报告
    alert_source：告警源
    on_watch：值班人员
    date：交班日期
    """
    __tablename__ = 'check_details'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hardware = db.Column(db.Text())
    system = db.Column(db.Text())
    network = db.Column(db.Text())
    service = db.Column(db.Text())
    is_handle = db.Column(db.Integer, default=1)
    is_report = db.Column(db.Integer, default=0)
    alert_source = db.Column(db.String(32))
    classes = db.Column(db.String(32))
    on_watch = db.Column(db.String(16))
    date = db.Column(db.String(32))

    def __repr__(self):
        return '<CheckDetails %r>' % self.__tablename__

    @staticmethod
    def from_json(json_post):
        """由用户post的json数据返回checkdetail对象"""

        hardware = json_post.get('hardware')
        system = json_post.get('system')
        network = json_post.get('network')
        service = json_post.get('service')
        is_handle = json_post.get('is_handle')
        is_report = json_post.get('is_report')
        alert_source = json_post.get('alert_source')
        on_watch = json_post.get('on_watch')
        date = json_post.get('date')
        classes = json_post.get('classes')
        return CheckDetails(hardware=hardware,
                            system=system,
                            network=network,
                            service=service,
                            is_handle=is_handle,
                            is_report=is_report,
                            alert_source=alert_source,
                            on_watch=on_watch,
                            date=date,
                            classes=classes)




