#!/usr/bin/env python
# coding: utf-8

import re

from .utils import *

VALID_URL = r'(\.le\.com|letv)'

def extract(url):
    objs = []
    pages = [url]
    '''
    if re.search(r'list.', url):
        nextpage = re.search(r'<div class="next-page">.*?</div>', load(url), re.DOTALL|re.MULTILINE)
        if nextpage:
            for m in re.finditer(r'href="([^"]*)"', nextpage.group()):
                if m.group(1) not in pages:
                    pages.append(m.group(1))
    '''
    for page in pages[0:5]:
        for obj in findImageLink(page, ImageExt='png'):
            if re.search(r'/tv/', obj.link):
                image = re.search(r'\'(.*?.jpg)\'', obj.html)
                image = image.group(1) if image else None
                objs.append(obj.to_page())
            elif re.search(r'/vplay/', obj.link):
                image = re.search(r'\'([^\']*\.jpg)\'', obj.html)
                image = image.group(1) if image else None
                objs.append(obj.to_video())

    return objs
