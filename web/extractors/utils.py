#!/usr/bin/env python
# coding: utf-8

import re
import json

import xurl

itemResult = []

class entryObj(object):
    def __init__(self, link, title=None, image=None, desc=None, video=True):
        self.link = link
        self.title = title or link
        self.image = image
        self.desc = desc
        self.video = video
    def show(self):
        print('\tlink: %s' %(self.link))
        print('\ttitle: %s' %(self.title or ''))
        print('\timage: %s' %(self.image or ''))
        print('\tdesc: %s' %(self.desc or ''))
        print('\tvideo: %s' %(self.video))

class videoObj(entryObj):
    def __init__(self, link, title=None, image=None, desc=None):
        self.link = link
        self.title = title or link
        self.image = image
        self.desc = desc
        self.video = True

class pageObj(entryObj):
     def __init__(self, link, title=None, image=None, desc=None):
        self.link = link
        self.title = title or link
        self.image = image
        self.desc = desc
        self.video = False

class navObj(object):
    def __init__(self, label, link):
        self.label = label
        self.link = link
    def show(self):
        print('\tlabel: %s' %(self.label))
        print('\tlink: %s' %(self.link))

class imageObj(object):
    def __init__(self, link, title, image, html):
        self.link = link
        self.title = title
        self.image = image
        self.html = html
    def to_page(self):
        return pageObj(self.link, self.title, self.image)
    def to_video(self):
        return videoObj(self.link, self.title, self.image)

def load(url):
    return xurl.curl(url)

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

def darg(d, *arg):
    if len(arg) == 1:
        return d[arg[0]].encode('utf8')
    return [d[a].encode('utf8') for a in arg]

def urljoin(url, *arg):
    if len(arg) == 1:
        return xurl.urljoin(url, arg[0])
    return [xurl.urljoin(url, a) for a in arg]

def findImageLink(url, ImageExt='jpg', ImagePattern=r'src\s*=\s*"([^"]*)"'):
    txt = load(url)
    objs = []
    for m in re.finditer(r'<a\s.*?</a>', txt, re.DOTALL|re.MULTILINE):
        link = re.search(r'href\s*=\s*"([^"]*)"', m.group(0))
        link = link.group(1) if link else None
        image = re.search(ImagePattern, m.group(0))
        image = image.group(1) if image else None
        title = re.search(r'alt\s*=\s*"([^"]*)"', m.group(0)) or re.search(r'title\s*=\s*"([^"]*)"', m.group(0))
        title = title.group(1) if title else None
        if not link or not image:
            continue
        if ImageExt and not image.endswith(ImageExt):
            continue
        link = xurl.urljoin(url, xurl.unquote(link))
        image = xurl.urljoin(url, xurl.unquote(image))
        objs.append(imageObj(link, title or link, image, m.group(0)))
    return objs

def getLink(site, vid):
    if site == 'youtube':
        return 'https://www.youtube.com/watch?v='+vid
    if site == 'dailymotion':
        return 'http://www.dailymotion.com/video/'+vid
    if site == 'openload':
        return 'https://openload.co/embed/'+vid
    if site == 'googledrive':
        return 'https://drive.google.com/file/d/'+vid
    return None

def getTitle(site, index, cnt):
    title = site.title()
    if cnt > 1:
        title += ' Part %d/%d' %(index, cnt)
    return title

