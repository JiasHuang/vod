#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import json

import extractors
import xurl

def autotest():
    list_pass = []
    list_fail = []
    bookmarkJSONURL = 'https://gist.githubusercontent.com/JiasHuang/30f6cc0f78ee246c1e28bd537764d6c4/raw/bookmark.json'
    data = json.loads(xurl.load(bookmarkJSONURL))
    for d in data['channels']:
        channel = d['channel'].encode('utf8')
        for x in d['links']:
            title = x['title'].encode('utf8')
            link = x['link'].encode('utf8')
            test = '[%s][%s] %s' %(channel, title, link)
            m = re.search(r'view.py\?(.*?)$', link)
            if m:
                q = re.search(r'q=([^&]*)', m.group(1))
                q = q.group(1) if q else None
                s = re.search(r's=([^&]*)', m.group(1))
                s = s.group(1) if s else None
                x = re.search(r'x=([^&]*)', m.group(1))
                x = x.group(1) if x else None
                p = re.search(r'p=([^&]*)', m.group(1))
                p = p.group(1) if p else None
                if q:
                    entryCnt = len(extractors.search(q, s, x))
                if p:
                    entryCnt = len(extractors.extract(p))
            else:
                entryCnt = len(extractors.extract(link))
            if entryCnt <= 0:
                list_fail.append(test)
            else:
                list_pass.append(test)
    print('\n--- pass ---\n')
    print('\n'.join(list_pass))
    print('\n--- fail ---\n')
    print('\n'.join(list_fail))

def main():

    if len(sys.argv) < 2:
        autotest()
        return

    m = re.search(r'(view\.py|load\.py|search\.html)\?(.*?)$', sys.argv[1])
    if m:
        q = re.search(r'q=([^&]*)', m.group(2))
        q = q.group(1) if q else None
        s = re.search(r's=([^&]*)', m.group(2))
        s = s.group(1) if s else None
        x = re.search(r'x=([^&]*)', m.group(2))
        x = x.group(1) if x else None
        p = re.search(r'p=([^&]*)', m.group(2))
        p = p.group(1) if p else None
        if q:
            extractors.search_debug(q, s, x)
        if p:
            extractors.extract_debug(p)
    else:
        extractors.extract_debug(sys.argv[1])

    return

if __name__ == '__main__':
    main()
