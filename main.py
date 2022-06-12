# coding=gbk
from bs4 import BeautifulSoup
#from flask import jsonify
import random
import time
import requests#用于抓取网页源代码
import http.client
import socket

#用于获取单个花语的html代码（百度网站）
def get_content1(url , data = None):
    #header的目的是模拟浏览器访问
    header={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    }
    timeout = random.choice(range(80, 180))
    while True:
        try:
            #requests.get()获得url服务端的response代码
            req = requests.get(url, headers = header, timeout = timeout)
            req.encoding = 'utf-8'
            break
        #socket.timeout 是HttpClient 已经连接到了目标服务器，等待服务端响应数据的超时时间
        except socket.timeout as e:
            print( '3:', e)
            #如果超时了，就随机停7-16s,再发送请求
            time.sleep(random.choice(range(7,16)))
        #如果无法连上服务器
        except socket.error as e:
            print( '4:', e)
            time.sleep(random.choice(range(20, 60)))

        except http.client.BadStatusLine as e:
            print( '5:', e)
            time.sleep(random.choice(range(30, 80)))
        #返回数据中途卡住
        except http.client.IncompleteRead as e:
            print( '6:', e)
            time.sleep(random.choice(range(5, 15)))

    return req.text


#用于获取单个花语的html代码（百度百科网站）
def get_content2(url , data = None):
    header={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.30'
    }
    timeout = random.choice(range(80, 180))
    while True:
        try:
            req = requests.get(url, headers = header,timeout = timeout)
            req.encoding = 'utf-8'
            break

        except socket.timeout as e:
            print( '3:', e)
            time.sleep(random.choice(range(8,15)))

        except socket.error as e:
            print( '4:', e)
            time.sleep(random.choice(range(20, 60)))

        except http.client.BadStatusLine as e:
            print( '5:', e)
            time.sleep(random.choice(range(30, 80)))

        except http.client.IncompleteRead as e:
            print( '6:', e)
            time.sleep(random.choice(range(5, 15)))

    return req.text


#根据关键字爬虫花的数据
def get_data_flower(keyword):
    #根据关键字确定搜索域名
    url = "https://baike.baidu.com/item/"
    #对用户输入名进行专门化(紫罗兰的特殊判断)
    if '罗' in keyword and '兰' in keyword and '紫' not in keyword:
        keyword = '紫' + keyword
    if '花' not in keyword:
        keyword = keyword + '花'
    url = url + keyword
    html_doc = get_content2(url)

    #字典存放信息
    dic =dict()
    #建立解析对象bs
    bs = BeautifulSoup(html_doc, 'html.parser')
    body = bs.find('body')
    if body.find('div',{'class':'para', 'label-module': 'para'}) != None:
       div = body.find('div',{'class':'para', 'label-module': 'para'})
       introduce = div.text
       introduce = introduce.replace(u'\xa0', u'')#bgk编码无法解析\xa0,因此把它过滤掉
       dic['introduce'] = introduce
       #print(introduce)#获取花的介绍
    elif body.find('div', {'class': "c-font-normal c-color-text"}) != None:
       div = body.find('div', {'class': "c-font-normal c-color-text"})
       introduce = div.text
       #print(introduce)
       dic['introduce'] = introduce

    #同理，爬花语的信息
    url_huayu = "https://baike.baidu.com/item/"
    url_huayu = url_huayu + keyword + "花语"
    html_doc1 = get_content2(url_huayu)
    bs = BeautifulSoup(html_doc1, 'html.parser')
    body = bs.find('body')
    #由于爬虫结构不一样，因此加个条件判断
    if  body.find('div', {"class": "lemma-summary", "label-module": "lemmaSummary"}) != None:
        if div.find('div', {"class": "para", "label-module": "para"}) != None:
           div = div.find('div', {"class": "para", "label-module": "para"})
           huayu_info = div.text
           #print(huayu_info)
           dic['huayu_info'] = huayu_info

    #根据用户输入的参数确定域名
    url = "https://www.baidu.com/"
    url_new = url +'s?'+"&"+'wd='+ keyword + '花语'
    #print(url_new)
    html_doc = get_content1(url_new)
    bs = BeautifulSoup(html_doc, 'html.parser')
    body = bs.find('body')
    if body.find('div', {'class':'c-font-middle c-color-text wenda-abstract-new_1p73z'}) != None:
       div = body.find('div', {'class': 'c-font-middle c-color-text wenda-abstract-new_1p73z'})
       huayu_info_2 = div.text
       #print(huayu_info_2)
       dic['huayu_info2']=huayu_info_2

    elif body.find('div', {'class': "c-font-middle c-color-text wenda-abstract-new_1p73z"}) != None:
       div = body.find('div', {'class': "c-font-middle c-color-text wenda-abstract-new_1p73z"})
       huayu_info_2 = div.text
       #print(huayu_info_2)
       dic['huayu_info2'] = huayu_info_2

    elif body.find('div', {'class': "answer-property_1ExvD"}) != None:
       div = body.find('div', {'class': "answer-property_1ExvD"})
       huayu_info_2 = div.text
       #print(huayu_info_2)
       dic['huayu_info2'] = huayu_info_2
    #print(dic)
    #return jsonify(dic)
    return dic


