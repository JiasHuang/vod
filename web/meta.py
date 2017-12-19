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

import conf
import page

gDebugLog = []
itemResult = []

class defs:
    linkPattern = r'http(s|)://(www.|)(redirector.googlevideo|dailymotion|videomega|videowood|youtube|openload)(.com|.tv|.co)([^"]*)'

class entryObj(object):
    url = None
    title = None
    image = None

    def __init__(self, url, title, image):
        self.url = url
        self.title = title
        self.image = image

def search(pattern, txt, flags=0):
    if not txt:
        return None
    m = re.search(pattern, txt, flags)
    if m:
        return m.group(1)
    return None

def readLocal(local, buffering=-1):
    if os.path.exists(local):
        fd = open(local, 'r', buffering)
        txt = fd.read()
        fd.close()
        return txt
    return ''

def saveLocal(local, text, buffering=-1):
    fd = open(local, 'w', buffering)
    fd.write(text)
    fd.close()
    return

def checkExpire(local):
    t0 = int(os.path.getmtime(local))
    t1 = int(time.time())
    if (t1 - t0) > 3600:
        return True
    return False

def dict2str(adict):
    return ''.join('{}{}'.format(key, val) for key, val in adict.items())

def genLocal(url, prefix=None, suffix=None):
    global gDebugLog
    local = conf.workdir+(prefix or 'vod_load_')+hashlib.md5(url).hexdigest()+(suffix or '')
    gDebugLog.append('%s -> %s' %(url, local))
    return local

def load(url, local=None, headers=None, cache=True):

    local = local or genLocal(url)
    if cache and os.path.exists(local) and not checkExpire(local):
        return readLocal(local)

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', conf.ua)]

    if headers:
        opener.addheaders += headers

    try:
        f = opener.open(url, None, 10) # timeout=10
        if f.info().get('Content-Encoding') == 'gzip':
            buf = StringIO(f.read())
            txt = gzip.GzipFile(fileobj=buf).read()
        else:
            txt = f.read()
        saveLocal(local, txt)
        return txt
    except urllib2.HTTPError, e:
        return 'Exception HTTPError: ' + str(e.code)
    except urllib2.URLError, e:
        return 'Exception URLError: ' + str(e.reason)
    except httplib.HTTPException, e:
        return 'Exception HTTPException'
    except :
        return 'Exception'

def post(url, payload, local=None, headers=None, cache=True):

    local = local or genLocal(url)
    if cache and os.path.exists(local) and not checkExpire(local):
        return readLocal(local)

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', conf.ua)]

    if headers:
        opener.addheaders += headers

    data = urllib.urlencode(payload)
    try:
        f = opener.open(url, data)
        txt = f.read()
        saveLocal(local, txt)
        return txt
    except:
        return ''

def wget_refresh(url, local, options=None):
    output = readLocal(conf.log_wget)
    if re.search(r'ERROR 503', output):
        parsed_uri = urlparse.urlparse(url)
        domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
        m = re.search(r'Refresh: (\d+);URL=(.*?)\n', output, re.DOTALL)
        if m:
            time.sleep(float(m.group(1)))
            newURL = absURL(domain, m.group(2))
            cmd = '%s -O %s \'%s\' %s' %(conf.wget, local, newURL, options or '')
            os.system(cmd)

def wget(url, local, options=None):
    cmd = '%s -O %s \'%s\' %s' %(conf.wget, local, url, options or '')
    try:
        subprocess.check_output(cmd, shell=True)
    except:
        wget_refresh(url, local, options)

def load2(url, local=None, options=None, cache=True, ref=None):

    local = local or genLocal(url)
    if cache and os.path.exists(local) and not checkExpire(local):
        return readLocal(local)
    if ref:
        options = (options or '') + ' --referer='+ref
    wget(url, local, options)
    return readLocal(local)

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
    return search(r'poster="([^"]*)"', load2(link))

def getImage(link):

    m = re.search(r'www.youtube.com/(watch\?v=|embed/)(.{11})', link)
    if m:
        return 'http://img.youtube.com/vi/%s/0.jpg' %(m.group(2))

    m = re.search(r'https?://www.dailymotion.com/(embed/|)video/(.*)', link)
    if m:
        return 'http://www.dailymotion.com/thumbnail/video/'+m.group(2)

    m = re.search(r'youku.com/(embed/|v_show/id_)([0-9a-zA-Z]*)', link)
    if m:
        return 'http://events.youku.com/global/api/video-thumb.php?vid=' + m.group(2)

    m = re.search(r'(openload.co|videomega.tv|up2stream.com)', link)
    if m:
        return findPoster(link)

    m = re.search(r'http(s|)://drive.google.com/file/d/(\w*)', link)
    if m:
        #return search(r'<meta property="og:image" content="([^"]*)">', load(m.group()))
        return 'https://drive.google.com/thumbnail?authuser=0&sz=w320&id='+m.group(2)

    return None

def comment(req, msg):
    req.write('\n<!--\n')
    req.write(msg)
    req.write('\n-->\n')
    return

def findVideoLink(req, url, showPage=False, showImage=False, ImageSrc='src', ImageExt='jpg', ImagePattern=None):
    parsed_uri = urlparse.urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    txt = load2(url)
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
    txt = load2(url)
    objs = []
    for m in re.finditer(r'<a\s.*?</a>', txt, re.DOTALL|re.MULTILINE):
        link = search(r'href\s*=\s*"([^"]*)"', m.group(0))
        image = search(r'src\s*=\s*"(.*?\.jpg)"', m.group(0))
        title = search(r'alt\s*=\s*"([^"]*)"', m.group(0)) or search(r'title\s*=\s*"([^"]*)"', m.group(0))
        if link and image:
            if unquote == True:
                link = urllib.unquote(link)
            link = absURL(domain, link)
            if urlparse.urlparse(link).path.rstrip('/') == '':
                continue
            if not req:
                objs.append(entryObj(link, title or link, image))
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
    txt = load2(url)
    for m in re.finditer(defs.linkPattern, txt):
        if m.group() != link:
            link = m.group()
            image = getImage(link)
            page.addVideo(req, link, link, image)

def findFrame(req, url):
    for m in re.finditer(r'<iframe (.*?)</iframe>', load2(url)):
        src = re.search(r'src="([^"]*)"', m.group(1))
        if src:
            if re.search(defs.linkPattern, src.group(1)):
                page.addVideo(req, src.group(1))

def parseJSON(txt):
    try:
        return json.loads(txt)
    except:
        return {}

def showDebugLog(req):
    global gDebugLog
    req.write('\n\n<!--DebugLog-->\n')
    for l in gDebugLog:
        req.write('<!-- %s -->\n' %(l))

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
