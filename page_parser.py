from bs4 import BeautifulSoup
import request
import re
import xml.etree.ElementTree as ET
import os
import cache
import utils


class PageParser():

    def __init__(self, url=None):
        self.url = url
        if url:
            self.file_path = './html/'+self.download_html_page()
            self.file_name = utils.get_file_name(url)[:-5]

    def download_html_page(self):
        request.request(self.url)
        return utils.get_file_name(self.url)

    def download_css_files(self):
        text = open(self.file_path, 'rb+').read().decode('utf-8')
        soup = BeautifulSoup(text, "lxml")

        # find css files
        css_list = soup.find_all(attrs={"type": "text/css"})
        for css in css_list:
            if 'svgtextcss' in css.get('href'):
                url = 'http:'+css.get('href')
                request.request(url, './css/', 'css')
                self.parse_css_file('./css/' + utils.get_file_name(url))
        print("Css files have been downloaded and parsed.")

    def parse_css_file(self, file_path):
        print("Parsing %s ..."%file_path)
        text = open(file_path, 'rb+').read().decode('utf-8')
        #print(text)
        class_svg = ""
        #instance_pos = {}
        classes = []
        for item in text.split(";}"):
            if item.startswith("."):
                splits = item.split("{background:")

                key = splits[0][1:]
                value = (splits[1].split()[0][1:][:-2], splits[1].split()[1][1:][:-2])

                #print(key, value)

                cache.instance_pos[key] = value

                #instance_pos = instance_pos + "%s %s %s" % (key, value[0], value[1]) + "\n"

                #print(key, value)
            elif 'class' in item:
                # c[class^="egm"]{width: 12px;height: 31px;margin-top: -11px;background-image: url(//s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/347989744d0b930fdc60e773cc80acea.svg);background-repeat: no-repeat;display: inline-block;vertical-align: middle
                class_ = re.findall('class\^="\w*"', item)[0][8:][:-1]
                #print(class_)
                # http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/347989744d0b930fdc60e773cc80acea.svg
                url = 'http:'+re.findall('url\(.*\);', item)[0][4:][:-2]
                #print(svg_url)
                # Save to file
                request.request(url, './svg/', '.svg')
                self.parse_svg_file('./svg/' + utils.get_file_name(url), class_)

                file_name = utils.get_file_name(url)
                #print("%s %s"%(class_, file_name))
                class_svg = class_svg + "%s %s"%(class_, file_name) + "\n"

                classes.append(class_)

        #print(class_svg)
        #request.save_to_file('./idx/', 'class_pos.txt', class_svg)
        #request.save_to_file_append('./idx/', 'class_svg.txt', class_svg)

        for c in classes:

            if c in cache.class_pos.keys():
                continue

            if os.path.exists('./idx/pos/'+c+'.txt'):
                # Load in
                text = open('./idx/pos/'+c+'.txt', 'r').read()
                cache.class_pos[c] = text.split('\n')
                continue
            # Find the coordinates
            x = []
            y = []
            for k,v in cache.instance_pos.items():
                if k.startswith(c):
                    x.append(int(float(v[0])))
                    y.append(int(float(v[1])))
            x = sorted(list(set(x)))
            y = sorted(list(set(y)))

            xy = ' '.join([str(i) for i in x ]) + '\n' + ' '.join([str(i) for i in y ])
            utils.save_to_file('./idx/pos/', c + '.txt', xy)
            cache.class_pos[c] = xy.split('\n')


    def parse_svg_file(self, file_path, class_):
        print("Parsing %s ..." % file_path)

        if class_ in cache.class_text.keys():
            return

        if os.path.exists('./idx/svg_text/' + class_ + '.txt'):
            # Load in
            text = open('./idx/svg_text/' + class_ + '.txt', 'r').read()
            cache.class_text[class_] = text.split('\n')
            return

        root = ET.parse(file_path).getroot()
        # root.tag = {http://www.w3.org/2000/svg}svg
        namespace = re.findall('\{.*}', root.tag)[0]
        # print(namespace)

        # # get ids
        # pos_y = []
        # for item in root.findall('.//%spath' % namespace):
        #     #print(item.get('d').split()[1])
        #     # M0 31 H600
        #     pos_y.append(item.get('d').split()[1])
        #
        # if not pos_y:
        #     for item in root.findall('.//%stext' % namespace):
        #         pos_y.append(item.get('y'))

        # get content
        contents = ""
        for item in root.findall('.//%stextPath' % namespace):
            #print(item.text)
            contents = contents + item.text + "\n"


        if not contents:
            for item in root.findall('.//%stext' % namespace):
                # print(item.text)
                contents = contents + item.text + "\n"

        # assert (len(pos_y) == len(contents))

        # for pos, content in zip(pos_y, contents):
        #     print(pos, content)

        utils.save_to_file('./idx/svg_text/', class_ + '.txt', contents)
        cache.class_text[class_] = contents.split('\n')


    def extract_shop_info(self):
        print("Extracting shop basic info...")
        text = open(self.file_path, 'rb+').read().decode("utf-8")
        #print(text.decode("utf-8"))
        # Shop info, location, category
        soup = BeautifulSoup(text, "lxml")
        list_crumb = soup.find_all(attrs={"class": "list-crumb"})
        for crumb in list_crumb:
            a_list = crumb.find_all('a')
            for item in a_list:
                print(item.contents[0])
        #shop_name = soup.find(attrs={"class": "shop-name"}).contents[0]
        # Price
        rank_info = soup.find(attrs={"class": "rank-info"})
        price = rank_info.find(attrs={"class": "price"}).contents[0]
        print(price)
        # Scores
        scores = rank_info.find(attrs={"class": "score"})
        for item in scores.find_all(attrs={"class": "item"}):
            print(item.contents[0])
        # Address
        add_info = soup.find(attrs={"class": "address-info"}).contents
        address = ""
        for sub in add_info:
            sub = str(sub).strip()
            if sub.startswith('<'):
                #print(sub)
                sub = self.get_character_by_pos(sub)
            address = address + sub
            #print(sub)
        print(address)

        # Phone
        phone_info = soup.find(attrs={"class": "phone-info"}).contents
        phone = ""
        for sub in phone_info:
            if re.findall('^\s$', str(sub)):
                phone = phone + " "
                continue
            sub = str(sub).strip()
            if sub.startswith('<'):
                sub = self.get_character_by_pos(sub)
            phone = phone + sub
        print(phone)

    def extract_comments(self):
        print("Extracting shop comments...")
        # print(cache.class_pos)
        # print(cache.class_text)
        # print("x")
        text = open(self.file_path, 'rb+').read().decode('utf-8')
        soup = BeautifulSoup(text, "lxml")

        # find reviews
        comments = soup.find_all(attrs={"class": "review-words Hide"})
        for item in comments:
            comment = ""
            for seg in item.contents:
                if seg.string:
                    comment = comment + seg.string.strip()
                elif seg.name == 'span':
                    #<span class="mrsc35"></span>
                    #instance = re.findall('\"\w*\"', str(seg))[0][1:-1]
                    character = self.get_character_by_pos(str(seg))
                    comment = comment + character
                elif seg.name == 'br':
                    comment = comment + '</br>'
            print(comment)

    # #<span class="mrsc35"></span>
    def get_character_by_pos(self, span):
        instance = re.findall('\"\w*\"', span)[0][1:-1]
        #print(instance)
        #print(cache.class_pos)
        class_ = ""
        for key in cache.class_pos.keys():
            if instance.startswith(key):
                class_ = key
        if class_ == "":
            print("Error!!! No such instance %s in cache."%instance)
            return

        x,y = cache.instance_pos[instance]

        y_idx = cache.class_pos[class_][0].split().index(str(int(float(x))))
        x_idx = cache.class_pos[class_][1].split().index(str(int(float(y))))

        return cache.class_text[class_][x_idx][y_idx]


if __name__ == "__main__":
    #pp = PageParser('http://www.dianping.com/shop/4674001/review_all')
    #PageParser().parse_svg_file('a974c69de518a0b1d9bda58f69bae6f5.svg.html')
    #parse_svg_file('test.xml')
    #pp.extract_comments()
    seg = "<span class=\"mrsc35\"></span>"
    r = re.findall('\"\w*\"', seg)[0]
    print(r[1:-1])



