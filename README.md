# searchEngine
通过搜索关键字批量抓取百度、google搜索引擎的url链接的python实现
在批量抓马的过程中，需要通过搜索关键字比如.action、powered by xxx等，然后获取搜索内容的的连接地址，因而写了下面的脚本以供日后使用
```
✗ >python searchEngine.py  -h
Usage: searchEngine.py [options]

Options:
  -h, --help            show this help message and exit
  -e ENGINE, --engine=ENGINE
                        search engine:  baidu, google
  -k KEYWORD, --keyword=KEYWORD
                        keyword
  -p PAGES, --pages=PAGES
                        page num
```

```
✗ >python searchEngine.py -e "baidu" -k "powered by wordpress" -p 1
https://wordpress.org
https://zhidao.baidu.com
https://www.mywpku.com
http://www.wopus.org
https://ja.wordpress.org
http://www.rehbock.com
6
```
详情见个人博客
博客地址：http://weixinglian.com/index.php/archives/38/