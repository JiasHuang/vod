#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import xurl
import youtubedl

def findLink(url):
    urls = []
    for m in re.finditer(r'(http://|https://|)(www.|)(dailymotion|videomega|videowood|youtube|openload)(.com|.tv|.co)([^"]*)', xurl.load2(url)):
        link = xurl.absURL(m.group())
        if link not in urls:
            urls.append(link)
    srcs = []
    for link in urls:
        if youtubedl.checkURL(link):
            link = youtubedl.extractURL(link)
        srcs.append(link)
    return srcs

