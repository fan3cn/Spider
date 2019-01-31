import time
from page_parser import PageParser
import random
import requests

class Crawl():

    def __init__(self, url):
        self.urls = []
        self.addUrl(url)

    def addUrl(self, url):
        self.urls.append(url)

    def run(self):

        while(True):

            #print(self.urls)

            if not self.urls:
                self.sleep()
                continue

            url = self.urls.pop(0)
            print(url)

            #self.crawl(url)

            review_url = url + '/review_all'
            self.crawl(review_url)

            #pp.parse_svg_file()
            self.sleep()

    def crawl(self, url):
        pp = PageParser(url)
        pp.download_css_files()

        pp.extract_shop_info()
        pp.extract_comments()

        # if 'review_all' in url:
        #     pp.extract_comments()
        # else:
        #     pp.extract_shop_info()

    def sleep(self):
        print("Running...")
        time.sleep(random.randint(3,10))




if __name__ == "__main__":
    #url = 'http://quotes.toscrape.com/tag/humor/review_all'
    #url = 'http://www.dianping.com/shop/4674001'
    url = 'http://www.dianping.com/shop/72145036'
    #url = 'https://www.dianping.com/dpnav/userCardData'
    #url = 'http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/4fb494446f78aaedb88026ae33420b94.css'
    crawl = Crawl(url)
    crawl.addUrl('http://www.dianping.com/shop/23975904')
    crawl.addUrl('http://www.dianping.com/shop/124054656')
    crawl.addUrl('http://www.dianping.com/shop/23885092')
    crawl.addUrl('http://www.dianping.com/shop/4178369')
    crawl.addUrl('http://www.dianping.com/shop/24812466')
    crawl.addUrl('http://www.dianping.com/shop/4674001')
    crawl.run()
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    # r = requests.get(url, headers=headers)
    #
    # print(r.content)
    # print(r.cookies)
