# encoding: utf-8
# 主要用来定义工具函数
from flask_restful import marshal


def query_set_to_json(query_data,resource_fields):
    """
    该函数将从数据库中查询出的数据对象直接转换为字典
    :param query_data: 数据对象
    :param resource_fields: 格式化字段
    :return:
    """
    if isinstance(query_data,list):
        data = [marshal(query_set, resource_fields) for query_set in query_data]
    else:
        data = marshal(query_data, resource_fields)
    return data