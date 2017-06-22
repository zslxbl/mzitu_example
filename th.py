import os
import time
import threading
import multiprocessing
from mongoqueue import MogoQueue
from download import request
from bs4 import BeautifulSoup

SLEEP_TIME = 1

def mzitu_crawler(max_threads=10):
    crawl_queue = MogoQueue('meinvxiezhenji', 'crawl_queue')
    def pageurl_crawler():
        while True:
            try:
                url = crawl_queue.pop()
                print(url)
            except KeyError:
                print(u'队列没有数据了')
                break
            else:
                img_urls = []
                req = request.get(url, 3).text
                title = crawl_queue.pop_title(url)
                mkdir(title)
                os.chdir('D:\mzitu\\' + title)
                max_span = BeautifulSoup(req, 'lxml').find('div', class_='pagenavi').find_all('span')[-2].get_text()
                for page in range(1, int(max_span) +1):
                    page_url = url + '/' + str(page)
                    img_url = BeautifulSoup(request.get(page_url, 3).text, 'lxml').find('div', class_='main_image').find('img')['src']
                    img_urls.append(img_url)
                    save(img_url)
                crawl_queue.complate(url)

    def save(img_url):
        name = img_url[-9:-4]
        img = request.get(img_url, 3)
        f = open(name, '.jpg', 'ab')
        f.write(img.content)
        f.close()

    def mkdir(path):
        path = path.strip()
        isExist = os.path.exists(os.path.join('D:\meiziut', path))
        if not isExist:
            os.makedirs(os.path.join('D:\meiziut', path))
            return True
        else:
            return False

    threads = []
    while threads or crawl_queue:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)
        while len(threads) < max_threads or crawl_queue.peek():
            thread = threading.Thread(target=pageurl_crawler)
            thread.setDaemon(True)
            thread.start()
            threads.append(thread)
        time.sleep(SLEEP_TIME)

def process_crawler():
    process = []
    num_cpus = multiprocessing.cpu_count()
    for i in range(num_cpus):
        p = multiprocessing.Process(target=mzitu_crawler)
        p.start()
        process.append(p)
    for p in process:
        p.join()

if __name__ == '__main__':
    process_crawler()
