#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import requests
import urllib
import threading
import xdef

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

def dlProgress(count, blockSize, totalSize):
    percent = int(count*blockSize*100/totalSize)
    if (0 <= percent < 100):
        sys.stdout.write("\r%2d%%" % percent)
        sys.stdout.flush()
    if (percent >= 100):
        sys.stdout.write("\r")
        sys.stdout.flush()

def savetext(text, local):
    fd = open(local, 'w')
    fd.write(text)
    fd.close()
    return 0

def verbose(url, local, agent):
    print('[xurl] %s' %(color.GREEN+url+color.END))
    print('[xurl] %s ==> %s' %(agent, local))
    return 0

def wget(url, local):
    if os.path.exists(local):
        print('[xurl] %s already exist' %(local))
        return 0
    verbose(url, local, 'wget')
    cmd = '%s -U \'%s\' -O %s \'%s\' ' %(xdef.wget, xdef.ua, local, url)
    os.system(cmd.encode('utf8'))
    print('[xurl] %s Done' %(local))
    return 0

def get(url, local):
    verbose(url, local, 'get')
    r = requests.get(url)
    savetext(r.text.encode('utf8'), local)
    print('[xurl] %s Done' %(local))
    return 0

def urlretrieve(url, local):
    verbose(url, local, 'urlretrieve')
    try:
        #urllib.urlretrieve (url, local, dlProgress)
        urllib.urlretrieve (url, local)
        print('[xurl] %s Done' %(local))
    except:
        print("[xurl] %s Fail" %(local))
    return 0

def load(url, payload=None):

    headers={'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/33.0'}

    if payload:
        r = requests.post(url, data=payload)
    else:
        r = requests.get(url, headers=headers)

    return r.text.encode('utf8')

