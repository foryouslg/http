import re


class HttpHead():
    '''
    handle the HTTP request
    '''
    def __init__(self,request):
        self.request = request
        if isinstance(request,bytes):
            self.request = request.decode()
        self.request = request


    def getFirst(self):
        '''
        get first line
        :return: first line
        '''
        return self.request.split('\r\n')[0]

    def getMethodAndFullpath(self):
        '''
        get method,fullpath,protocol
        :return: method,fullpath,pro
        '''
        firstline = self.getFirst()
        return firstline.split()

    def getSendData(self):
        '''
        get thd data sent to the server
        the data is 'str' type,when using,need to transform
        :return:'str' types of data
        '''
        firstline = self.getFirst()
        method,fullpath,pro = self.getMethodAndFullpath()
        if fullpath.find(':') != -1:
            mainurl = re.findall(r'(?<=://).*?(?=/)',fullpath)[0]
            self.relativepath = fullpath[len(re.findall(r'.*?://', fullpath)[0]) + len(mainurl):]
            return self.request.replace(firstline, (method + ' ' + self.relativepath + ' ' + pro))
        else:
            return self.request

    def getSerAdd(self):
        host = re.findall(r'(?<=Host: ).*?(?=\r\n)',self.getSendData())[0]
        if host.find(':') == -1:
            serAdd = host
            port = '80'
            return serAdd,port
        else:
            serAdd,port = host.split(':')
            return serAdd,port

    def getUserData(self):
        userData = self.getSendData().split('\r\n\r\n')[1]
        return userData

if __name__ == '__main__':
    request = 'GET http://10.70.18.47:8080/finance/bidding?loanApplicationNo=16596 ' \
              'HTTP/1.1\r\nHost: 10.70.18.47\r\nAccept: text/html,application/xhtml+xml,' \
              'application/xml;q=0.9,image/webp,*/*;q=0.8\r\n\r\nCookie: JSESSIONID=2AD300AB4CFC61DA4BBBC0E893B0AC40; ' \
              'CNZZDATA1257010978=101257115-1474361058-%7C1474361058'
    print(HttpHead(request).getFirst(),
          HttpHead(request).getMethodAndFullpath(),
          HttpHead(request).getSendData(),
          HttpHead(request).getSerAdd(),
          HttpHead(request).getUserData()
          )