#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
import urllib
import urllib2
import hashlib
import xdef

def verbose(url, local, agent):
    print('\n[xurl][%s]\n' %(agent))
    print('\tsrc: '+url)
    print('\tdst: '+local)
    return 0

def verbose_status(status):
    print('\tret: '+status)
    return 0

def readLocal(local):
    with open(local, 'r') as fd:
        return fd.read()
    return ''

def saveLocal(text, local):
    fd = open(local, 'w')
    fd.write(text)
    fd.close()
    return

def findSite(url):
    m = re.search(r'://([^/]*)', url);
    if m:
        return m.group(1)
    return ''

def absURL(url, site=None):
    if re.search(r'^//', url):
        return 'http:'+url
    if site and re.search(r'^/', url):
        return re.sub('^/', site, url)
    if not re.search(r'^http', url):
        return 'http://'+url
    return url

def wget(url, local):
    verbose(url, local, 'wget')
    if os.path.exists(local):
        verbose_status('already exist')
        return 0
    cmd = '%s -U \'%s\' -O %s \'%s\' ' %(xdef.wget, xdef.ua, local, url)
    os.system(cmd.encode('utf8'))
    verbose_status('done')
    return 0

def get(url, local):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/33.0')]
    try:
        f = opener.open(url)
        if f.info().get('Content-Encoding') == 'gzip':
            buf = StringIO(f.read())
            return gzip.GzipFile(fileobj=buf).read()
        saveLocal(f.read(), local)
    except:
        return

def urlretrieve(url, local):
    verbose(url, local, 'urlretrieve')
    try:
        urllib.urlretrieve (url, local)
        verbose_status('done')
    except:
        verbose_status('fail')
    return 0

def load(url, local=None):
    url = absURL(url)
    if not local:
        local = xdef.workdir+'load_'+hashlib.md5(url).hexdigest()
    get(url, local)
    return readLocal(local)

def post(url, payload):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/33.0')]
    data = urllib.urlencode(payload)
    try:
        f = opener.open(url, data)
        return f.read()
    except:
        return ''

def load2(url, local=None):
    url = absURL(url)
    if not local:
        local = xdef.workdir+'load_'+hashlib.md5(url).hexdigest()
    wget(url, local)
    return readLocal(local)

