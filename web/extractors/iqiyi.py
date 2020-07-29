#!/usr/bin/env python
# coding: utf-8

import re
import string

from .utils import *

VALID_URL = r'iqiyi'

def extract(url):
    objs = []
    if re.search(r'list.', url):
        category = re.search(r'www/(\d+)/', url) or 'err'
        category = category.group(1) if category else None
        pages = []
        pages.append(url)
        for m in re.finditer(r'<a data-key.*? href="([^"]*)"', load(url), re.DOTALL):
            page = urljoin(url, m.group(1))
            if page not in pages:
                pages.append(page)
        for page in pages[0:5]:
            for m in re.finditer(r'<div class="plist-item">(.*?)<p class="pic-sub-title">', load(page), re.DOTALL|re.MULTILINE):
                link = re.search(r'href="([^"]*)"', m.group(1))
                link = link.group(1) if link else None
                title = re.search(r'<a class="pic-title".*?>(.*?)</a>', m.group(1))
                title = title.group(1) if title else None
                image = re.search(r'v-i71-anim-img="\'([^\']*)\'"', m.group(1))
                image = image.group(1) if image else None
                if link and title and image:
                    link, image = urljoin(page, link, image)
                    objs.append(entryObj(link, title, image, video=(category == '1')))
    else:
        m = re.search(r'album-page="([^"]*)"', load(url))
        if m:
            albumPage = urljoin(url, m.group(1))
            for m in re.finditer(r'"name":"([^"]*)","url":"([^"]*)","imageUrl":"([^"]*)"', load(albumPage)):
                title, link, image = m.group(1), m.group(2), m.group(3)
                link, image = urljoin(url, link, image)
                objs.append(entryObj(link, title, image))

    return objs

def search_iqiyi(q, start=None):
    objs = []
    url = 'http://www.google.com/search?tbm=vid&num=100&hl=en&q=site%3Aiqiyi.com%20'+q
    if start:
        url = url+'&start='+start
    txt = load(url)
    img_codes = re.findall(r'var s=\'([^\']*)\'', txt)
    for m in re.finditer(r'<a href="(http:[^"]*\.iqiyi\.com/\w+\.html)".*?>(.*?)<img id="([^"]*)"', txt):
        link, desc, img_id = m.group(1), m.group(2), m.group(3)
        m2 = re.search(r'<h3.*?>(.*?)</h3>', desc)
        title = m2.group(1) if m2 else None
        m3 = re.search(r'"'+re.escape(img_id)+r'":"([^"]*)"', txt)
        image = m3.group(1).decode('unicode_escape') if m3 else None
        idx = int(img_id.strip(string.ascii_letters)) - 1
        if not image and idx < len(img_codes):
            image = img_codes[idx].decode('unicode_escape')
        if link and title:
            objs.append(entryObj(link, title, image))

    return objs
