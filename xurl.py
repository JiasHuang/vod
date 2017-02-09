#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
import urllib
import urllib2
import hashlib
import urlparse
import time

import xdef

def verbose(url, local, agent):
    print('\n[xurl][%s]\n' %(agent))
    print('\tsrc: '+url)
    print('\tdst: '+local)
    return

def verbose_status(status):
    print('\tret: '+status)
    return

def readLocal(local):
    if os.path.exists(local):
        fd = open(local, 'r')
        txt = fd.read()
        fd.close()
        return txt
    return ''

def saveLocal(local, text):
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

def findSite(url):
    if re.search(r'://', url):
        m = re.search(r'://([^/]*)', url);
    else:
        m = re.search(r'([^/]*)', url);
    if m:
        return m.group(1)
    return ''

def parse(url):
    p = urlparse.urlparse(url)
    prefix = p.scheme + '://' + p.netloc + os.path.dirname(p.path) + '/'
    basename = os.path.basename(p.path)
    return prefix, basename

def absURL(url, site=None):
    if re.search(r'^//', url):
        return 'http:'+url
    if site and re.search(r'^/', url):
        return re.sub('^/', site, url)
    if not re.search(r'^http', url):
        return 'http://'+url
    return url

def wget(url, local, options=None):
    verbose(url, local, 'wget')
    if os.path.exists(local):
        verbose_status('already exist')
        return
    cmd = '%s -U \'%s\' -O %s \'%s\' %s' %(xdef.wget, xdef.ua, local, url, options or '')
    os.system(cmd)
    verbose_status('done')
    return

def get(url, local):
    verbose(url, local, 'urllib2')
    if os.path.exists(local):
        verbose_status('already exist')
        return
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/33.0')]
    try:
        f = opener.open(url)
        if f.info().get('Content-Encoding') == 'gzip':
            buf = StringIO(f.read())
            saveLocal(local, gzip.GzipFile(fileobj=buf).read())
        else:
            saveLocal(local, f.read())
        verbose_status('done')
    except:
        verbose_status('fail')
    return

def urlretrieve(url, local):
    verbose(url, local, 'urlretrieve')
    try:
        urllib.urlretrieve (url, local)
        verbose_status('done')
    except:
        verbose_status('fail')
    return

def load(url, local=None):
    url = absURL(url)
    local = local or xdef.workdir+'vod_load_'+hashlib.md5(url).hexdigest()
    get(url, local)
    return readLocal(local)

def post(url, payload, local=None):

    local = local or xdef.workdir+'vod_post_'+hashlib.md5(dict2str(payload)).hexdigest()
    if os.path.exists(local):
        verbose_status('already exist')
        return readLocal(local)

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/33.0')]
    data = urllib.urlencode(payload)
    try:
        f = opener.open(url, data)
        txt = f.read()
        saveLocal(local, txt)
        return txt
    except:
        return ''

def load2(url, local=None, options=None):
    url = absURL(url)
    local = local or xdef.workdir+'vod_load_'+hashlib.md5(url).hexdigest()
    wget(url, local, options)
    return readLocal(local)

def getFrame(url):
    frm = re.search(r'<iframe ([^>]*)>', load2(url))
    if frm :
        src = re.search(r'src="([^"]*)"', frm.group())
        if src:
            link = src.group(1)
            if re.search(r'^//', link):
                link = 'http:'+link
            return link
    return None

def getContentType(url):
    res = urllib.urlopen(url)
    info = res.info()
    res.close()
    return info.type

def saveCookies(local, url, rawdata):
    parsed_uri = urlparse.urlparse(url)
    domain = '{uri.netloc}'.format(uri=parsed_uri)
    expire = str(int(time.time())+20000)
    fd = open(local, 'w')
    for pair in rawdata.split(';'):
        m = re.search(r'([^=]*)=(.*)$', pair)
        if m:
            fd.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\n' %(domain, 'TRUE', '/', 'FALSE', expire, m.group(1), m.group(2)))
    fd.close()
    return
