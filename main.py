# coding=gbk
from bs4 import BeautifulSoup
#from flask import jsonify
import random
import time
import requests#����ץȡ��ҳԴ����
import http.client
import socket

#���ڻ�ȡ���������html���루�ٶ���վ��
def get_content1(url , data = None):
    #header��Ŀ����ģ�����������
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
            #requests.get()���url����˵�response����
            req = requests.get(url, headers = header, timeout = timeout)
            req.encoding = 'utf-8'
            break
        #socket.timeout ��HttpClient �Ѿ����ӵ���Ŀ����������ȴ��������Ӧ���ݵĳ�ʱʱ��
        except socket.timeout as e:
            print( '3:', e)
            #�����ʱ�ˣ������ͣ7-16s,�ٷ�������
            time.sleep(random.choice(range(7,16)))
        #����޷����Ϸ�����
        except socket.error as e:
            print( '4:', e)
            time.sleep(random.choice(range(20, 60)))

        except http.client.BadStatusLine as e:
            print( '5:', e)
            time.sleep(random.choice(range(30, 80)))
        #����������;��ס
        except http.client.IncompleteRead as e:
            print( '6:', e)
            time.sleep(random.choice(range(5, 15)))

    return req.text


#���ڻ�ȡ���������html���루�ٶȰٿ���վ��
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


#���ݹؼ������滨������
def get_data_flower(keyword):
    #���ݹؼ���ȷ����������
    url = "https://baike.baidu.com/item/"
    #���û�����������ר�Ż�(�������������ж�)
    if '��' in keyword and '��' in keyword and '��' not in keyword:
        keyword = '��' + keyword
    if '��' not in keyword:
        keyword = keyword + '��'
    url = url + keyword
    html_doc = get_content2(url)

    #�ֵ�����Ϣ
    dic =dict()
    #������������bs
    bs = BeautifulSoup(html_doc, 'html.parser')
    body = bs.find('body')
    if body.find('div',{'class':'para', 'label-module': 'para'}) != None:
       div = body.find('div',{'class':'para', 'label-module': 'para'})
       introduce = div.text
       introduce = introduce.replace(u'\xa0', u'')#bgk�����޷�����\xa0,��˰������˵�
       dic['introduce'] = introduce
       #print(introduce)#��ȡ���Ľ���
    elif body.find('div', {'class': "c-font-normal c-color-text"}) != None:
       div = body.find('div', {'class': "c-font-normal c-color-text"})
       introduce = div.text
       #print(introduce)
       dic['introduce'] = introduce

    #ͬ�����������Ϣ
    url_huayu = "https://baike.baidu.com/item/"
    url_huayu = url_huayu + keyword + "����"
    html_doc1 = get_content2(url_huayu)
    bs = BeautifulSoup(html_doc1, 'html.parser')
    body = bs.find('body')
    #��������ṹ��һ������˼Ӹ������ж�
    if  body.find('div', {"class": "lemma-summary", "label-module": "lemmaSummary"}) != None:
        if div.find('div', {"class": "para", "label-module": "para"}) != None:
           div = div.find('div', {"class": "para", "label-module": "para"})
           huayu_info = div.text
           #print(huayu_info)
           dic['huayu_info'] = huayu_info

    #�����û�����Ĳ���ȷ������
    url = "https://www.baidu.com/"
    url_new = url +'s?'+"&"+'wd='+ keyword + '����'
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


#���ݹؼ������滨��ͼƬ
def get_picture_flower(keyword):
    # ���ݹؼ���ȷ����������
    url = "https://www.so.com/s?q="
    if '��' not in keyword:
        keyword = keyword + '��'
    url = url + keyword + 'ͼƬ'
    html_doc = get_content1(url)

    # ������������bs
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


#��ȡ���л��Ļ����������
def get_data_all_flowers(url):
    html = get_content2(url)
    flower_name = dict()
    #flower_name_all = dict()
    bs = BeautifulSoup(html, "html.parser")  # ����BeautifulSoup����
    body = bs.body  # ��ȡbody����
    flag = 1
    tables = body.find_all('table', {'log-set-param': 'table_view'})  # �ҵ����е�table��ǩ
    for  a_table in tables:

         if flag == 1:#õ��Ĺ�����������ͬ
             trs = a_table.find_all('tr', limit=2)  # ��ȡ����tr����
             count = 0
             for tr in trs:
                 if count == 0:
                     count = 1
                     continue
                 tds = tr.find_all('td')  # ��ȡtr���ֵ����е�td
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
                 trs = a_table.find_all('tr', limit = 2)  # ��ȡ����tr����
                 count = 0
                 for tr in trs:
                     if count == 0:
                        count = 1
                        continue
                     tds = tr.find_all('td')  # ��ȡtr���ֵ����е�td
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
#������д��csv�ļ���
'''def write_data(data, name):
   with open(name, 'w', newline='') as f:
        writer = csv.writer(f)
        for row in data.items():
            writer.writerow(row)
'''



#������йؼ����Ƽ��ʵ��Ļ�
def recommend_system(emotion):
    url ='https://baike.baidu.com/item/%E8%8A%B1%E8%AF%AD/100496'
    result = get_data_all_flowers(url)
    result['������'] = '���ˡ������İ�����Ǹ����ڡ��Ҹ�����'
    recommendation = dict()

    count = get_data_all_flowers(url)
    count['������'] = '���ˡ������İ�����Ǹ����ڡ��Ҹ�����'
    for i in count.keys():
        count[i] = 0

    #������Ĺؼ��ֽ��г���
    for ch in ',����.\��':
        emotion = str(emotion)
        emotion = emotion.replace(ch, " ")
        #emotion = list(emotion)
        emotion = emotion.split(' ')

    for i in emotion:
        for j in result.items():
            length = len(i)
            for k in range(0,length):
               #������Ҳ��Ƚϱ�׼
               if i[k] in j[1]:
                   count[j[0]] = count[j[0]] + 1
    #���ؼ���ƥ��ȴ�С��������
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
        print("Ŀ¼: {},����: {};".format(i, result_dict[i]))
        print('\n')
    result_link = get_picture_flower(keyword)
    for i in result_link:
        print(i)

    emotion = input("Search emotion you will get flowers recommended   ")
    result_dict2 = recommend_system(emotion)
    for i in result_dict2:
        print("�Ƽ�����: {},ԭ��: {};".format(i, result_dict2[i]), end=" ")
        print('\n')
