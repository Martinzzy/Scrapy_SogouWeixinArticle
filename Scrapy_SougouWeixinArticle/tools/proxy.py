# -*- coding:utf-8 -*-
#author:zzy #data:2018/4/21 #Version:Python 3.6
import requests

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36"}

def get_proxy():
    res = requests.get("http://127.0.0.1:5555/random",headers=headers)
    if res.status_code == 200:
        return res.text
    else:
        return get_proxy()

