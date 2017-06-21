#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/14 23:55
# @Author  : zhangshilong
# @Software: PyCharm Community Edition

from bs4 import BeautifulSoup
import os
import time
from download import request


class mzitu():
    def mkdir(self, path):
        path = path.strip()
        is_exist = os.path.exists(os.path.join("E:\mzitu", path))
        if not is_exist:
            print u'新建文件夹名称为：{}'.format(path)
            os.makedirs(os.path.join("E:\mzitu", path))
            os.chdir(os.path.join("E:\mzitu", path))
            return True
        else:
            print u'名称为{}的文件夹已经存在！'.format(path)
            return False

    def all_url(self, all_url):
        start_html = self.request_mzitu(all_url, 3)
        # print (start_html.text)
        Soup = BeautifulSoup(start_html.text, 'lxml')
        a_list = Soup.find('div', class_='all').find_all('a')

        for a in a_list:
            # print a
            title = a.get_text()
            print u'开始保存{}...'.format(title)
            path = title.replace('?', '_')
            self.mkdir(path)
            href = a['href']
            self.html(href)

    def html(self, href):
        html = self.request_mzitu(href, 3)
        html_Soup = BeautifulSoup(html.text, 'lxml')
        max_span = html_Soup.find('div', class_='pagenavi').find_all('span')[-2].get_text()

        for page in range(1, int(max_span) + 1):
            page_url = href + '/' + str(page)
            time.sleep(0.6)
            self.image(page_url)

    def image(self, page_url):
        image_html = self.request_mzitu(page_url, 3)
        image_Soup = BeautifulSoup(image_html.text, 'lxml')
        image_url = image_Soup.find('div', class_='main-image').find('img')['src']
        self.save(image_url)

    def save(self, image_url):
        name = image_url[-9:-4]
        img = self.request_mzitu(image_url, 3)
        f = open(name + '.jpg', 'ab')
        f.write(img.content)
        f.close()

    def request_mzitu(self, url, timeout):
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
        content = request.get(url, timeout=timeout)
        return content


Mzitu = mzitu()
Mzitu.all_url('http://www.mzitu.com/all')
