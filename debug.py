import requests
import lxml.html
url= "https://en.wikipedia.org/w/index.php?title=Web_crawler&action=edit&section=2"
resp = requests.get(url)
print(resp.text[:500])
tree = lxml.html.fromstring(resp.text)
title = tree.xpath('//title')
print(title)