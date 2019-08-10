#!/usr/bin/env python
# coding: utf-8

import re

from .utils import *

VALID_URL = r'pangzitv'

def extract(url):
    objs = []
    if re.search(r'vod-detail-id', url):
        for m in re.finditer(r'href="(/\?m=vod-play-id-[^"]*)" title="(.*?)"', load(url)):
            ep_url, ep_title = 'http://www.pangzitv.com' + m.group(1), m.group(2)
            objs.append(entryObj(ep_url, ep_title))
    elif re.search(r'(vod-type-id|vod-list-id)', url):
        for m in re.finditer(r'href="([^"]*)" .*? <img class="lazy" src="([^"]*)" alt="([^"]*)"', load(url)):
            p_url = 'http://www.pangzitv.com' + m.group(1)
            p_image = 'http://www.pangzitv.com' + m.group(2)
            p_title = m.group(3)
            objs.append(entryObj(p_url, p_title, p_image, video=False))
        for m in re.finditer(r'<a .*? href="([^"]*)".*?>(.*?)</a>', load(url)):
            if re.search(r'pagelink', m.group(0)):
                p_url = 'http://www.pangzitv.com' + m.group(1)
                objs.append(entryObj(p_url, m.group(2), 'Mimetypes-inode-directory-icon.png', video=False))

    return objs
