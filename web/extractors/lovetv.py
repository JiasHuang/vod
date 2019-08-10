#!/usr/bin/env python
# coding: utf-8

import re

from .utils import *

VALID_URL = r'lovetv'

def extract(url):
    objs = []
    if re.search(r'special-drama-list.html$', url):
        for m in re.finditer(r'<a href="([^"]*)">([^<]*)</a>', load(url)):
            if re.search(r'special-drama-([0-9-]+).html$', m.group(1)):
                link = urljoin(url, m.group(1))
                title = m.group(2)
                objs.append(pageObj(link, title))
    elif re.search(r'(drama-list.html|/)$', url):
        for m in re.finditer(r'<a href=[\'|"]([^\'"]*)[\'|"]>([^<]*)</a>', load(url)):
            if re.search(r'(-list|/label/)', m.group(1)):
                link = urljoin(url, m.group(1))
                title = m.group(2)
                objs.append(entryObj(link, title, video=False))
    elif re.search(r'(-list|/label/)', url):
        for m in re.finditer(r'<a href=["|\'](.*?)["|\']>([^<]*)</a>', load(url)):
            if re.search(r'-ep([0-9]+).html$', m.group(1)):
                link = urljoin(url, m.group(1))
                title = m.group(2)
                objs.append(entryObj(link, title, video=False))
    else:
        video_types = {'1':'youtube', '2':'dailymotion', '3':'openload', '21':'googledrive'}
        txt = load(url)
        m = re.search(r'密碼：(\w+)', txt)
        password = m.group(1) if m else None
        for m in re.finditer(r'<div id="video_div(|_s[0-9])">.*?</div>\n*</div>', txt, re.DOTALL|re.MULTILINE):
            video_ids = re.search(r'video_ids.*?>([^<]*)</div>', m.group())
            video_ids = video_ids.group(1) if video_ids else None
            video_type = re.search(r'video_type.*?>([^<]*)</div>', m.group())
            video_type = video_type.group(1) if video_type else None
            if not video_type or not video_ids or video_type not in video_types:
                continue
            videos = video_ids.split(',')
            vcnt = len(videos)
            for videoIndex, video in enumerate(videos, 1):
                site = video_types[video_type]
                link = getLink(site, video)
                title = getTitle(site, videoIndex, vcnt)
                objs.append(entryObj(link, title))

    return objs
