import re
import json
import base64

from .utils import *

VALID_URL = r'dramasq'

def extract(url):
    objs = []
    if url.endswith(('/jp/', '/kr/', '/cn/', '/tw/', '/th/')):
        txt = load(url)
        for m in re.finditer(r'<a href="(.*?)">(.*?)</a>', txt, re.DOTALL | re.MULTILINE):
            if not re.search(r'\d+/$', m.group(1)):
                continue
            link = urljoin(url, m.group(1))
            img = re.search(r'background-image: url\((.*?)\)', m.group(2))
            if img:
                title = re.search(r'<div class="title sizing">([^<]*)</div>', m.group(2))
                if img and title:
                    objs.append(entryObj(link, title.group(1), img.group(1), video=False))
            else:
                objs.append(entryObj(link, m.group(2), video=False))
    elif url.endswith('/'):
        txt = load(url)
        for m in re.finditer(r'<li><a href="([^"]*)">([^<]*)</a></li>', txt):
            link = urljoin(url, m.group(1))
            objs.append(entryObj(link, m.group(2), video=False))
        if not len(objs):
            for m in re.finditer(r'xxx\(\'(\w+)\',\'(\w+)\'', txt):
                if m.group(1) != 'none':
                    link = url + m.group(2) + '.html'
                    objs.append(entryObj(link, m.group(2), video=False))
    else:
        for m in re.finditer(r'data-data="([^"]*)"', load(url)):
            dict_str = base64.b64decode(m.group(1)[::-1])
            dict_obj = eval(dict_str)
            for i in range(len(dict_obj['ids'])):
                link = 'https://dramasq.cc/a/m3u8/?ref=' + dict_obj['ids'][i]
                title = dict_obj['source']
                if len(dict_obj['ids']) > 1:
                    title += ' %d/%d' %(i + 1, len(dict_obj['ids']))
                objs.append(entryObj(link, title, video=True))
    return objs
