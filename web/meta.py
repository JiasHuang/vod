#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import urllib
import urllib2
import urlparse
import hashlib
import time

from StringIO import StringIO
import gzip

import conf
import page

def search(patten, txt):
    m = re.search(patten, txt)
    if m:
        return m.group(1)
    return None

def readLocal(local):
    with open(local, 'r') as fd:
        return fd.read()
    return ''

def saveLocal(text, local):
    fd = open(local, 'w')
    fd.write(text)
    fd.close()
    return

def checkExpire(local):
    t0 = int(os.path.getmtime(local))
    t1 = int(time.time())
    if (t1 - t0) > 14400:
        return True
    return False

def dict2str(adict):
    return ''.join('{}{}'.format(key, val) for key, val in adict.items())

def load(url, local=None, headers=None, cache=True):

    local = local or conf.workdir+'vod_load_'+hashlib.md5(url).hexdigest()
    if cache and os.path.exists(local) and not checkExpire(local):
        return readLocal(local)

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/33.0')]

    if headers:
        opener.addheaders += headers

    try:
        f = opener.open(url, None, 10) # timeout=10
        if f.info().get('Content-Encoding') == 'gzip':
            buf = StringIO(f.read())
            txt = gzip.GzipFile(fileobj=buf).read()
        else:
            txt = f.read()
        saveLocal(txt, local)
        return txt
    except:
        return ''

def post(url, payload, local=None, cache=True):

    local = local or conf.workdir+'vod_post_'+hashlib.md5(dict2str(payload)).hexdigest()
    if cache and os.path.exists(local) and not checkExpire(local):
        return readLocal(local)

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/33.0')]
    data = urllib.urlencode(payload)
    try:
        f = opener.open(url, data)
        txt = f.read()
        saveLocal(txt, local)
        return txt
    except:
        return ''

def getContentType(url):
    res = urllib.urlopen(url)
    info = res.info()
    res.close()
    return info.type

def absURL(domain, url):
    if re.search(r'^//', url):
        return 'http:'+url
    if re.search(r'^/', url):
        return domain+url
    if not re.search(r'^http', url):
        return domain+'/'+url
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

def comment(req, msg):
    req.write('\n<!--\n')
    req.write(msg)
    req.write('\n-->\n')
    return

def findVideoLink(req, url, showPage=False, showImage=False, ImageSrc='src', ImageExt='jpg'):
    parsed_uri = urlparse.urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    txt = load(url)
    for m in re.finditer(r'<a .*?</a>', txt, re.DOTALL):
        link = search(r'href="([^"]*)"', m.group(0))
        title = search(r'title="([^"]*)"', m.group(0))
        image = search(re.escape(ImageSrc)+r'="([^"]*)"', m.group(0))
        if image and ImageExt and not image.endswith(ImageExt):
            continue
        if link and title and image:
            link = absURL(domain, link)
            image = absURL(domain, image)
            if showPage == False:
                page.addVideo(req, link, title, image)
            elif showImage == True:
                page.addPage(req, link, title, image)
            else:
                page.addPage(req, link, title)

def findImageLink(req, url, unquote=False, showPage=False):
    parsed_uri = urlparse.urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    txt = load(url)
    for m in re.finditer(r'<a .*?</a>', txt, re.DOTALL):
        link = search(r'href="([^"]*)"', m.group(0))
        image = search(r'src="(.*?\.jpg)"', m.group(0))
        title = search(r'alt="([^"]*)"', m.group(0))
        if link and image:
            if unquote == True:
                link = urllib.unquote(link)
            link = absURL(domain, link)
            if urlparse.urlparse(link).path.rstrip('/') == '':
                continue
            if showPage == False:
                page.addVideo(req, link, title or link, image)
            else:
                page.addPage(req, link, title or link, image)

def findVideo(req, url):
    return findVideoLink(req, url)

def findPage(req, url, showImage=False):
    return findVideoLink(req, url, True, showImage)

def findLink(req, url):
    link = ''
    txt = load(url)
    for m in re.finditer(r'"http(s|)://(www.|)(redirector.googlevideo|dailymotion|videomega|videowood|youtube|openload)(.com|.tv|.co)([^"]*)', txt):
        if m.group()[1:-1] != link:
            link = m.group()[1:-1]
            image = getImage(link)
            page.addVideo(req, link, link, image)

def findFrame(req, url):
    for m in re.finditer(r'<iframe (.*?)</iframe>', load(url)):
        src = re.search(r'src="([^"]*)"', m.group(1))
        if src:
            page.addVideo(req, src.group(1))

