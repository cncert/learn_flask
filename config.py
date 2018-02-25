# encoding: utf-8
#  'mysql+pymysql://lmapp:lmapp@localhost/smp'
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24) # SECRET_KEY作用：给session中的数据
    # 加密用的盐.如：session['username'] = 'wt', SECRET_KEY = 'abc',
    # 则session加盐后，session['username'] = 'awbtc', 然后再加密
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    @staticmethod  # 使用类名可以直接调用该方法
    def init_app(app):
        pass


class DevelopmentConfig(Config):  # 开发环境
    DEBUG = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    HOSTNAME = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'learn'
    USERNAME = 'root'
    PASSWORD = '111111'
    DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
    SQLALCHEMY_DATABASE_URI = DB_URI


class TestingConfig(Config):  # 测试环境
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):  # 生产环境
    HOSTNAME = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'learn'
    USERNAME = 'root'
    PASSWORD = '111111'
    DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
    SQLALCHEMY_DATABASE_URI = DB_URI


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


