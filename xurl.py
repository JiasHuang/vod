#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
import hashlib
import time
import subprocess
import StringIO
import gzip

try:
    # python 3
    from urllib.request import urlopen, build_opener
    from urllib.parse import urlparse, urlencode, quote, unquote, urljoin
    from urllib.error import HTTPError, URLError
except ImportError:
    # python 2
    from urlparse import urlparse, urljoin
    from urllib import urlopen, quote, unquote
    from urllib2 import build_opener, HTTPError, URLError

gDebugLog = []

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
    p = urlparse(url)
    prefix = p.scheme + '://' + p.netloc + os.path.dirname(p.path) + '/'
    basename = os.path.basename(p.path)
    return prefix, basename

def getContentType(url):
    res = urlopen(url)
    info = res.info()
    res.close()
    return info.type

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

def load(url, local=None, headers=None, cache=True):
    local = local or genLocal(url)
    if cache and not checkExpire(local):
        return debug_readLocal(url, local)

    opener = build_opener()
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
    local = local or genLocal(url)
    if cache and not checkExpire(local):
        return debug_readLocal(url, local)

    opener = build_opener()
    opener.addheaders = [('User-agent', defvals.ua)]

    if headers:
        opener.addheaders += headers

    data = urlencode(payload)
    try:
        f = opener.open(url, data)
        txt = f.read()
        return debug_saveLocal(url, local, txt)
    except:
        return 'Exception'

def wget(url, local=None, opts=[], cache=True, ref=None):
    local = local or genLocal(url)
    print('[wget] %s -> %s' %(url, local))
    if cache and not checkExpire(local):
        return debug_readLocal(url, local)
    if ref:
        opts.append('--referer=\'%s\'' %(ref))
    opts.append('-U \'%s\'' %(defvals.ua))
    cmd = 'wget -T 10 -S -O %s.part %s \'%s\'' %(local, ' '.join(opts), url)
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        if re.search('Content-Encoding: gzip', output):
            cmd2 = 'mv %s %s.gz; gunzip %s.gz' %(local, local, local)
            subprocess.check_output(cmd2, shell=True)
        os.rename(local+'.part', local)
        return debug_readLocal(url, local)
    except:
        print('Exception: '+cmd)
        return None

def curl(url, local=None, opts=[], cache=True, ref=None):
    local = local or genLocal(url)
    print('[curl] %s -> %s' %(url, local))
    if cache and not checkExpire(local):
        return debug_readLocal(url, local)
    if ref:
        opts.append('-e \'%s\'' %(ref))
    opts.append('-H \'User-Agent: %s\'' %(defvals.ua))
    opts.append('-H \'Accept-Encoding: gzip, deflate\'')
    opts.append('--compressed')
    cmd = 'curl -kLs -o %s.part %s \'%s\'' %(local, ' '.join(opts), url)
    try:
        subprocess.check_output(cmd, shell=True)
        os.rename(local+'.part', local)
        return debug_readLocal(url, local)
    except:
        print('Exception: ' + cmd)
        return None

