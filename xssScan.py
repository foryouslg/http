import requests
import re



def url_is_correct():
    '''
    使用requests.get方法判断url是否正确,并返回url
    :return:
    '''
    try:
        #url = input("Please input the target test url:")
        #url = "http://10.70.18.47:8080/finance/bidding?loanApplicationNo=16540"
        url = "http://10.70.18.47:8080"
        #url = "http://10.70.18.33:8083/shopxx-mobile/"
        requests.get(url)
        print("--->" + url + ' url正确...')
        return url
    except:
        print('please input the correct url!!!')
        #url = input("Please input the target test url:")
    return url_is_correct()

url = url_is_correct()

def url_protocol(url):
    print("--->" + '该站使用的协议是：' + re.findall(r'.*(?=://)',url)[0])
    return re.findall(r'.*(?=://)',url)[0]

urlprotocol = url_protocol(url)

def same_url(url):
    '''
    处理用户输入的url，并为后续判断是否为一个站点的url做准备
    :return: sameurl
    '''
    #url = url.replace((re.findall(r'.*(?=://)',url_is_correct())[0]) + '://','')
    url = url.replace(urlprotocol + '://','')
    '''
    if url.find('http://') == 0:
        url_www = re.findall(r'(?<=http://).*',url)[0]
    '''
    if re.findall(r'^www',url) == []:
        sameurl = 'www.' + url
        if sameurl.find('/') != -1:
            sameurl = re.findall(r'(?<=www.).*?(?=/)', sameurl)[0]
        else:
            sameurl = sameurl + '/'
            sameurl = re.findall(r'(?<=www.).*?(?=/)', sameurl)[0]
    else:
        if url.find('/') != -1:
            sameurl = re.findall(r'(?<=www.).*?(?=/)', url)[0]
        else:
            sameurl = url + '/'
            sameurl = re.findall(r'(?<=www.).*?(?=/)', sameurl)[0]
    print("--->" + '同站域名地址：' + sameurl)
    return sameurl

domain_url = same_url(url)


def load_payload():
    '''
    从payload.txt文件中加载payload
    :return:
    '''
    file = open('payload.txt', 'r')
    payloads = []
    for payload in file.readlines():
        if payload != '\r' and payload != '\n' and payload != '\r\n':
            payloads.append(payload.split('\n')[0])
    return payloads

'''
处理url的类，对已访问过的和未访问过的进行记录，待后续使用
'''
class linkQuence:
    def __init__(self):
        self.visited = []
        self.unvisited = []

    def getVisitedUrl(self):
        return self.visited
    def getUnvisitedUrl(self):
        return self.unvisited
    def addVisitedUrl(self,url):
        return self.visited.append(url)
    def addUnvisitedUrl(self,url):
        if url != '' and url not in self.visited and url not in self.unvisited:
            return self.unvisited.insert(0,url)

    def removeVisited(self,url):
        return self.visited.remove(url)
    def popUnvisitedUrl(self):
        try:
            return self.unvisited.pop()
        except:
            return None
    def unvisitedUrlEmpty(self):
        return len(self.unvisited) == 0

class Spider():
    def __init__(self,url):
        #self.url = url
        self.linkQuence = linkQuence()
        self.linkQuence.addUnvisitedUrl(url)
        #self.page_links = []
        #self.true_url = []
        #self.same_target_url = []
        #self.unrepect_url = []
        self.current_deepth = 1

    def getPageLinks(self,url):
        pageSource = requests.get(url).text
        pageLinks = re.findall(r'(?<=href=\").*?(?=\")|(?<=href=\').*?(?=\')',pageSource)
        '''
        |(?<=action=\").*?(?=\")这是抓取<form>中的连接，即post数据
        '''
        #self.page_links = self.page_links + pageLinks
        #print(self.page_links)
        for l in pageLinks:
            print(url + '该页面的源码链接有：' + l)
        #for l in self.page_links:
        #    print(url + '该页面的源码链接有：' + l)
        #return self.page_links
        return pageLinks

    def processUrl(self,url):
        '''
        判断正确的url及处理相对路径为正确的完整url
        :return:
        '''
        true_url = []
        for l in self.getPageLinks(url):
            if re.findall(r'/',l):
                if re.findall(r':',l):
                    true_url.append(l)
                else:
                    true_url.append(urlprotocol + '://' + domain_url + l)
        #print(trueUrl)
        for l in true_url:
            print(url + '该url页面源码中，有效url：' + l)
        return true_url

    def sameTargetUrl(self,url):
        same_target_url = []
        for l in self.processUrl(url):
            if re.findall(domain_url,l):
                same_target_url.append(l)
        #print(self.same_target_url)
        for l in same_target_url:
            print(url + '该url页面源码中属于同一域的url有：' + l)
        return same_target_url

    def unrepectUrl(self,url):
        unrepect_url = []
        for l in self.sameTargetUrl(url):
            if l not in unrepect_url:
                unrepect_url.append(l)
        for l in unrepect_url:
            print(url + '该url下不重复的url有------：' + l)
        #print(self.unrepect_url)
        return unrepect_url

    def crawler(self,crawl_deepth=1):
        while self.current_deepth <= crawl_deepth:
            while not self.linkQuence.unvisitedUrlEmpty():
                visitedUrl = self.linkQuence.popUnvisitedUrl()
                #print(visitedUrl)
                if visitedUrl is None or visitedUrl == '':
                    continue
                #self.getPageLinks(visitedUrl)
                links = self.unrepectUrl(visitedUrl)
                self.linkQuence.addVisitedUrl(visitedUrl)
                for link in links:
                    self.linkQuence.addUnvisitedUrl(link)
            self.current_deepth += 1
        for l in self.linkQuence.visited:
            print('已访问过的url有----：' + l)
        return self.linkQuence.visited

