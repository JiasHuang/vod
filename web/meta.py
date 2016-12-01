#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import urllib
import urllib2
import json
import urlparse
import hashlib
import conf

from StringIO import StringIO
import gzip

import page

def readLocal(local):
    with open(local, 'r') as fd:
        return fd.read()
    return ''

def saveLocal(text, local):
    fd = open(local, 'w')
    fd.write(text)
    fd.close()
    return

def load(url, local=None):
    if not local:
        local = conf.workdir+'vod_load_'+hashlib.md5(url).hexdigest()
    if os.path.exists(local):
        return readLocal(local)
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/33.0')]
    try:
        f = opener.open(url)
        if f.info().get('Content-Encoding') == 'gzip':
            buf = StringIO(f.read())
            return gzip.GzipFile(fileobj=buf).read()
        txt = f.read()
        saveLocal(txt, local)
        return txt
    except:
        return ''

def absURL(domain, url):
    if re.search(r'^/', url):
        return domain+url
    return url

def findPoster(link):
    poster = re.search(r'poster="([^"]*)"', load(link))
    if poster:
        return poster.group(1)
    return None

def getImage(link):

    m = re.search(r'www.youtube.com/(watch\?v=|embed/)(.{11})', link)
    if m:
        return 'http://img.youtube.com/vi/%s/0.jpg' %(m.group(2))

    m = re.search(r'http://www.dailymotion.com/(embed/|)video/(.*)', link)
    if m:
        return 'http://www.dailymotion.com/thumbnail/video/'+m.group(2)

    m = re.search(r'youku.com/(embed/|v_show/id_)([0-9a-zA-Z]*)', link)
    if m:
        return 'http://events.youku.com/global/api/video-thumb.php?vid=' + m.group(2)

    m = re.search(r'(openload.co|videomega.tv|up2stream.com)', link)
    if m:
        return findPoster(link)

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

def findImageLink(req, url, unquote=False, showPage=False):
    txt = load(url)
    for m in re.finditer(r'<a .*?</a>', txt, re.DOTALL):
        link = re.search(r'href="([^"]*)"', m.group(0))
        image = re.search(r'src="([^"]*)"', m.group(0))
        if link and image:
            if unquote == True:
                link1 = urllib.unquote(link.group(1))
            else:
                link1 = link.group(1)
            image1 = image.group(1)
            if showPage == False:
                page.addVideo(req, link1, link1, image1)
            else:
                page.addPage(req, link1, link1, image1)

def findVideo(req, url):
    return findVideoLink(req, url)

def findPage(req, url, showImage=False):
    return findVideoLink(req, url, True, showImage)

def findLink(req, url):
    link = ''
    txt = load(url)
    for m in re.finditer(r'"http(s|)://(www.|)(dailymotion|videomega|videowood|youtube|openload)(.com|.tv|.co)([^"]*)', txt):
        if m.group()[1:-1] != link:
            link = m.group()[1:-1]
            image = getImage(link)
            page.addVideo(req, link, link, image)

