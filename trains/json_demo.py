# -*- coding: utf-8 -*-
import json

print(json.__file__)
# Python 字典类型转换为 JSON 对象
data1 = {
    'no': 1,
    'name': 'Runoob',
    'url': 'http://www.runoob.com'
}

json_str = json.dumps(data1)
print("Python 原始数据：", repr(data1))
print("JSON 对象：", json_str)

a = '{"next":true}'
b = json.loads(a)
ne = b['next']
print(ne)
if ne:
    print("yeeeeees")
