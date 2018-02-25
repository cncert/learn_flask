# encoding: utf-8

from flask_script import Manager

DBmanager = Manager()  # 由于本文件不是运行主app，所以
# 就不用初始化app了

@DBmanager.command
def init():
    print('初始化数据库')

@DBmanager.command
def migrate():
    print('数据库迁移成功')
