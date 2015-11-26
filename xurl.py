#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import requests
import urllib
import threading
import xdef

from selenium import webdriver

from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
from PyQt4.QtWebKit import *  

engine = 'PhantomJS'

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

class Render(QWebPage):  
  def __init__(self, url):  
    self.app = QApplication(sys.argv)  
    QWebPage.__init__(self)  
    self.loadFinished.connect(self._loadFinished)  
    self.mainFrame().load(QUrl(url))  
    self.app.exec_()  
  
  def _loadFinished(self, result):  
    self.frame = self.mainFrame()  
    self.app.quit()  
  
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
    print '[xurl] %s' %(color.GREEN+url+color.END)
    print '[xurl] %s ==> %s' %(agent, local)
    return 0

def wget(url, local):
    verbose(url, local, 'wget')
    cmd = '%s -U \'%s\' -O %s \'%s\' ' %(xdef.wget, xdef.ua, local, url)
    os.system(cmd.encode('utf8'))
    print '[xurl] %s Done' %(local)
    return 0

def get(url, local):
    verbose(url, local, 'get')
    r = requests.get(url)
    savetext(r.text.encode('utf8'), local)
    print '[xurl] %s Done' %(local)
    return 0

def webkit(url, local):
    verbose(url, local, 'webkit')
    r = Render(url)
    html = r.frame.toHtml()
    savetext(html.toUtf8(), local)
    print '[xurl] %s Done' %(local)
    return 0

def webdrv(url, local):
    verbose(url, local, 'webdrv')
    if engine == 'Firefox':
        driver = webdriver.Firefox()
    if engine == 'PhantomJS':
        driver = webdriver.PhantomJS()
    driver.get(url)
    savetext(driver.page_source.encode('utf8'), local)
    driver.close()
    print '[xurl] %s Done' %(local)
    return 0

def urlretrieve(url, local):
    verbose(url, local, 'urlretrieve')
    try:
        #urllib.urlretrieve (url, local, dlProgress)
        urllib.urlretrieve (url, local)
        print '[xurl] %s Done' %(local)
    except:
        print "[xurl] %s Fail" %(local)
    return 0

def load(*arg):

    url = None
    payload = None

    if len(arg) >= 1:
        url = arg[0]
    if len(arg) >= 2:
        payload = arg[1]

    headers={'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/33.0'}

    if payload: 
        r = requests.post(url, data=payload)
    else:
        r = requests.get(url, headers=headers)

    return r.text.encode('utf8')

