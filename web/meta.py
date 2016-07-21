#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
import urllib2
import json
import urlparse
import page

def load(url):
    headers={'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/33.0'}
    r = requests.get(url, headers=headers)
    if r.encoding == 'utf-8' or r.apparent_encoding == 'utf-8':
        return r.content
    return r.text.encode('utf8')

def load2(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/33.0')]
    return opener.open(url).read()

def absURL(domain, url):
    if re.search(r'^/', url):
        return domain+url
    return url

def getImage(link):
    m = re.search(r'www.youtube.com/watch\?v=(.{11})', link)
    if m:
        return 'http://img.youtube.com/vi/%s/0.jpg' %(m.group(1))
    m = re.search(r'http://www.dailymotion.com/video/(.*)', link)
    if m:
        return 'http://www.dailymotion.com/thumbnail/video/'+m.group(1)
    return None

def findVideoLink(req, url, showPage=False, showImage=False):
    parsed_uri = urlparse.urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    txt = load(url)
    for m in re.finditer(r'<a .*?</a>', txt, re.DOTALL):
        link = re.search(r'href="([^"]*)"', m.group(0))
        title = re.search(r'title="([^"]*)"', m.group(0))
        image = re.search(r'src="([^"]*)"', m.group(0))
        if link and title and image:
            link1 = absURL(domain, link.group(1))
            title1 = title.group(1)
            image1 = absURL(domain, image.group(1))
            if showPage == False:
                page.addVideo(req, link1, title1, image1)
            elif showImage == True:
                page.addPage(req, link1, title1, image1)
            else:
                page.addPage(req, link1, title1)

def findVideo(req, url):
    return findVideoLink(req, url)

def findPage(req, url, showImage=False):
    return findVideoLink(req, url, True, showImage)

def findLink(req, url):
    link = ''
    for m in re.finditer(r'http://(www.dailymotion.com|videomega.tv|videowood.tv|www.youtube.com)/([0-9a-zA-Z=/_?.]*)', load(url)):
        if m.group() != link:
            link = m.group()
            image = getImage(link)
            page.addVideo(req, link, link, image)

