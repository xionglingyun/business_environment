# coding=utf-8
import logging
import random
import re
import urllib2

from datetime import datetime, timedelta
from os import path

from bs4 import BeautifulSoup


logging.basicConfig(level=logging.INFO)


_USER_AGENTS = [
  'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3',
  "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1',
  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6',
  'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3',
  'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3',
  'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3',
  'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3',
  'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6',
  'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1',
  'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24',
  "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
  'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24',
  'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11',
  'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
  'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko',
  'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
  "Mozilla/5.0 (Windows 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Safari/536.3",
]


_KEYWORDS = [
  '营商',
  '营商环境',
  '开办企业',
  '申请建筑许可',
  '雇佣员工',
  '登记物权',
  '获取信贷',
  '保护投资人',
  '缴付税负',
  '交税',
  '出入境贸易',
  '跨境贸易',
  '合同强制执行',
  '关闭企业',
  '获得电力供应的便利程度',
  '办理施工许可',
  '法治',
  '法制保障',
  '惩处虚假诉讼',
  '股东权利保护',
  '产权保护',
  '知识产权保护',
  '企业家财产权',
  '公司治理',
  '创业',
  '市场准入',
  '契约自由',
  '金融便利',
  '金融',
  '市场竞争',
  '破产程序',
  '信用',
  '信息化',
  '失信',
  '诚信',
  '自主经营权',
  '监管环境',
]


def get_html(url):
  """Gets raw HTML content of the input URL.

  获取输入URL链接的HTML内容。

  Args:
    url: string

  Returns:
    Raw HTML string content in Unicode format.
  """
  user_agent = random.choice(_USER_AGENTS)
  headers = {'User-Agent': user_agent}
  req = urllib2.Request(url=url, headers=headers)
  max_tries = 10
  html = ''

  for tries in range(max_tries):
    try:
      html = urllib2.urlopen(url=req, timeout=30).read()
      break
    except:
      if tries < max_tries - 1:
        continue

      logging.error(
          'Tried {0} times to access URL {1}'.format(tries, url))
      break

  html_unicode = html.decode('gbk', 'ignore')
  logging.debug(html_unicode.encode('utf-8'))

  return html_unicode


class NewsPage(object):
  def __init__(self, name, url, content_selector):
    self.name = name
    self.url = url
    self.time_id = 'pubtime_baidu'
    self.content_selector = content_selector

  def get_news(self):
    """Returns news page in a tuple of (title, time, content).

    将获取的新闻以以下形式返回（文章标题，发布时间，文章内容）。
    """
    # Get the raw HTML content of the news page in Unicode.
    news = ''
    try:
      news = get_html(self.url)
    except:
      pass

    # Convert the HTML content to BeautifulSoup object.
    soup = BeautifulSoup(news, 'html.parser')

    # Get the news title.
    title = soup.title.string
    logging.debug('News page title is {0}'.format(
        title.encode('utf-8', 'ignore')))

    # Get the news time.
    time = soup.find(id='pubtime_baidu').string
    temp = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    time = temp.strftime('%Y-%m-%d-%H-%M')
    logging.debug('News page time is {0}'.format(
        time.encode('utf-8', 'ignore')))

    # Get the news content.
    # content = soup.find(id='fontzoom').get_text()
    content = soup.select(self.content_selector)[0].get_text()
    content = content.strip()
    logging.debug('News page content is {0}'.format(
        content.encode('utf-8', 'ignore')))

    return (title, time, content)

  def record_news(self):
    """Writes news into a file.

    将获取的新闻以txt文本写入本地文件夹。
    """
    (title, time, content) = self.get_news()
    filename = '{0}_news_{1}.txt'.format(self.name, time)
    with open(filename, 'w+') as f:
      f.write(title.encode('utf-8', 'ignore'))
      f.write('\n')
      f.write(time.encode('utf-8', 'ignore'))
      f.write('\n')
      f.write(content.encode('utf-8', 'ignore'))


