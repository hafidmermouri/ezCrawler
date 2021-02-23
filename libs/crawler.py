import requests, json
import lxml.html
from config import *
from utils import *
from urllib.parse import urljoin, urlparse
from libs.cache import Cache
import datetime, codecs, csv

class Crawler() :
    def __init__(self):
        self.headers = {
            "user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7",
        }

        self.current_depth = 0
        self.visited_links = set()
        self.queue={}
        self.crawled_data= []
        self.csv_headers = []
    def init(self, url):
        parsed = urlparse(url)
        self.cache_dir = os.path.join(CACHE_DIR, parsed.netloc)
        self.output_dir =  os.path.join(OUTPUT_DIR, parsed.netloc)
        for f in [self.cache_dir, self.output_dir] :
            if not os.path.isdir(f) :
                os.makedirs(f, exist_ok=True)
        print(self.output_dir)
    def run(self, url):
        self.init(url)
        self.queue = []
        self.queue.append([url, 0])
        i=0
        while self.queue :
            if i >= MAX_URLS_COUNT :
                break

            u,depth = self.queue.pop(0)
            u=u.strip()
            uid = md5(u)
            res = self.crawl(uid, u)
            html = res["html"] #.content.decode('utf-8')
            if not html :
                continue
            tree = lxml.html.fromstring(html)
            links = self.find_links(u, tree, depth)
            res['links'] = links
            data = self.parse(tree)
            res['data'] = data
            self.csv_headers += [x for x in list(data.keys()) if x not in self.csv_headers]
            self.crawled_data.append(res)
            i+=1

        self.save()

    def save(self):
        filename = os.path.join(self.output_dir, "crawl_%s.csv" % str(datetime.date.today()))
        _sep=";"
        with codecs.open(filename, "w") as owt :
            row = ['url', 'status_code'] + [x for x in self.csv_headers] + ['\n']
            owt.write(_sep.join(row))
            for r in self.crawled_data :
                row = [r['url'], str(r['status_code'])]
                for x in self.csv_headers :
                    t=""
                    if x in r['data'] :
                        t = r['data'][x]
                    row.append(t)
                row +=['\n']
                owt.write(_sep.join(row))

    def crawl(self, uid, url):
        res = Cache.get(uid, dir=self.cache_dir)
        if res :
            res = json.loads(res)
            print("CACHED", res['status_code'], url)
            return res
        try :
            res = requests.get(url, headers=self.headers)
            res = self._tojson(res)
            Cache.set(uid, res, dir=self.cache_dir)
            print("CRAWLED", res['status_code'], url)
        except Exception as e :
            print("ERROR", url, e)

        return res
    def _tojson(self, r):
        res = {
            "status_code": r.status_code,
            "html": r.content.decode('utf-8'),
            "headers": r.headers.__dict__['_store'],
            "is_redirect": r.is_redirect,
            "url": r.url,
            "encoding": r.encoding
        }
        return res
    def _requests(self, url):
        pass
    def parse(self, tree):
        data = {}
        for name, xpath in PARSER_XPATH.items():
            row = tree.xpath(xpath)
            res = []
            for i, x in enumerate(row):
                rename=name.strip()
                if i > 0:
                    rename = "%s_%s" % (name, str(i+1))

                value = x.text_content()
                data.update({rename: value.strip()})
        return data
    def find_links(self, root, tree, depth):
        links = set()

        for link in tree.xpath("//a[@href]") :
            href = link.get('href').strip()
            href = self.get_absolute_link(root, href)
            if not href :
                continue
            uid = md5(href)
            if uid in self.visited_links :
                continue
            self.visited_links.add(uid)

            links.add(href)
            self.queue.append((href, depth+1))
        return links

    def get_absolute_link(self, url, href):
        href = href.split('#')[0]
        href = urljoin(url, href)
        if INTERNAL_LINKS_ONLY and urlparse(href).netloc != urlparse(url).netloc :
            return False

        return href
