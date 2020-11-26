import getopt
import sys
import re
from bs4 import BeautifulSoup
import requests,threading,time,os
class Parent():
    def __init__(self):
        self.url_list=[]
        self.js_list=[]
        #当显示一个结果时将新的与已经展示过的分隔开
        self.new_domain_list = []
        self.domain_list=[]
        self.header={
    'User-Agent':
        'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 73.0.3683.75Safari / 537.36'
}
        self.baiduHeader= {
    'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding':
        'gzip, deflate, br',
    'Accept-Language':
        'zh-CN,zh;q=0.9',
    'Cache-Control':
        'max-age=0',
    'Connection':
        'keep-alive',
    'Cookie':
        'BIDUPSID=1D0FFDE743B97BC908D8C9C6BD560435; PSTM=1588071045; BAIDUID=1D0FFDE743B97BC998C72244E22E71C8:FG=1; BD_UPN=12314753; BDUSS=0ZXR2VBWEMwNVpMaEdSMUJPQlFiNmdYa2FSR0ZMd0xXWWhlY2gzLWM0NW40ZWhlRVFBQUFBJCQAAAAAAAAAAAEAAABf5ldiAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGdUwV5nVMFeY; BD_HOME=1; H_PS_PSSID=31726_1451_31326_21088_31111_31595_31463_31715_30823_22160; delPer=0; BD_CK_SAM=1; PSINO=2; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; COOKIE_SESSION=204_0_7_7_4_9_0_0_7_4_0_0_14622_0_0_0_1590484100_0_1590591580%7C9%23157017_144_1590464947%7C9; BDRCVFR[feWj1Vr5u3D]=mk3SLVN4HKm; H_PS_645EC=a00dlYAGkKoJohyvUrGVc5YUFTBl%2FPSi9gL82hmdiPPTnuF2XY3eY7yHWZ6OD%2FlF06J8',
    'Host':
        'www.baidu.com',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',

    }
        self.option={"url":'Null','cookie':'Null','domain':'baidu.com'}
        self.Http_Response = {}
        self.BaiduSearch='https://www.baidu.com/s?wd=site:baidu.com'+'&rsv_spt=1&rsv_iqid=0xdc92df6d0000e4b1&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=1&rsv_dl=tb&rsv_sug3=6&rsv_sug1=5&rsv_sug7=100&rsv_sug2=0&rsv_btype=i&inputT=913&rsv_sug4=913'
        #防止频繁打印更新
        self.printClock=0
    def frame(self):
        menu = "*********************************************************"
        menu2 = "1.功能介绍：\n" \
                "2.扫描目录结构。\n" \
                "3.扫描js\n" \
                "4.扫描子域名以及注册域名id\n" \
                "5.开放端口\n"
        menu3 = "*********************************************************"
        print(menu)
        print(menu2)
        print(menu3)
        setCommand = {'url': "输入url", 'cookie': "设置cookie", '?': "帮助"}
        while 1:
            command = input(">:")
            cmd = command.split(' ')
            if cmd[0] == 'show':
                if cmd[1] == 'option':
                    for i in self.option:
                        print(i,':',self.option[i])
                    for i in self.header:
                        print(i, ":", self.header[i])
                elif cmd[1] == 'header':
                    for i in self.header:
                        print(i, ":", self.header[i])
                elif cmd[1] == 'result':
                    for i in self.Http_Response:
                        print(i,':',self.Http_Response[i])
                    print('-------------------------------------------------')
                    for i in self.url_list:
                        print(i)
                    print('-------------------------------------------------')
                    print('这里是js')
                    for i in self.js_list:
                        print(i)
                    print('-------------------------------------------------')
                    self.printClock=0
                    print('这里是old domain_list：')
                    for i in self.domain_list:
                        print(i)
                    print('-------------------------------------------------')
                    #如果不为空则显示以下内容
                    if self.new_domain_list:
                        print('以下是update domain_list')
                        print('-------------------------------------------------')
                        for i in self.new_domain_list:
                            print(i)
                            self.domain_list.append(i)

                    else:
                        pass
                    self.new_domain_list=[]
                elif cmd[1]=='domainip':
                    domain = cmd[2]
                    self.DomainIP(domain)
                else:
                    print('[*Error]:未找到命令')
            if cmd[0] == 'set':
                if cmd[1] == 'url':
                    self.option["url"] = cmd[2]
                if cmd[1] == 'cookie':
                    self.option['cookie'] = cmd[2]
                if cmd[1] =='domain':
                    self.option['domain']=cmd[2]
                if cmd[1] == '?':
                    for i in setCommand:
                        print(i, "---", setCommand[i])

            if cmd[0] == 'scan':
                if cmd[1]=='domain':
                    # 2 扫描快的放在前面
                    self.Subdomain_name_search()
                    #1.法1
                    self.Subdomain_name_fuzz()

                print("扫描中.........")
                if cmd[1]=='dir':
                    ans=input("是否深度扫描(yes/no):")
                    if ans=='yes':
                        self.request(self.option["url"])
                        self.Dscan()
                    else:
                        self.request(self.option["url"])
    def request(self,url):
        try:
            html = requests.get(url=url, headers=self.header)
            urlSplit = url.split('/')
            for i in html.headers:
                #print(i,":",html.headers[i])
                self.Http_Response[str(i)]=str(html.headers[i])
            _html = BeautifulSoup(html.text, 'lxml')
            href_all = re.findall(r"href=\"(.+?)\"", str(_html))
            src_all = re.findall(r"src=\".+\.js.+\"", str(_html))
            for i in src_all:
                # 去除src=
                js = i.replace('src=', '')
                # 去除“
                js = js.replace('"', '')
                js = js.replace('type=text/javascript','')
                jsSplit = js.split('/')
                if  jsSplit[0]=='http':
                    self.js_list.append(js)
                else:
                    if url[0:len(url)-1]=='/' or js[0:1]=='/':
                        self.js_list.append(url+js)
                    else:
                        self.js_list.append(url +'/'+ js)
            # 处理检索道德src_all
            # 处理检索到的href
            for i in href_all:
                flag_http = re.match('http', i)
                if len(i) <= 1:
                    continue
                # 这是一个自带全路径的链接
                if flag_http:
                    if i in self.url_list:
                        continue
                    httpUrlSplit = i.split('/')
                    if httpUrlSplit[3]==urlSplit[3]:
                        self.url_list.append(i)
                    else:
                        pass
                else:
                    new_url = url + i
                    flag_spot = i.split('/')
                    Url_split = url.split('/')
                    new_url = ''
                    # 判断上升基层目录
                    spot_num = 0;
                    for i in flag_spot:
                        if i == '..':
                            spot_num += 1
                    for i in range(0, len(Url_split) - (spot_num + 1), 1):
                        new_url = new_url + Url_split[i] + '/'
                    for i in range(spot_num, len(flag_spot), 1):
                        new_url = new_url + flag_spot[i] + '/'
                    new_url = new_url[0:-1]

                    # 如果已经在加载到缓存里则不需要再次加入
                    if new_url in self.url_list:
                        continue
                    else:
                        self.url_list.append(new_url)
        except Exception as a:
            pass
    def Dscan(self):
        try:
            for url in self.url_list:
                thread = threading.Thread(target=self.request, args=(url,))
                thread.start()
            thread.join()
        except:
            pass
    # 爬取存在的目录及js脚本
    def findjs(self):
        pass

    def findImage(self):
        pass

    # 子域名查找
    def Subdomain_name_fuzz(self):

        domeDomain='baidu.com'
        try:
            randstr='Tqzubtuz1op'
            test = randstr+'.'+self.option['domain']
            testHtml=requests.get(test)
            if testHtml.status_code==200:
                print("开启了子域名范析式。结束爆破")
                return
        except:
            pass
        of = open('./dict.txt','r')
        domainDict=[]
        while 1:
            line = of.readline()
            line=line[0:len(line)-1]
            domainDict.append(line)
            if len(domainDict)==500:
                thread = threading.Thread(target=self.Scandomain,args=(domainDict,))
                thread.start()
                domainDict=[]
            if line:
                pass
            else:
                break
        thread = threading.Thread(target=self.Scandomain, args=(domainDict,))
        thread.start()

    def Scandomain(self,dict):

        for i in dict:
            try:
                domain =  i + '.' + self.option['domain']
                url = 'http://'+domain
                status = requests.get(url)
                if status.status_code==200:
                    self.new_domain_list.append(domain)
                    if self.printClock==0:
                        self.printClock=1
                        print("DomainList had update(子域名列表以更新 show result 查看)")
                    else:
                        pass
            except Exception as a:
                pass
    def Subdomain_name_search(self):
        try:
            all_link=[]
            #只分析前十页
            baiduHtml = requests.get(self.BaiduSearch,headers=self.baiduHeader)
            #print(baiduHtml.text)
            _html = BeautifulSoup(baiduHtml.text,'lxml')
            page_div = _html.find_all('div',id='page')
            h3_all = _html.find_all('h3')
            #检测本页面的链接
            for i in h3_all:
                href_all = re.findall(r"href=\"(.+?)\"", str(i))
                #print(href_all[0])
                h3_html = requests.get(href_all[0],headers=self.baiduHeader)
                h3_url = h3_html.url
                #处理得到的url因为其中有一些无用的或者已经检测到的域名
                url_split = h3_url.split('/')
                #观察分割结构第三个为域名
                if url_split[2] in self.domain_list or self.new_domain_list:
                    pass
                else:
                    if self.option['domain'] in url_split[2]:
                        self.new_domain_list.append(url_split[2])
            linkOfpage = page_div[0].find_all('a')
            for i in linkOfpage:
                href_all = re.findall(r"href=\"(.+?)\"", str(i))
                all_link.append(href_all[0])
            for i in all_link:
                url = 'https://www.baidu.com'+i
                url=url.replace('amp;','')
                thread = threading.Thread(target=self.threadScan,args=(url,))
                thread.start()
            thread.join()
            print("[*]  GoogleHack检索完毕")
        except:
            pass
    def threadScan(self,url):
        try:
            html = requests.get(url,headers=self.baiduHeader)
            _html = BeautifulSoup(html.text, 'lxml')
            h3_all = _html.find_all('h3')
            # 检测本页面的链接
            for i in h3_all:
                href_all = re.findall(r"href=\"(.+?)\"", str(i))

                h3_html = requests.get(href_all[0])
                h3_url = h3_html.url
                # 处理得到的url因为其中有一些无用的或者已经检测到的域名
                url_split = h3_url.split('/')
                # 观察分割结构第三个为域名
                if url_split[2] in self.domain_list or self.new_domain_list:
                    pass
                else:
                    if self.option['domain'] in url_split[2]:
                        self.new_domain_list.append(url_split[2])
        except Exception as a:
            print(a)
    #域名ip查询
    def DomainIP(self,domain):
        f = os.popen('nslookup '+domain)
        line = f.readline()
        while line:
            print(line)
            line = f.readline()
'''
1.记得添加一个源码泄露的扫描
2.子域名爆破+siet:
3.以文件的形式保存
4.端口扫描
6.csrf检测
7.目录扫描
由于一直有乱七八糟的事情没有完成，后续会陆续完成的。
'''

if __name__ == '__main__':
    a = Parent()
    a.frame()
    # request(url='http://whois.chinaz.com/gao.com')
    # Dscan()
    # for i in url_list:
    #     print(i)
