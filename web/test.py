#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import json

import page
import meta
import xurl

def autotest():
    list_pass = []
    list_fail = []
    fd = open('/dev/null', 'w')
    bookmarkJSONURL = 'https://gist.githubusercontent.com/JiasHuang/30f6cc0f78ee246c1e28bd537764d6c4/raw/bookmark.json'
    data = meta.parseJSON(xurl.load2(bookmarkJSONURL))
    for d in data['channels']:
        channel = d['channel']
        for x in d['links']:
            title, link = x['title'], x['link']
            test = '[%s][%s] %s' %(channel, title, link)
            try:
                page.reset()
                page.page_core(fd, link)
            except:
                page.entryCnt = 0
            if page.entryCnt <= 0:
                list_fail.append(test)
            else:
                list_pass.append(test)
    print('\n--- pass ---\n')
    print('\n'.join(list_pass))
    print('\n--- fail ---\n')
    print('\n'.join(list_fail))
    fd.close()

def main():

    if len(sys.argv) < 2:
        autotest()
        return

    fd = open('output.html', 'w')

    m = re.search(r'load.py\?(.*?)$', sys.argv[1])
    if m:
        q = meta.search(r'q=([^&]*)', m.group(1))
        s = meta.search(r's=([^&]*)', m.group(1))
        x = meta.search(r'x=([^&]*)', m.group(1))
        p = meta.search(r'p=([^&]*)', m.group(1))
        if q:
            page.search(fd, q, s, x)
        if p:
            page.page_core(fd, p)
    else:
        page.page(fd, sys.argv[1])

    fd.close()
    return

if __name__ == '__main__':
    main()
