#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import xurl
import youtubedl

def search(patten, txt):
    m = re.search(patten, txt)
    if m:
        return m.group(1)
    return None

def findLink(url):
    urls = []
    for m in re.finditer(r'(http://|https://|)(www.|)(dailymotion|videomega|videowood|youtube|openload)(.com|.tv|.co)([^"]*)', xurl.load2(url)):
        link = xurl.absURL(m.group())
        if link not in urls:
            urls.append(link)
    srcs = []
    for link in urls:
        if youtubedl.checkURL(link):
            vids = youtubedl.extractURL2(link)
            if vids:
                srcs = srcs+vids
        else:
            srcs.append(link)
    return srcs