#根据关键字爬虫花的图片
def get_picture_flower(keyword):
    # 根据关键字确定搜索域名
    url = "https://www.so.com/s?q="
    if '花' not in keyword:
        keyword = keyword + '花'
    url = url + keyword + '图片'
    html_doc = get_content1(url)

    # 建立解析对象bs
    bs = BeautifulSoup(html_doc, 'html.parser')
    body = bs.find('body')
    a_all = body.find_all('a', {'target':"_blank", 'class':"mh-img-link"})
    link_all = list()
    for a in a_all:
        if '360' in a.get('href'):
            link = a.get('href')
            link_all.append(link)
            #print(link)
    #return jsonify(link_all)
    return link_all


#爬取所有花的花语的主函数
def get_data_all_flowers(url):
    html = get_content2(url)
    flower_name = dict()
    #flower_name_all = dict()
    bs = BeautifulSoup(html, "html.parser")  # 创建BeautifulSoup对象
    body = bs.body  # 获取body部分
    flag = 1
    tables = body.find_all('table', {'log-set-param': 'table_view'})  # 找到所有的table标签
    for  a_table in tables:

         if flag == 1:#玫瑰的规则与其它不同
             trs = a_table.find_all('tr', limit=2)  # 获取所有tr部分
             count = 0
             for tr in trs:
                 if count == 0:
                     count = 1
                     continue
                 tds = tr.find_all('td')  # 获取tr部分的所有的td
                 for i in range(3):
                     div = tds[i].find('div')
                     if i == 0:
                         b = div.find('b')
                         name = b.find('a').string
                     elif i == 1:
                         meaning = div.string
                         break
                 flower_name[name] = meaning
                 #print(flag, end = ' ')
                 #print(flower_name)
                 flag = flag + 1
                 #flower_name_all.append(flower_name)
         elif flag == 2 or flag == 15 or flag == 40:
                 flag = flag + 1
                 continue

         else:
                 trs = a_table.find_all('tr', limit = 2)  # 获取所有tr部分
                 count = 0
                 for tr in trs:
                     if count == 0:
                        count = 1
                        continue
                     tds = tr.find_all('td')  # 获取tr部分的所有的td
                     for i in range(1, 3):
                         div = tds[i].find('div')
                         if i == 1:
                            b = div.find('b')
                            if b.find('a') == None:
                                name = b.string
                            else:
                                name = b.find('a').string
                         elif i == 2:
                            meaning = div.string
                            break
                 flower_name[name] = meaning
                 flag = flag + 1
                 #flower_name_all.append(flower_name)
         if flag == 39:
             break


    return flower_name
    #return  jsonify(flower_name)
#将数据写到csv文件里
'''def write_data(data, name):
   with open(name, 'w', newline='') as f:
        writer = csv.writer(f)
        for row in data.items():
            writer.writerow(row)
'''



#根据情感关键字推荐适当的花
def recommend_system(emotion):
    url ='https://baike.baidu.com/item/%E8%8A%B1%E8%AF%AD/100496'
    result = get_data_all_flowers(url)
    result['风信子'] = '悲伤、忧郁的爱、道歉、后悔、幸福美满'
    recommendation = dict()

    count = get_data_all_flowers(url)
    count['风信子'] = '悲伤、忧郁的爱、道歉、后悔、幸福美满'
    for i in count.keys():
        count[i] = 0

    #对输入的关键字进行除杂
    for ch in ',，。.\、':
        emotion = str(emotion)
        emotion = emotion.replace(ch, " ")
        #emotion = list(emotion)
        emotion = emotion.split(' ')

    for i in emotion:
        for j in result.items():
            length = len(i)
            for k in range(0,length):
               #近义字也算比较标准
               if i[k] in j[1]:
                   count[j[0]] = count[j[0]] + 1
    #按关键字匹配度从小到大排序
    count = sorted(count.items(), key=lambda x:x[1], reverse=True)
    #print(count)
    flag = 1
    recommendation[count[0][0]] = result[count[0][0]]

    while True:
         if count[flag][1] == count[0][1]:
            recommendation[count[flag][0]] = result[count[flag][0]]
            flag = flag + 1
            #print(count[flag][1])
         elif flag > 5:
            break
         else:
            break
    #return jsonify(recommendation)
    return recommendation


if __name__ == "__main__":
    keyword = input("Search flower you will get its meaning  ")
    result_dict = get_data_flower(keyword)
    for i in result_dict:
        print("目录: {},内容: {};".format(i, result_dict[i]))
        print('\n')
    result_link = get_picture_flower(keyword)
    for i in result_link:
        print(i)

    emotion = input("Search emotion you will get flowers recommended   ")
    result_dict2 = recommend_system(emotion)
    for i in result_dict2:
        print("推荐花朵: {},原因: {};".format(i, result_dict2[i]), end=" ")
        print('\n')
