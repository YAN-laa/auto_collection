from optparse import OptionParser
active=True

while active:
    def main():
        print("ICMP发现(1),网站信息收集(2),邮箱收集(3)退出(886)")
        usr_request=int(input("请输入:"))
        # parser=OptionParser("Usage")
        # parser.add_option('-i',type='string',dest='IP',help='specify target host')
        # parser.add_option('-u', type='string', dest='IP', help='specify target host')
        # options,args=parser.parse_args()
        # global options
        # print("Search for"+ options.IP+"\n")
        return usr_request
    if __name__ == '__main__':
        usr_request=main()
        if usr_request==886:
           active=False
        if usr_request==1:
            from 主机发现模块 import ICMP主机探测
            try:
                ICMP主机探测.main()
            except KeyboardInterrupt:
                print("interrupted by user")
        if usr_request==2:
            from 被动信息收集 import 网站信息搜集
            try:
                网站信息搜集.main()
            except KeyboardInterrupt:
                print("interrupted by user")
        if usr_request==3:
            from 被动信息收集 import 邮件收集
            try:
                邮件收集.start()
            except KeyboardInterrupt:
                print("interrupted by user")
