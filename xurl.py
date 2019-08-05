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
import subprocess
import StringIO
import gzip

gDebugLog = []
domain = None

class defvals:
    workdir             = '/var/tmp/'
    wget_path_cookie    = workdir+'vod_wget.cookie'
    ua                  = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    wget_opt_base       = 'wget -T 10 -S'
    wget_opt_cookie     = '--save-cookies %s --load-cookies %s' %(wget_path_cookie, wget_path_cookie)
    wget_opt_ua         = '-U \'%s\'' %(ua)
    wget_opt_lang       = '--header=\'Accept-Language:zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7\''
    wget                = '%s %s' %(wget_opt_base, wget_opt_ua)
    expiration          = 14400

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

def debug_readLocal(url, local):
    global gDebugLog
    gDebugLog.append('%s -> %s' %(url, local))
    return readLocal(local)

def debug_saveLocal(url, local, txt):
    global gDebugLog
    gDebugLog.append('%s -> %s' %(url, local))
    saveLocal(local, txt)
    return txt

def showDebugLog(req, clear=True):
    global gDebugLog
    req.write('\n\n<!--DebugLog-->\n')
    for l in gDebugLog:
        req.write('<!-- %s -->\n' %(l))
    if clear:
        del gDebugLog[:]
    return

def checkExpire(local):
    if not os.path.exists(local):
        return True
    if os.path.getsize(local) <= 0:
        return True
    t0 = int(os.path.getmtime(local))
    t1 = int(time.time())
    if (t1 - t0) > defvals.expiration:
        return True
    return False

def genLocal(url, prefix=None, suffix=None):
    local = defvals.workdir+(prefix or 'vod_load_')+hashlib.md5(url).hexdigest()+(suffix or '')
    return local

def parse(url):
    p = urlparse.urlparse(url)
    prefix = p.scheme + '://' + p.netloc + os.path.dirname(p.path) + '/'
    basename = os.path.basename(p.path)
    return prefix, basename

def absURL(url, site=None):
    global domain
    site = site or domain
    if url.startswith('//'):
        return 'http:'+url
    if site and url.startswith('/'):
        return site+url
    if not url.startswith('http'):
        return 'http://'+url
    return url

def setDomain(url):
    global domain
    if url.startswith('http'):
        parsed_uri = urlparse.urlparse(url)
        domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
        return domain
    return None

def getContentType(url):
    res = urllib.urlopen(url)
    info = res.info()
    res.close()
    return info.type

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

def load(url, local=None, headers=None, cache=True):
    url = absURL(url)
    local = local or genLocal(url)
    if cache and not checkExpire(local):
        return debug_readLocal(url, local)

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', defvals.ua)]

    if headers:
        opener.addheaders += headers

    try:
        f = opener.open(url, None, 10) # timeout=10
        if f.info().get('Content-Encoding') == 'gzip':
            buf = StringIO(f.read())
            txt = gzip.GzipFile(fileobj=buf).read()
        else:
            txt = f.read()
        return debug_saveLocal(url, local, txt)
    except urllib2.HTTPError, e:
        return 'Exception HTTPError: ' + str(e.code)
    except urllib2.URLError, e:
        return 'Exception URLError: ' + str(e.reason)
    except:
        return 'Exception'

def post(url, payload, local=None, headers=None, cache=True):
    url = absURL(url)
    local = local or genLocal(url)
    if cache and not checkExpire(local):
        return debug_readLocal(url, local)

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', defvals.ua)]

    if headers:
        opener.addheaders += headers

    data = urllib.urlencode(payload)
    try:
        f = opener.open(url, data)
        txt = f.read()
        return debug_saveLocal(url, local, txt)
    except:
        return 'Exception'

def wget(url, local, options=None, cmd=None):
    print('[wget] %s -> %s' %(url, local))
    c = '%s %s' %(cmd or defvals.wget, options or '')
    cmd = '%s -O %s.part \'%s\'' %(c, local, url)
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        if re.search('Content-Encoding: gzip', output):
            cmd2 = 'mv %s %s.gz; gunzip %s.gz' %(local, local, local)
            subprocess.check_output(cmd2, shell=True)
        os.rename(local+'.part', local)
    except:
        print('Exception: '+cmd)
    return

def load2(url, local=None, options=None, cache=True, ref=None, cmd=None):
    url = absURL(url)
    local = local or genLocal(url)
    if cache and not checkExpire(local):
        return debug_readLocal(url, local)
    if ref:
        options = ' '.join([options or '', '--referer='+ref])
    wget(url, local, options, cmd=cmd)
    return debug_readLocal(url, local)

def curl(url, local=None, opts=[], cache=True):
    url = absURL(url)
    local = local or genLocal(url)
    if cache and not checkExpire(local):
        return debug_readLocal(url, local)
    cmd = 'curl -k -o %s.part %s \'%s\'' %(local, ' '.join(opts), url)
    try:
        subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        os.rename(local+'.part', local)
        return debug_readLocal(url, local)
    except:
        print('Exception: ' + cmd)
    return None

