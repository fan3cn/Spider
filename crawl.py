import  requests
from bs4 import BeautifulSoup

class Crawl():

    def __init__(self, url):
        self.url = url

    def request(self):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        r = requests.get(self.url, headers=headers)
        #print(r.text.split("}."))
        class_dict = {}
        for item in r.text.split(";}"):
            if item.startswith("."):
                splits = item.split("{background:")
                key = splits[0][1:]
                value = (splits[1].split()[0][1:][:-2], splits[1].split()[1][1:][:-2])
                print(key, value)
            else:
                print(item)
        self.save_to_file(r)

    def save_to_file(self, r):
        filename = self.url.split("/")[-1] + '.html'
        with open(filename, 'wb') as f:
            f.write(r.content)

    def bs(self):
        filename = self.url.split("/")[-1] + '.html'
        doc_html = open(filename, 'rb').read()

        soup = BeautifulSoup(doc_html, "lxml")

        # find css
        css_list = soup.find_all(attrs={"type": "text/css"})
        for css in css_list:
            if 'svgtextcss' in css.get('href'):
                self.url = 'http:'+css.get('href')
                self.request()
                #print(css.get('href'))

        # # find all comments
        # comments = soup.find_all(attrs={"class": "info J-info-all clearfix Hide", "class": "desc J-desc"})
        # #tag = soup.div
        # for div in comments:
        #     # for sub in div.contents:
        #     #     print(sub)
        #     print(div.contents)
        #     #print(''.join(list(div.contents)))
        # #print(soup.prettify())


if __name__ == "__main__":
    #url = 'http://quotes.toscrape.com/tag/humor/'
    url = 'http://www.dianping.com/shop/17182037'
    #url = 'http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/4fb494446f78aaedb88026ae33420b94.css'
    Crawl(url).bs()
    # r = requests.get(url)
    # print(r.content)