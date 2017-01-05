import subprocess
import os

def systemcall(command):
    '''系统命令调用'''
    # p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    # output = p.stdout.readlines()
    popen=subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    # f = os.popen(command)
    # output = f.readlines()
    returncode = popen.poll()
    output = []
    while returncode is None:
        line = popen.stdout.readline()
        returncode = popen.poll()
        line = line.strip()
        output.append(line.decode('utf-8'))
    return output[:-1]

# # test code
# def main():
#     cmd = 'uptime'
#     result = systemcall(cmd)
#     for line in result:
#         print(line)
#
# if __name__ == '__main__':
#     main()


class Partition:
    '''分页显示的类'''
    def __init__(self, pageSize):
        self.pageSize = pageSize
        self.currentPage = 1

    def setData(self, data):
        self.data = data
        self.setTotalpages()
        if self.currentPage > self.totalpages:
            self.currentPage = self.totalpages

    def getCurPage(self):
        '''获取当前页面的数据'''
        return self.getPage(self.currentPage)

    def nextPage(self):
        if self.currentPage is not self.pageSize:
            self.currentPage = self.currentPage + 1
        return self.getCurPage()

    def frontPage(self):
        if self.currentPage is not 1:
            self.currentPage = self.currentPage - 1
        return self.getCurPage()

    def getPage(self, page):
        startLine = (page-1) * self.pageSize
        if page is self.totalpages:
            endLine = len(self.data) - 1
        else:
            endLine = page * self.pageSize - 1
        return self.data[startLine:endLine]

    def setTotalpages(self):
        if len(self.data)%self.pageSize is 0:
            self.totalpages = len(self.data)/self.pageSize
        else:
            self.totalpages = round(len(self.data)/self.pageSize) + 1