# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time
import json

cookie = '__jdu ... 26.1683600056' # 替换成自己的 cookie
headers = { # 通用头
    'authority': 'club.jd.com',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'referer': 'https://club.jd.com/myJdcomments/saveCommentSuccess.action',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
}

headers2 = { # 提交评价头
    'authority': 'club.jd.com',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://club.jd.com',
    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

def all_appraisal():
    appraisal = {}
    url = "https://club.jd.com/myJdcomments/myJdcomment.action?sort=0"
    headers['cookie'] = cookie
    req = requests.get(url, headers=headers)
    print(req.text)
    soup = BeautifulSoup(req.text, "html.parser")
    url = soup.find('ul', class_='tab-trigger')
    with open("index.html", "w", encoding='utf-8') as f:
        f.write(req.text)
    for li in url.find_all('li'):
        contents = li.a.text
        b = li.b
        if b != None:
            appraisal[contents] = int(b.text)
    return appraisal
    
def be_evaluated_test():
    file = open("index.html", 'r', encoding='utf-8')
    soup = BeautifulSoup(file.read(), "html.parser")
    file.close()
    table = soup.find('table', class_ = 'td-void order-tb')
    if not table:
        print("没有记录了")
        return
        
    tbodys = table.find_all('tbody')
    for order in tbodys:
        products = order.findAll('div', class_='p-name')
        for p in products:
            pname = p.a.text
            print(pname)

def be_evaluated():
    '''
    待评价
    '''
    over_oids = []
    while True:
        url = 'https://club.jd.com/myJdcomments/myJdcomment.action?sort=0&page=1'
        headers['cookie'] = cookie
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.text, "html.parser")
        table = soup.find('table', class_ = 'td-void order-tb')
        if not table:
            print("没有记录了")
            break
            
        tbodys = table.find_all('tbody')
        overcount = 0
        for order in tbodys:
            oid = order.find('span', class_="number").a.text
            if oid in over_oids:
                overcount += 1
                continue

            products = order.findAll('div', class_='p-name')
            for p in products:
                product = p.a
                pname = product.text
                pid=product['href'].replace('//item.jd.com/', '').replace('//book.jd.com/', '').replace('.html', '')
                content = pname + '，东西质量非常好，与卖家描述的完全一致，非常满意,真的很喜欢，完全超出期望值，发货速度非常快，包装非常仔细、严实，物流公司服务态度很好，运送速度很快，很满意的一次购物'
                

                saveProductComment_url = "https://club.jd.com/myJdcomments/saveProductComment.action"
                saveProductComment_data = {
                    'orderId': oid,
                    'productId': pid,  
                    'score': '5',
                    'content': bytes(content, encoding="gbk"),  
                    'saveStatus': '1',
                    'anonymousFlag': '1'
                }
                headers2['referer'] = f'https://club.jd.com/myJdcomments/orderVoucher.action?ruleid={oid}'
                headers2['cookie'] = cookie
                resp = requests.post(saveProductComment_url, headers=headers2, data=saveProductComment_data)
                if resp.status_code == 200:
                    over_oids.append(oid)
                    print(pname, "评价完成")
                else:
                    print(resp.status_code, resp.text)
                    print(pname, "评价失败")
                time.sleep(5)

        if overcount >= len(tbodys):
            print("有用记录了，或者记录无法执行过去")
            break
        else:
            print('准备翻页……')

def be_shown_img():
    '''
    待晒单
    '''
    url = 'https://club.jd.com/myJdcomments/myJdcomment.action?sort=1'
    headers['cookie'] = cookie
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, "html.parser")
    pro_info = soup.find_all('div', class_ = 'pro-info')
    for plist in pro_info:
        oid = plist['oid']
        pid = plist['pid']
        
        img_url = 'https://club.jd.com/discussion/getProductPageImageCommentList.action?productId={}'.format(pid)
        headers['cookie'] = cookie
        img_req = requests.get(img_url, headers=headers)
        text = img_req.text
        print(img_url)

        result = json.loads(text)
        imgurl = result["imgComments"]["imgList"][0]["imageUrl"]
        

        saveUrl = 'https://club.jd.com/myJdcomments/saveShowOrder.action'
        img_data = {
            'orderId': oid,
            'productId': pid,
            'imgs': imgurl,
            'saveStatus': 3
        }
        print(img_data)
        headers['Referer'] = 'https://club.jd.com/myJdcomments/myJdcomment.action?sort=1'
        headers['Origin'] = 'https://club.jd.com'
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        headers['cookie'] = cookie
        save = requests.post(saveUrl, data=img_data, headers=headers)
        print(pid,oid, "评价完成", save)
        time.sleep(5)
        
def review():
    '''
    待追评
    '''
    saveUrl = 'https://club.jd.com/afterComments/saveAfterCommentAndShowOrder.action'
    while True:
        url = 'https://club.jd.com/myJdcomments/myJdcomment.action?sort=3&page=1'
        headers['cookie'] = cookie
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.text, "html.parser")
        operates = soup.find_all('div', class_='operate')
        if len(operates) == 0:
            print("没有记录了")
            break
        for o in operates:
            href = o.a['href']
            infos = href.replace('http://club.jd.com/afterComments/productPublish.action?sku=','').split('&orderId=');
            pid = infos[0]
            oid = infos[1]

            data = {
                'orderId': oid,
                'productId': pid,
                'content': bytes('宝贝和想象中差不多所以好评啦，对比了很多家才选择了这款，还是不错的，很NICE！真的', encoding='gbk'),
                'imgs': '', 
                'anonymousFlag': 1,
                'score': 5
            }
            headers['cookie'] = cookie
            save = requests.post(saveUrl, headers=headers, data=data)
            print(pid,oid, "评价完成", save)
            time.sleep(5)
            
def service_rating():
    '''
    服务评价
    '''
    saveUrl = 'https://club.jd.com/myJdcomments/insertRestSurvey.action?voteid=145&ruleid={}'
    while True:
        url = "https://club.jd.com/myJdcomments/myJdcomment.action?sort=4&page=1"
        headers['cookie'] = cookie
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.text, "html.parser")
        trs = soup.find_all('tr', class_='tr-th');
        if len(trs) == 0:
            print("没有记录了")
            break
            
        for tr in trs:
            oid = tr.find('span', class_='number').a.text
            saveUrl = saveUrl.format(oid)
            data = {
                'oid': oid,
                'gid': 69,
                'sid': 549656,
                'stid': 0,
                'tags': '',
                'ro1827': '1827A1',
                'ro1828': '1828A1',
                'ro1829': '1829A1',
            }
            headers['cookie'] = cookie
            requests.post(saveUrl, headers=headers, data=data)
            print('订单号：' + oid + '服务评价完成')
            time.sleep(5)


handle_map = {
    '待评价订单': be_evaluated,
    '待晒单': be_shown_img,
    '待追评': review,
    '服务评价': service_rating
}

if __name__ == '__main__':
    # be_evaluated_test()
    # exit()
    # 读取一个配置文件 获取 cookie
    appraisal = all_appraisal()
    # {'待评价订单': 6, '待晒单': 1, '待追评': 1, '服务评价': 2}
    for key in appraisal:
        handle = handle_map[key]
        print("准备处理 ", key, "一共", appraisal[key], '单')
        handle()
        print(key, '处理完毕')
        time.sleep(10)
    print("处理完成")
# be_evaluated()
# be_shown_img()
# review()
#service_rating()
#print(all_appraisal())
