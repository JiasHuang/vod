#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import time
import json
import sys

path = os.path.realpath(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(path))

import extractors
import xurl
import conf

def loadFile(filename):
    path = os.path.dirname(os.path.abspath(__file__))+'/'+filename
    with open(path, 'r') as fd:
        return fd.read()
    return None

def render(req, filename, result):
    html = loadFile(filename+'.html')
    if result:
        html = re.sub('<!--result-->', result, html)
    req.write(html)

def renderDIR(req, d):
    html = re.split('<!--result-->', loadFile('list.html'))
    req.write(html[0])
    req.write('<h1>Index of %s</h1>\n' %(d))
    req.write('<div style="line-height:200%;font-size:32px">\n')
    for dirName, subdirList, fileList in os.walk(d):
        for subdir in sorted(subdirList):
            if subdir[0] != '.':
                req.write('<li><img src="/icons/folder.gif"> <a href="view.py?d=%s/%s">%s</a>\n' \
                    %(dirName, subdir, subdir))
        for fname in sorted(fileList):
            suffix = ('.mkv', '.mp4', '.avi', '.flv', '.rmvb', '.rm', '.f4v', '.wmv', '.m3u', '.m3u8', '.ts')
            if fname.lower().endswith(suffix):
                req.write('<li><img src="/icons/movie.gif"> <a href="view.py?f=%s/%s">%s</a>\n' \
                    %(dirName, fname, fname))
        break
    req.write('</div>\n')
    req.write(html[1])

def addEntry(req, link, title, image=None, desc=None, password=None, video=True, referer=None):
    if video:
        if not image:
            image = 'Movies-icon.png'
        if password:
            password = '&__password__='+password
        if referer:
            referer = '&__referer__='+referer
        source = '%s%s%s' %(link, password or '', referer or '')
        anchor = 'href="view.py?v=%s" target="playVideo"' %(source)
    else:
        anchor = 'href="view.py?p=%s" onclick="onPageClick.call(this);" title="%s"' %(link, title)
    if image:
        req.write('\n<div class="imageWrapper">\n')
        req.write('<div class="imageContainer">\n')
        req.write('<a %s><img src="%s" onerror=\'this.onerror=null; this.src="Movies-icon.png"\' /></a>\n' %(anchor, image))
        if desc:
            req.write('<p>%s</p>\n' %(desc))
        req.write('</div>\n')
        req.write('<h2><a %s>%s</a></h2>\n' %(anchor, title))
        req.write('</div>\n')
    else:
        req.write('\n<h2 class="entryTitle"><a %s>%s</a></h2>\n' %(anchor, title))

def addNextPage(req, q, s, label, link):
    m = re.search(r'(prev|next)', label.lower())
    label = m.group(1) if m else label
    link = link or ''
    x = None
    if re.search(r'youtube\.com', link):
        m = re.search(r'sp=([a-zA-Z0-9%]*)', link)
        x = m.group(1) if m else None
    elif re.search(r'google\.com', link):
        m = re.search(r'start=(\d+)', link)
        x = m.group(1) if m else None
    req.write('<div id="div_page_%s" title="%s" s="%s" q="%s" x="%s"></div>\n' %(label, label.title(), s, q, x or ''))
    return

def addResults(req, results, q=None, s=None):
    local = '/var/tmp/vod_list_pagelist_%s' %(str(os.getpid() % 100))
    fd = open(local, 'w')
    for obj in results:
        if isinstance(obj, extractors.entryObj):
            addEntry(req, obj.link, obj.title, obj.image, obj.desc, video=obj.video)
            fd.write(obj.link+'\n')
        elif isinstance(obj, extractors.navObj):
            addNextPage(req, q, s, obj.label, obj.link)
    fd.close()
    req.write('<meta id="pagelist" pagelist="%s">\n' %(local))
    return

def search_core(req, q, s=None, x=None):
    s = (s or 'youtube').lower()
    q1 = re.sub(' ', '+', q)
    results = extractors.search(q1, s, x)
    if results:
        addResults(req, results, q, s)
    else:
        onPageNotFound(req)

def search(req, q, s=None, x=None):
    logfile = xurl.genLocal('q=%s&s=%s&x=%s' %(q, s or '', x or ''), suffix='.log')
    req.write('\n\n<!-- logfile: %s -->\n\n' %(logfile))
    sys.stdout = open(logfile, 'w')
    search_core(req, q, s, x)
    sys.stdout.close()

def onPageNotFound(req):
    req.write('<h1><span class="message" id="NotFound"></span></h1>\n')

def page_core(req, url):
    results = extractors.extract(url)
    if results:
        addResults(req, results)
    else:
        onPageNotFound(req)

def page(req, url):
    logfile = xurl.genLocal(url, suffix='.log')
    html = re.split('<!--result-->', loadFile('list.html'))
    req.write(html[0])
    req.write('\n\n<!-- logfile: %s -->\n\n' %(logfile))
    sys.stdout = open(logfile, 'w')
    page_core(req, url)
    sys.stdout.close()
    req.write(html[1])

