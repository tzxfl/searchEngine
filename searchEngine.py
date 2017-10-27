#!/usr/bin/python
#-*- coding: utf-8 -*-
"""
    SearchEngine
    ~~~~~~
    :author:    jadore <jadore@baimaohui.com.cn>
    :homepage:  https://www.baimaohui.com.cn
    :interpre:  python2
"""
import urllib2, time
import re, random, types
import requests
from optparse import OptionParser
from bs4 import BeautifulSoup

class SearchEngine:
    def __init__(self):
        self.google_url = 'https://www.google.ca'
        self.baidu_url = 'http://www.baidu.com'
        self.base_url = ""
        self.user_agents = list()
        self.load_user_agents()

    def randomSleep(self):
        time.sleep(random.randint(60, 120))

    def extractUrl(self, href):
        url = ''
        #pattern = re.compile(r'http[s]?://([^/]+)/', re.U | re.M) #domain pattern example: www.baidu.com
        pattern = re.compile(r'(http[s]?://[^/]+)/', re.U | re.M) #simple url example: http://www.baidu.com
        #pattern = re.compile(r'(http[s]?://[^\s]+)', re.U | re.M)  #entire url example: http://www.baidu.com/www/wer?ww=aa
        url_match = pattern.search(href)
        if(url_match and url_match.lastindex > 0):
            url = url_match.group(1)
        return url

    def load_user_agents(self):
        fp = open('./user_agents', 'r')
        lines  = fp.readlines()
        for line in lines:
            self.user_agents.append(line.strip('\n'))
        fp.close()

    def getHeaders(self):
        user_agents = self.user_agents
        length = len(user_agents)
        user_agent = user_agents[random.randint(0, length - 1)]
        headers = {
            'User-agent': user_agent,
            'connection': 'keep-alive',
            'Accept-Encoding': 'gzip',
            'referer': self.base_url
        }
        return headers

    def search(self, engine, keyword, pages):
        search_urls = []
        keyword = urllib2.quote(keyword)
        total = pages * 10
        for start in range(0, total, 10):
            if engine == "google":
                self.base_url = self.google_url
                url = '%s/search?hl=en&q=%s&start=%s'% (self.google_url, start, keyword)
            elif engine == "baidu":
                self.base_url = self.baidu_url
                url = '%s/s?wd=%s&pn=%s' % (self.baidu_url, keyword, start)
            else:
                exit("请输入正确的搜索引擎类型：baidu、google")
            retry = 3
            while (retry > 0):
                try:
                    headers = self.getHeaders()
                    response = requests.get(url=url, headers=headers)
                    html = response.content
                    #print html
                    results = self.extractSearchResults(engine, html)
                    search_urls.extend(results)
                    break
                except urllib2.URLError, e:
                    print 'url error:', e
                    self.randomSleep()
                    retry = retry - 1
                    continue

                except Exception, e:
                    print 'error:', e
                    retry = retry - 1
                    self.randomSleep()
                    continue
        return search_urls

    def extractSearchResults(self, engine, html):
        results = []
        soup = BeautifulSoup(html, 'html.parser')
        if engine == "google":
            divs = soup.findAll('div', {'class': 'g'})
            if(len(divs) > 0):
                for div in divs:
                    h3 = div.find('h3', {'class': 'r'})
                    if(type(h3) == types.NoneType):
                        continue

                    a = h3.find('a')
                    if (type(a) == types.NoneType):
                        continue

                    href = a['href']
                    url = self.extractUrl(href)
                    if(cmp(url, '') == 0):
                        continue
                    else:
                        if url not in results:
                            results.append(url)
            return results
        if engine == "baidu":
            divs = soup.findAll('div', {'class': 'f13'})
            if (len(divs) > 0):
                for div in divs:
                    a = div.find('a', {'class': 'c-showurl'})
                    if (type(a) == types.NoneType):
                        continue

                    href = a['href']
                    # 使用百度搜索关键字的响应页面，对网站真实URL做了加密处理，通过http://www.baidu.com/link?url=xxx进一步获取真实url
                    # http://www.baidu.com/link?url=0h-hSz3rAB3A8N-DJeLwGDGhrgt51b6Gjv0OnT0ZB7Xc3-jUjgcoi5U5YHP5r3v6
                    if 'www.baidu.com/link?url=' in href:
                        headers = self.getHeaders()
                        response = requests.get(href, headers=headers)
                        #print link.content
                        # 对跳转地址进行一次访问，返回访问的url就能得到我们需要抓取的url结果了
                        if response.status_code == 200:
                            url = self.extractUrl(response.url)
                        # 由于请求http://www.baidu.com/link?url=xxx的时候，可能导致502响应，二该响应数据包如下所示
                        # <strong>http://www.example.com</strong><strong>502,xxxxx</strong>
                        # 因而需要对502响应做单独处理
                        if response.status_code == 502:
                            soup = BeautifulSoup(response.content, 'html.parser')
                            strongs = soup.findAll('strong')
                            for strong in strongs:
                                url = self.extractUrl(strong.string)
                                if url:
                                    break
                        if url:
                            if url not in results:
                                results.append(url)
                        else:
                            continue

                return results

if __name__ == '__main__':
    searchEngine = SearchEngine()

    parser = OptionParser()
    parser.add_option("-e", "--engine",
                      dest = "engine",
                      help="search engine:  baidu, google",
                      default='baidu')
    parser.add_option("-k", "--keyword",
                      dest = "keyword",
                      default=True,
                      help="keyword")
    parser.add_option("-p", "--pages",
                      dest = "pages",
                      default=0,
                      type = int,
                      help="page num")
    (options, args) = parser.parse_args()

    res = searchEngine.search(options.engine, options.keyword, options.pages)
    for r in res:
        print r
    print len(res)