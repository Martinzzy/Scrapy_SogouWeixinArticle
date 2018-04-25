# -*- coding:utf-8 -*-
#author:zzy #data:2018/4/21 #Version:Python 3.6
import hashlib
def get_md5(url):
    if isinstance(url,str):
        url.encode('utf-8')
    m= hashlib.md5()
    m.update(url.encode('utf-8'))
    return m.hexdigest()