class HomePage(object):
  def __init__(self, name, url, keywords=_KEYWORDS, newspage_url_regex=None):
    self.name = name
    self.url = url
    self.keywords = keywords
    self.newspage_url_regex = newspage_url_regex

  def get_html(self):
    """Gets raw HTML content of the input URL.

    获取输入主页面的HTML内容。

    Args:
      url: string

    Returns:
      Raw HTML string content in Unicode format.
    """
    return get_html(self.url)

  def delete_comments(self, html):
    """Returns HTML content without comments.

    删除HTML中的注释。
    """
    r = re.compile(r'<!--[^>]*-->')
    return r.sub('', html)

  def get_urls(self):
    """Returns URLs that match the required keywords.

    获取主页面中和输入关键词相匹配的新闻链接。
    """
    html = self.get_html()
    html = self.delete_comments(html)

    url_regex = self.newspage_url_regex
    if not url_regex:
      url_regex = 'http://finance.jxcn.cn/system/\d+/\d+/\d+/\d+\.shtml'

    keywords_regex = ('|'.join(self.keywords)).decode('utf-8', 'ignore')
    regex_template = u'<a href="{0}"[^<>]*>[^</>]*(?:{1})[^</>]*</a>'.format(
        url_regex, keywords_regex)
    regex = re.compile(regex_template, re.S)
    links = re.findall(regex, html)

    results = [re.search(url_regex, l, re.I) for l in links]
    urls = [r.group(0) for r in results]
    logging.info(urls)

    return urls

  def record_urls(self):
    """Writes URLs into a local txt file and returns the filename.

    将获取的新闻链接以txt文本写入本地文件夹并返回写入的文件名。
    """
    filename = '{0}_urls.txt'.format(self.name)
    urls = self.get_urls()

    # Convert the string list to string and then write into the file.
    lines = '\n'.join(urls)
    # Mode w+ also creates the file if it does not exist.
    with open(filename, 'w+') as f:
      f.write(lines.encode('utf-8', 'ignore'))
      # Add a newline at the end of the file.
      f.write('\n')

    logging.info(
        'Financial URLs has been written into the file {0}'.format(filename))

    return filename


class NewsSpider(object):
  def __init__(self):
    self.sources = {
      # 江西舆情在线
      'yuqing': {
        'homepage_url': 'http://yuqing.jxnews.com.cn/',
        'newspage_url_regex': 'http://yuqing.jxnews.com.cn/system/\d+/\d+/\d+/\d+\.shtml',
        'content_selector': '.sc_contect',
      },
      # 中国江西网廉政频道
      'lianzheng': {
        'homepage_url': 'http://jjjc.jxcn.cn/',
        'newspage_url_regex': 'http://jjjc.jxcn.cn/system/\d+/\d+/\d+/\d+\.shtml',
        'content_selector': '#Zoom',
      },
      # 中国江西网金融频道
      'jinrong': {
        'homepage_url': 'http://finance.jxcn.cn/',
        'newspage_url_regex': 'http://finance.jxcn.cn/system/\d+/\d+/\d+/\d+\.shtml',
        'content_selector': '#fontzoom',
      },
      # 大江网经济频道
      'jingji': {
        'homepage_url': 'http://ce.jxcn.cn/',
        'newspage_url_regex': 'http://ce.jxcn.cn/system/\d+/\d+/\d+/\d+\.shtml',
        'content_selector': '.cBlack',
      },
    }

  def record_all_news(self):
    """Writes all news content into local txt files.

    将获取的所有新闻以txt文本写入本地文件夹。"""
    filenames = []
    for name, value in self.sources.iteritems():
      homepage = HomePage(name=name, url=value['homepage_url'],
                          newspage_url_regex=value['newspage_url_regex'])
      newspage_urls = homepage.get_urls()

      for url in newspage_urls:
        newspage = NewsPage(name, url, value['content_selector'])
        newspage.record_news()


def main():
  news_spider = NewsSpider()
  news_spider.record_all_news()


if __name__ == '__main__':
  main()
