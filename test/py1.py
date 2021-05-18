from urllib import request
from urllib import parse
import json

word=input("请输入需要翻译的中文：")
Request_URL="http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"
form_data={}
form_data['i']=word
form_data['from'] = 'AUTO'
form_data['to'] = 'AUTO'
form_data['smartresult'] = 'dict'
form_data['doctype']='json'
form_data['version']='2.1'
form_data['keyfrom']='fanyi.web'
form_data['action']='FY_BY_CLICKBUTTION'
form_data['typoResult']='false'

data=parse.urlencode(form_data).encode('utf-8')
response=request.urlopen(Request_URL,data)
html=response.read().decode('utf-8')
translate_results = json.loads(html)
# 找到翻译结果
translate_result = translate_results["translateResult"][0][0]['tgt']
# 打印翻译结果
print("翻译的结果是：%s" % translate_result)