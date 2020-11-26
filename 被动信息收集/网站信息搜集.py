from urllib import request
from optparse import OptionParser
import re

def main():
    # parser = OptionParser("Usage:%prog -i <target host> ")   # 输出帮助信息
    # parser.add_option('-u',type='string',dest='IP',help='specify target host')   # 获取ip地址参数
    # options,args = parser.parse_args()
    url=input("请输入你想要查询的url")
    firsturl = f'http://seo.chinaz.com/{url}'
    html = request.urlopen(firsturl).read().decode('utf-8')
    #备案号
    info={}
    info['title']=re.findall(rf'<span class="mr50">备案号：<i class="color-2f87c1"><a href="//icp.chinaz.com/{url}" target="_blank">(.*?)</a></i></span>',html)
    print('备案号：',info['title'])
    #性质
    info['xibzhi']=re.findall(rf'<span class="mr50">性质：<i class="color-63">(.*?)</i></span>',html)
    print('性质：',info['xibzhi'])
    #名称
    info['minzi']=re.findall(rf'target="_blank" style="color:#4192E7">(.*?)</a>',html)
    print('名称： ',info['minzi'])
    #审核时间
    info['time']=re.findall(rf'<span>审核时间：<i class="color-63">(.*?)</i></span>',html)
    print('审核时间： ',info['time'])
    #IP地址
    info['ip']=re.findall(rf'target="_blank">(.*?)</a></i></span>',html)
    print('IP地址： ',info['ip'][1])
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("interrupted by user, killing all threads...")