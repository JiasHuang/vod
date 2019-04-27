#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import urllib
import urllib2
import urlparse
import hashlib
import time
import json
import subprocess

from StringIO import StringIO
import gzip

import page
import xurl

itemResult = []

class defs:
    linkPattern = r'http(s|)://(www.|)(redirector.googlevideo|dailymotion|videomega|videowood|youtube|openload)(.com|.tv|.co)([^"]*)'

class entryObj(object):
    url = None
    title = None
    image = None

    def __init__(self, url, title, image, html):
        self.url = url
        self.title = title
        self.image = image
        self.html = html

def search(pattern, txt, flags=0):
    if not txt:
        return None
    m = re.search(pattern, txt, flags)
    if m:
        return m.group(1)
    return None

def findPoster(link, referer=None):
    return search(r'poster="([^"]*)"', xurl.load2(link, ref=referer))

def getImage(link, referer=None):

    m = re.search(r'www.youtube.com/(watch\?v=|embed/)(.{11})', link)
    if m:
        return 'http://img.youtube.com/vi/%s/0.jpg' %(m.group(2))

    m = re.search(r'https?://www.dailymotion.com/(embed/|)video/(.*)', link)
    if m:
        return 'http://www.dailymotion.com/thumbnail/video/'+m.group(2)

    m = re.search(r'youku.com/(embed/|v_show/id_)([0-9a-zA-Z]*)', link)
    if m:
        return 'http://events.youku.com/global/api/video-thumb.php?vid=' + m.group(2)

    m = re.search(r'(openload.co|videomega.tv|up2stream.com|rapidvideo)', link)
    if m:
        return findPoster(link, referer)

    m = re.search(r'http(s|)://drive.google.com/file/d/(\w*)', link)
    if m:
        #return search(r'<meta property="og:image" content="([^"]*)">', load(m.group()))
        return 'https://drive.google.com/thumbnail?authuser=0&sz=w320&id='+m.group(2)

    return None

def comment(req, msg):
    msg = re.sub('<!--', '<___>', msg)
    msg = re.sub('-->', '</___>', msg)
    req.write('\n<!--\n')
    req.write(msg)
    req.write('\n-->\n')
    return

def findVideoLink(req, url, showPage=False, showImage=False, ImageSrc='src', ImageExt='jpg', ImagePattern=None, cmd=None):
    txt = xurl.load2(url, cmd=cmd)
    for m in re.finditer(r'<a .*?</a>', txt, re.DOTALL):
        link = search(r'href="([^"]*)"', m.group(0))
        title = search(r'title="([^"]*)"', m.group(0))
        if ImagePattern:
            image = search(ImagePattern, m.group(0))
        else:
            image = search(re.escape(ImageSrc)+r'="([^"]*)"', m.group(0))
        if image and ImageExt and not image.endswith(ImageExt):
            continue
        if link and not ImageExt:
            parsed_link = urlparse.urlparse(link)
            if parsed_link.path == '/':
                continue
        if link and title and image:
            link = xurl.absURL(link)
            image = xurl.absURL(image)
            if showPage == False:
                page.addVideo(req, link, title, image)
            elif showImage == True:
                page.addPage(req, link, title, image)
            else:
                page.addPage(req, link, title)

def findImageLink(req, url, unquote=False, showPage=False, ImageExt='jpg', ImagePattern=None):
    parsed_uri = urlparse.urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    txt = xurl.load2(url)
    objs = []
    for m in re.finditer(r'<a\s.*?</a>', txt, re.DOTALL|re.MULTILINE):
        link = search(r'href\s*=\s*"([^"]*)"', m.group(0))
        if ImagePattern:
            image = search(ImagePattern, m.group(0))
        else:
            image = search(r'src\s*=\s*"([^"]*)"', m.group(0))
        title = search(r'alt\s*=\s*"([^"]*)"', m.group(0)) or search(r'title\s*=\s*"([^"]*)"', m.group(0))
        if image and ImageExt and not image.endswith(ImageExt):
            continue
        if link and image:
            if unquote == True:
                link = urllib.unquote(link)
            if not req:
                objs.append(entryObj(link, title or link, image, m.group(0)))
                continue
            if showPage == False:
                page.addVideo(req, link, title or link, image)
            else:
                page.addPage(req, link, title or link, image)
    if not req:
        return objs

def findVideo(req, url):
    return findVideoLink(req, url)

def findPage(req, url, showImage=False):
    return findVideoLink(req, url, True, showImage)

def findLink(req, url):
    link = ''
    txt = xurl.load2(url)
    for m in re.finditer(defs.linkPattern, txt):
        if m.group() != link:
            link = m.group()
            image = getImage(link)
            page.addVideo(req, link, link, image)

def findFrame(req, url):
    for m in re.finditer(r'<iframe (.*?)</iframe>', xurl.load2(url)):
        src = re.search(r'src="([^"]*)"', m.group(1))
        if src:
            if re.search(defs.linkPattern, src.group(1)):
                page.addVideo(req, src.group(1))

def parseJSON(txt):
    try:
        return json.loads(txt)
    except:
        return {}

def findItem_reentry(obj, keys):
    global itemResult
    if type(obj) is dict:
        for x in obj:
            if x in keys:
                itemResult.append(obj[x])
            else:
                findItem_reentry(obj[x], keys)
    elif type(obj) is list:
        for x in obj:
            findItem_reentry(x, keys)

def findItem(obj, keys):
    global itemResult
    itemResult = []
    findItem_reentry(obj, keys)
    return itemResult
