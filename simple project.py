'''
    简单爬虫项目

    前期准备：
    目的：爬某个直播网站一个游戏下面，各个主播的人气排行
    找到对应网页
    找到数据所在标签

    步骤：
    模拟HTTP请求，向服务器发送请求，获取服务器返回的HTML
    用正则表达式提取我们要的信息
'''

import re, time
from urllib import request

class Spider():
    url = 'https://www.huya.com/g/lol'   # 可以把目标网站放到类变量里面
    root_pattern = '<span class="txt">([\s\S]*?</span>[\s\S]*?</span>[\s\S]*?)</span>'       # 正则表达式，有了？ 后就不会继续找下一个</span>, 因为正则表达式默认贪婪，会继续找,     这个是特殊例子加不加()都一样
    name_pattern = '<i class="nick" title="([\s\S]*?)"'
    number_pattern = '<i class="js-num">([\s\S]*?)</i>'


    def __find_content(self):   #设置私有方法
        r = request.urlopen(Spider.url)    # 调用类变量 需要加上类名字
        htmls = r.read()
        htmls = str(htmls, encoding='utf-8')   # 相当于把上面的html中的数据解码出来
        return htmls

    def __analysis(self, htmls):      # 上面是打开网站，这里就是分析数据了，抓取目标数据
        root_htmls = re.findall(Spider.root_pattern, htmls)
        anchors = []
        for i in root_htmls:
            name = re.findall(Spider.name_pattern, i)
            number = re.findall(Spider.number_pattern, i)
            anchor = {'name':name, 'number':number}
            anchors.append(anchor)
        return anchors

    def __refine(self, anchors):                               # 调整格式，美观
        l = lambda anchor: {'name': anchor['name'][0].strip(), 'number': anchor['number'][0]}         # 去除多余字符，取出单一数据，再把单一数据做成字典
        return list(map(l, anchors))


    def __sortdata(self, anchors):
        anchors = sorted(anchors, key=self.__sort_seed, reverse=True)
        return anchors

    def __sort_seed(self, anchor):
        data = re.findall('[1-9]\d*\.?\d*', anchor['number'])
        data = float(data[0])                          # 不管后面有没有万，先转第一个。下面再用for 循环转万的计算
        if '万' in anchor['number']:
            data = data * 10000
        return data

    def __show(self, anchors):
        for rank in range(0,len(anchors)):
            print('rank  ' + str(rank +1) + ' :  ' + anchors[rank]['name'] + '----------' + anchors[rank]['number'])

    def go(self):                     # 由于是私有方法，所以要写一个入口方法，以便调试和运行
        t1 = time.time()
        htmls = self.__find_content()
        anchors = self.__analysis(htmls)
        anchors = self.__refine(anchors)
        anchors = self.__sortdata(anchors)
        self.__show(anchors)
        t2 = time.time()
        print('爬虫程序运行需要：' + str(t2-t1) + '秒')


spider = Spider()
spider.go()