class JudgeXss():

    def __init__(self,url=None,crawl_deepth=1):
        #self.urls = Spider(url).crawler(crawl_deepth)
        self.url = url
        self.spider = Spider(url)
        self.crawler = self.spider.crawler(crawl_deepth)
        #self.xss_urls = []
        #self.payload_url = []


    def xssUrl(self,url=None):
        '''
        如果url不为空，说明想对此url进行xss检测，如果url为空，那么是对整个url所包含的网站进行xss检测
        :param url: 是一个合法的url地址
        :return: 可能存在xss的url列表xss_urls
        '''
        xss_urls = []
        if self.url == None and url != None:
            if re.findall(r'\?',url):
                xss_urls.append(url)
                for l in xss_urls:
                    print("--->" + '可能存在xss漏洞的url有如下：' + l)
        else:
            for url in self.crawler:
                if re.findall(r'\?',url):
                    xss_urls.append(url)
            #print(self.xss_urls)
            for l in xss_urls:
                print("--->" + '可能存在xss漏洞的url有如下：' + l)
        return xss_urls


    def xssDetect(self,url=None):
        '''
        如果url不为空，说明想对此url进行xss检测，如果url为空，那么是对整个url所包含的网站进行xss检测
        :param url: 是一个合法的url地址
        :return: 可能存在xss的url与payload的捆绑列表payload_url
        '''
        payload_url = []
        if self.url != url:
            for l in self.xssUrl(url):
                '''
                此处是处理每个参数之后添加payload
                '''
                mainUrl = re.findall(r'.*?\?', l)[0]
                arguments = re.findall(r'(?<=\?).*', l)[0]
                args = []
                for payload in load_payload():
                    tmp = []
                    for i in arguments.split('&'):
                        tmp.append(i + payload)
                    args.append(tmp)

                newUrl = []
                for i in args:
                    newUrl.append('&'.join(i))
                for i in newUrl:
                    payload_url.append(mainUrl + i)
                '''
                for payload in load_payload():
                    payload_url.append(l + payload)
                '''
            for l in payload_url:
                print("--->" + '添加xss漏洞payload后的url：' + l)
        else:
            for l in self.xssUrl(url):
                '''
                此处是处理每个参数之后添加payload
                '''
                mainUrl = re.findall(r'.*?\?', l)[0]
                arguments = re.findall(r'(?<=\?).*', l)[0]
                args = []
                for payload in load_payload():
                    tmp = []
                    for i in arguments.split('&'):
                        tmp.append(i + payload)
                    args.append(tmp)

                newUrl = []
                for i in args:
                    newUrl.append('&'.join(i))
                for i in newUrl:
                    payload_url.append(mainUrl + i)
            for l in payload_url:
                print("--->" + '添加xss漏洞payload后的url：' + l)
        return payload_url

    def JudgeIsXss(self,url=None):
        '''
        如果url不为空，说明想对此url进行xss检测，如果url为空，那么是对整个url所包含的网站进行xss检测
        :param url: 是一个合法的url地址
        :return: 存在xss的url列表exist_xss_url
        '''
        exist_xss_url = []
        if self.url != url:
            for i in self.xssDetect(url):
                if re.findall(r'slg',requests.get(i).text):
                    exist_xss_url.append(i)
                    print("--->" + 'discover the %s exist xss!!!' % i)
        else:
            for i in self.xssDetect(url):
                if re.findall(r'slg', requests.get(i).text):
                    exist_xss_url.append(i)
                    print("--->" + 'discover the %s exist xss!!!' % i)
        if exist_xss_url == []:
            print('--------------->未发现xss漏洞！<----------------------')
        return exist_xss_url

'''
对于js链接和post请求的数据进行安全检测思路：
1、可以通过实现代理服务器的方式，使用鼠标将所有链接和第一次提交的post数据获取到
2、然后进行分析js页面和post提交的数据
3、添加payload

'''



if __name__ == '__main__':
    spider = Spider(url)           #开启掉第一步
    #print(spider.crawler(2))
    spider.crawler(20)          #开启爬虫，并设置爬虫深度
    #JudgeXss().JudgeIsXss(url)   #开启xss扫描
    #JudgeXss(url).xssDetect()