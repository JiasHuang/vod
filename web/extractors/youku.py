#!/usr/bin/env python
# coding: utf-8

import re

from utils import *

VALID_URL = r'youku'

def extract(url):
    objs = []
    for m in re.finditer(r'<div class="p-thumb">(.*?)</div>', load(url)):
        link = re.search(r'href="([^"]*)"', m.group())
        link = link.group(1) if link else None
        title = re.search(r'title="([^"]*)"', m.group())
        title = title.group(1) if title else None
        image = re.search(r'src="([^"]*)"', m.group())
        image = image.group(1) if image else None
        link, image = urljoin(url, link, image)
        objs.append(entryObj(link, title, image))

    return objs
