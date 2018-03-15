
# coding: utf-8

# In[1]:

'''
王者荣耀官网英雄皮肤采集
抓取网页为:[王者荣耀英雄](http://pvp.qq.com/web201605/herolist.shtml)
观察原网页,刷新, 取到herolist.json, 另存到当前目录
'''
#导入相关包
import requests
import json
import os

#打开下载的json文件
with open('herolist.json','r',encoding='utf-8') as myFile:#read 
    jsonFile = json.load(myFile)

#在当前目录下新建文件夹-HeroSkins ,并将其设置为工作目录
path = os.getcwd()
os.mkdir('HeroSkins')#在当前目录下生成新文件夹 heroskins
os.chdir(path + '\\HeroSkins') #进入生成的文件夹内
path = os.getcwd()  

for m in range(len(jsonFile)):
    ename = jsonFile[m]['ename'] #取出英雄的英文名称
    cname = jsonFile[m]['cname'] #取出英雄的中文名称
    hero_type = jsonFile[m]['hero_type'] #取出英雄类型
    skin_name = jsonFile[m]['skin_name'].split('|') #取出英雄皮肤名称,并得到用"\"分隔的单个皮肤名称
    skin_number = len(skin_name) #皮肤数量
    os.mkdir(cname)#在当前目录下生成新文件夹,文件夹名字是英雄名字
    os.chdir(path + '\\'+cname) #改变工作目录为当前英雄目录
    for bigskin in range(1,skin_number+1):
        #使用正则表示皮肤网址
        skin_url = 'http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/'+str(ename)+'/'+str(ename)+'-bigskin-'+ str(bigskin) +'.jpg'
        #获取图片二进制信息
        skins = requests.get(skin_url).content
        #写入文件
        with open(cname + '-'+skin_name[bigskin-1]+'.jpg','wb') as mySkin:
            mySkin.write(skins)
    os.chdir(path) #返回至上级目录

