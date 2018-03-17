import requests
import re
import pandas as pd
import json

#获得页面函数
def getHTMLText(url):
    try:
        r = requests.get(url,timeout = 30)  
        r.raise_for_status()    #检查是否成功
        r.encoding = r.apparent_encoding  # 文本的分析编码替换整体的编码
        return r.text
    except:
        return ''
       
#对每一个获得的页面进行解析
def parsePage(ilt,html):#(结果的列表类型,相关的网页)
    try:
        #标题   *? 表示最小匹配 
        title = re.findall(r'\"raw_title\"\:\"(.*?)\"',html)
        #价格
        price = re.findall(r'\"view_price\"\:\"([\d\.]*)\"',html) 
        #购买人数 
        buyNumer = re.findall(r'\"view_sales\"\:\"(\d*)人付款\"',html)
        #店铺名称
        shopName = re.findall(r'\"\,\"nick\"\:\"(.*?)\"',html)
        #判断是否为天猫店,并将结果转化为:'是','否'
        isTmall =re.findall(r'\"isTmall\"\:(.*?)\,\"',html)
        isTmall =list(map(lambda x:'是' if x =='true' else '否',isTmall))
        #判断是否包邮
        expressFee =re.findall(r'\"view_fee\"\:\"([\d\.]*)\"',html)      
        expressFee = list(map(lambda x:'包邮' if float(x) == 0 else '不包邮',expressFee))#将结果转化为'包邮','不包邮'
        #地点 
        location = re.findall(r'\"item_loc\"\:\"(.*?)\"',html)
        #详细网页
        dlt = re.findall(r'\"detail_url\"\:(\".*?\")',html)
        for i in range(len(dlt)):
            #网址解析
            detailURL = "https:" + json.loads(dlt[i])
            #加入ilt列表
            ilt.append([title[i],price[i],buyNumer[i],shopName[i],isTmall[i],expressFee[i],location[i],detailURL])
    except:
        print('')

#保存商品信息
def saveGoodList(ilt):
    names = ['商品名称','价格','购买人数','店铺名称','是否为天猫','是否包邮','地点','网址']
    # print(len(ilt))
    pd.DataFrame(columns= names, data = ilt).to_csv('MaleCup.csv',index = False)
        
#主函数
def main():
    goods ='飞机杯'  #关键字
    depth = 10  # 设置页面个数
    start_url = 'https://s.taobao.com/search?q=' + goods  #淘宝页面
    infoList = []  #存放商品信息
    for i in range(depth): 
        try:
            url = start_url + '&s= '+ str(44*i)  #设置翻页url
            html = getHTMLText(url)   #读取页面
            parsePage(infoList,html)  #解析页面
        except:
            continue
    saveGoodList(infoList)
    
main()
