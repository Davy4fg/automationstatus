# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time
import os
import urllib2,json
from lxml import etree


with open('player.json', 'r') as f1:
    data1 = json.load(f1)
# with open ('encounter.json', 'r') as f2:
#     data2 = json.load(f2)

class HiInterface:
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)
    def GET(self):
        print('GGGET')
        return self.render.hi()
        return '<BODY><BR>HiInterfaceFirst line~!@#$%^&*()_`-=+{}[];:<>?,./<BR>2nd Line<BR></BODY> '
        

class WeixinInterface:

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        print('GGGET')
        return self.render.hi()
        return '<BODY><BR>WeiXinInterfaceFirst line~!@#$%^&*()_`-=+{}[];:<>?,./<BR>2nd Line<BR></BODY> '
        #获取输入参数
        data = web.input()
        signature=data.signature
        timestamp=data.timestamp
        nonce=data.nonce
        echostr=data.echostr
        #自己的token
        token="DavysToken" #这里改写你在微信公众平台里输入的token
        #字典序排序
        l=[token,timestamp,nonce]
        l.sort()
        sha1=hashlib.sha1()
        map(sha1.update,l)
        hashcode=sha1.hexdigest()
        #sha1加密算法        

        #如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            return echostr

        
    def POST(self):
        print('PPPOST')
        str_xml = web.data() #获得post来的数据
        xml = etree.fromstring(str_xml)#进行XML解析
        #content=xml.find("Content").text#获得用户所输入的内容
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
        #return self.render.reply_text(fromUser,toUser,int(time.time()), u"现在的功能可以重复你的消息 ："+content)
        if msgType == 'event':
            #mscontent == xml.find("Event").text
            if xml.find("Event").text == 'subscribe':#关注的时候的欢迎语
                return self.render.reply_text(fromUser, toUser, int(time.time()), 'This is platform for automation status share.\n Please send \"h\" to get help infomation\nAny problem or suggestion, just feel free to leave a message')
        if msgType == 'text':
            content = xml.find("Content").text
            if content == 'help':
                reply = u'我们收录了参加奥运会的所有国家的球员信息\n你可以输入“国家”来获取我们收录的国家集合\n你可以输入这些国家的中文名来获取球队成员姓名（如 中国）\n输入任何女排球员的中文名来获取她的信息（如 魏秋月）\n\n输入about来看看主页君是谁\n\n不要输错字喔❤️建议先输国家名称获取球员名字再搜索球员信息'
                return self.render.reply_text(fromUser, toUser, int(time.time()), reply)
            if content == 'a':
                return self.render.reply_text(fromUser, toUser, int(time.time()), "--> http://1.automationstatus.applinzi.com/weixin")
            if content == 'b':
            	return self.render.reply_text(fromUser, toUser, int(time.time()), u'''1美国🇺🇸\n2中国🇨🇳\n''')
            #elif content == 'm':
            #    return self.render.reply_news(fromUser, toUser, int(time.time()), 'a', 'b', 'https://az616578.vo.msecnd.net/files/responsive/cover/main/desktop/2016/03/18/635939394083003642-770889348_love%20pic.jpg', 'www.baidu.com')
            for iter in data1:
            	if content == iter["ch_name"]:
                	return self.render.reply_text(fromUser, toUser, int (time.time()), "英文名: {0}\n号码: {1}\n位置: {2}\n国籍: {3}\n生日: {4}\n身高: {5}\n体重: {6}\n俱乐部: {7}\n扣球高度: {8}\n拦网高度: {9}".format(iter["name"],iter["number"],iter["position"].encode("utf8"),iter["nationality"].encode("utf8"),iter["birth_date"][0:10],iter["height"],iter["weight"],iter["club"],iter["spike"],iter["block"]))
            list = ['以下是检索到的信息：']
            is_country = False
            for iter in data1:
                if content == iter["nationality"]:
                    is_country = True
                    list.append("中文名: {0} 号码: {1}".format(iter["ch_name"].encode("utf8"), iter["number"]))
                    #list.append( iter["ch_name"].encode("utf8") ) 
            #return self.render.reply_text(fromUser, toUser, int(time.time()), "\n".join(list))
            if is_country:
            	return self.render.reply_text(fromUser, toUser, int(time.time()), "\n".join(list))
            else:
                #return self.render.reply_text(fromUser, toUser, int(time.time()), "\n".join(list))
                return self.render.reply_text(fromUser, toUser, int(time.time()), r'<BODY><BR>Such &lt;&gt; command is not supported.\n{Please} [send] !@#$%^&*()<>,.:;?// "h" to \"get help\' infomation\nAny problem or suggestion, just feel free to leave a message2<\BODY>')
        else:
            return self.render.reply_text(fromUser, toUser, int(time.time()), r'Such msgType is not supported.\n')
