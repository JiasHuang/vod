#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import requests
import urllib
import re
import xdef
import base64

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def savetext(text, local):
    fd = open(local, 'w')
    fd.write(text)
    fd.close()
    return 0

def verbose(url, local, agent):
    print('\n[xurl][%s]\n' %(agent))
    print('\tsrc: %s' %(color.GREEN+url+color.END))
    print('\tdst: %s' %(local))
    return 0

def verbose_status(status):
    print('\tret: %s' %(status))
    return 0

def readLocal(local):
    with open(local, 'r') as fd:
        return fd.read()
    return ''

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
    verbose(url, local, 'get')
    r = requests.get(url)
    savetext(r.text.encode('utf8'), local)
    verbose_status('done')
    return 0

def urlretrieve(url, local):
    verbose(url, local, 'urlretrieve')
    try:
        urllib.urlretrieve (url, local)
        verbose_status('done')
    except:
        verbose_status('fail')
    return 0

def load(url, payload=None):

    headers={'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/33.0'}

    if payload:
        r = requests.post(url, data=payload)
    else:
        r = requests.get(url, headers=headers)

    return r.text.encode('utf8')

def load2(url, local=None):
    url = absURL(url)
    if not local:
        local = xdef.workdir+'load_'+base64.urlsafe_b64encode(url)
    wget(url, local)
    return readLocal(local)

