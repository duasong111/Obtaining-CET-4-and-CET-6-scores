import urllib
from pprint import pprint

import requests
import json
import ssl

#解决SSL协议的问题
custom_ssl_options = {
    'keyfile': '/path/to/your/private/key.pem',
    'certfile': '/path/to/your/certificate/cert.pem',
    'ssl_version': ssl.PROTOCOL_SSLv23,
}

type_selection=input("四级输入 1 六级输入 2 :")
chinese_text = input("请输入姓名：")
encoded_text = urllib.parse.quote(chinese_text)
id_code=input("请输入证件号:")


url = "https://cachecloud.neea.cn/api/latest/results/cet"
params = {
    "km": type_selection,
    "xm": chinese_text ,
    "no": id_code,
    "source": "pc"
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Referer": "https://cjcx.neea.edu.cn/",
    "Origin": "https://cjcx.neea.edu.cn"
}

response = requests.get(url, params=params, headers=headers)
data = response.json()
if data['code'] != 404:
    Result={
        "code":200,
        "message":"获取数据成功",
        "personalInformationDetails":{
            "school":data['xx'],
            "name":urllib.parse.unquote(chinese_text),
            "ID":id_code,
            "admissionTicketNumber":data['zkzh'],
            "totalScore":data['score'],
            "hearing":data['sco_lc'],
            "read": data['sco_rd'],
            "write": data['sco_wt'],
            "scoreReportNumber":data['id'],
            "oralAdmissionTicketNumber":  "您未参加口语考试" if data['ky_sco'] == '--' else data['ky_sco'],
            "oralPerformance":"您未参加口语考试" if data['ky_zkz'] == '--' else data['ky_zkz']
        }
    }
else:
    Result={
        "code":404,
        "message":"您所提供的考试科目或个人信息有误，请核实后再查询。",
    }


pprint(Result)
