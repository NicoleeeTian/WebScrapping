#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 18 10:00:45 2021

@author: testad
"""

#-*- coding: UTF-8 -*-
# encoding:utf-8
import json
import urllib
import requests
import datetime
import pdfplumber
from PyPDF2 import PdfFileReader, PdfFileWriter


def gettoken(client_id,client_secret):
    url='http://webapi.cninfo.com.cn/api-cloud-platform/oauth2/token'
    post_data="grant_type=client_credentials&client_id=%s&client_secret=%s"%(client_id,client_secret)
    post_data={"grant_type":"client_credentials",
               "client_id":client_id,
               "client_secret":client_secret
               }
    req = requests.post(url, data=post_data)
    tokendic = json.loads(req.text)
    return tokendic['access_token']

def getPage(url):
    response = urllib.request.urlopen(url)
    #print ("Results：",response.read().decode('utf-8'))
    return response.read().decode('utf-8')


token = gettoken('YutGEvIratw1rXgp9EjtaRUgFI7g77Yq','WINTrrbrGJbkF6ODApPPRHJ5eB3qrS6U')  #这部分xxxxx分别代表的是个人中心-我的凭证下的Access Key,Access Secret,请自己填写
company_name = input("请输入公司代码:")
url = 'http://webapi.cninfo.com.cn/api/info/p_info3015?scode='+company_name+'&sdate=20210101&edate=20210501&access_token='+token
print (datetime.datetime.now())
response = getPage(url)
response = json.loads(response)
result =''

for record in response['records']: 
    if '2020年' and '年度报告' in record['F002V']:
        if ('摘要' not in record['F002V']) and ('关于' not in record['F002V']) and ('英文版' not in record['F002V']):
            print(record['F002V'])
            result = record['F003V']
            print(result) 
# local file 如果有乱码的话自行删除
i = result.rindex('/')
new_result= result[i+1:]
print("local_file_address:", new_result)


with pdfplumber.open(new_result) as pdf: 
    content = ''
        #len(pdf.pages)为PDF文档页数
    for i in range(len(pdf.pages)):
        #pdf.pages[i] 是读取PDF文档第i+1页
        page = pdf.pages[i]
        #page.extract_text()函数即读取文本内容，下面这步是去掉文档最下面的页码
        page_content = '\n'.join(page.extract_text().split('\n')[:-1])
        content = content + page_content
        #print(content)
        
s = content.split('第四节 ')[1].split('第六节 ')[0]
start = s.split('第五节 ')[0]
end= s.split('第五节 ')[1]
print('截取目录：')
print()
print(s)
index_start = start.rindex('.')
index_end = end.rindex('.')
string_start_page = start[index_start+2:]
string_end_page = end[index_end+2:]
        
# 开始页
start_page = int(string_start_page)
print(start_page)

# 截止页
end_page = int(string_end_page)
print(end_page)

output = PdfFileWriter()
pdf_file = PdfFileReader(open(new_result, "rb"))
pdf_pages_len = pdf_file.getNumPages()

# 保存input.pdf中的start_page-end_page页到output.pdf
for i in range(start_page, end_page):
    output.addPage(pdf_file.getPage(i))

outputStream = open("output"+new_result[-5:]+".pdf", "wb")
output.write(outputStream)