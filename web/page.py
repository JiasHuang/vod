#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, os, sys, time
import requests, urllib2
import subprocess

def load(url):
    headers={'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/33.0'}
    r = requests.get(url, headers=headers)
    return r.text.encode('utf8')

def load2(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/33.0')]
    return opener.open(url).read()

def getImage(req, link):
    if re.search(r'www.youtube.com/', link):
        m = re.search(r'watch\?v=(.{11})', link)
        return 'http://img.youtube.com/vi/%s/0.jpg' %(m.group(1))
    if re.search(r'http://www.dailymotion.com/', link):
        m = re.search(r'video/(.*)', link)
        return 'http://www.dailymotion.com/thumbnail/video/%s' %(m.group(1))
    return 'cat-walk-icon.png'

def addEntry(req, link, image, title):
    if title != '':
        req.write('<h2>')
        req.write('<a href=view.py?url=%s>%s</a>' %(link, title))
        req.write('</h2>')
    if image == 'auto':
        image = getImage(req, link)
    req.write('<a href=view.py?url=%s><img src=%s class="img"/></a>' %(link, image))

def addPage(req, link, title):
    if title != '':
        req.write('<h2>')
        req.write('<a href=view.py?p=%s>%s</a>' %(link, title))
        req.write('</h2>')

def search_bing(req, q):
    url = 'https://www.bing.com/videos/search?q=%s&qft=+filterui:duration-long+filterui:resolution-720p' %(q)
    txt = load(url)
    txt = re.sub('&quot;', '', txt)
    match = re.finditer(r'vrhm="{([^}]*)}"', txt)
    for m in match:
        p = re.search(r'p:([^,]*)', m.group())
        t = re.search(r't:([^,]*)', m.group())
        addEntry(req, p.group(1), 'auto', 'Bing: '+t.group(1))


def search_yandex(req, q):
    url = 'http://www.yandex.com/video/search?&text=%s&duration=long' %(q)
    txt = load(url)
    txt = re.sub('<b>', '', txt)
    txt = re.sub('</b>', '', txt)
    match = re.finditer(r'href="([^"]*)" target="_blank">([^<]*)</a></h2>', txt)
    for m in match:
        addEntry(req, m.group(1), 'auto', 'Yandex: '+m.group(2))


def search_google(req, q, site, arg):
    if site != '':
        q = 'site:%s+%s' %(site, q)
    if arg == 'vid':
        url = 'https://www.google.com.tw/search?tbm=vid&q=%s' %(q)
    else:
        url = 'https://www.google.com.tw/search?q=%s&safe=off&filter=0&num=10' %(q)

    txt = load(url)
    match = re.finditer(r'href="([^"]*)" [^>]*>([^<]*)</a></h3>', txt)
    for m in match:
        addEntry(req, m.group(1), 'auto', 'Google: '+m.group(2))

    # Its suck !! Google will block robot requests
    time.sleep(2)

def search_youtube(req, q):
    url = 'https://www.youtube.com/results?filters=hd&search_query=%s' %(q)
    txt = load(url)
    match = re.finditer(r'<a href="/watch\?v=(.{11})".*?>([^<]*)</a>', txt)
    for m in match:
        addEntry(req, 'https://www.youtube.com/watch?v='+m.group(1), 'auto', 'YouTube: '+m.group(2))

def search_dailymotion(req, q):
    url = 'http://www.dailymotion.com/tw/relevance/universal/search/%s/1' %(q)
    txt = load(url)
    match = re.finditer(r'href="/video/([^"]*)".*?>([^<]*)</a>', txt)
    for m in match:
        addEntry(req, 'http://www.dailymotion.com/video/'+m.group(1), 'auto', 'Dailymotion: '+m.group(2))

def search(req, q):
    q = re.sub(' ', '+', q)
    search_youtube(req, q)

def listURL_def(req, url):

    vid = ''
    txt = load(url)
    cnt = 0
    link = ''
    title = ''

    match = re.finditer(r'http://(www.dailymotion.com|videomega.tv)/([^"]*)', txt)
    for m in match:
        if m.group() != vid:
            if cnt == 1:
                addEntry(req, link, 'auto', title)
            vid = m.group()
            link = m.group()
            title = m.group()
            if cnt > 0:
                addEntry(req, link, 'auto', title)
            cnt = cnt + 1

    match = re.finditer(r'http://www.youtube.com/embed/(.{11})', txt)
    for m in match:
        if m.group(1) != vid:
            if cnt == 1:
                addEntry(req, link, 'auto', title)
            vid = m.group(1)
            link = 'http://www.youtube.com/watch?v=%s' %(vid)
            if cnt > 0:
                addEntry(req, link, 'auto', 'Youtube: '+vid)
            cnt = cnt + 1

    if cnt == 1:
        return link

    return ''

def listURL_xuite(req, url):

    # http://vlog.xuite.net/isaac.ntnu*1 
    # http://m.xuite.net/vlog/isaac.ntnu/

    txt = load(url)
    hdr = re.sub('vlog.xuite.net/', 'm.xuite.net/vlog/', url)
    hdr = re.sub('\*.', '/', hdr)
    match = re.finditer(r'href="/play/([^"]*)"[^<]*<img([^>]*)>', txt)
    for m in match:
        vid = m.group(1)
        link = hdr+vid
        image = 'http://vlog.xuite.net'+re.search(r'src="([^"]*)"', m.group(2)).group(1)
        title = re.search(r'title="([^"]*)"', m.group(2)).group(1)
        addEntry(req, link, image, title)

def listURL_DramaQIndex(req, zone):

    url = 'http://www.dramaq.com.tw'
    txt = load2(url)
    state = 0

    if zone == '':
        state = 100

    for line in txt:

        if state != 100:
            m = re.search(r'<h3>《([^》]*)》</h3>', line)
            if m:
                if m.group(1) == zone:
                    state = 1
                elif state == 1:
                    break
                else:
                    state = 0
                continue

        if state >= 1:
            m = re.search(r'<a title="([^"]*)" href="([^"]*)"><img src="([^"]*)"', line)
            if m:
                link = 'http://www.dramaq.com.tw'+m.group(2)
                title = m.group(1)
                image = 'http://www.dramaq.com.tw'+m.group(3)
                addPage(req, link, title)

    txt.close()


def listURL_dramaq(req, url):
    if re.search(r'php', url):
        return listURL_def(req, url)

    txt = load(url)
    match = re.finditer(r'<li class="item-751"><a href="([^.]*).php"', txt)
    for m in match:
        if re.search(r'ep', m.group(1)):
            link = url+m.group(1)+'.php'
            title = m.group(1)
            addPage(req, link, title)

def listURL_dodova(req, url):
    txt = load(url)
    match = re.finditer(r'<div class="mh-excerpt">([^<]*)<a href="([^"]*)" title="([^"]*)">', txt)
    for m in match:
        link = m.group(2)
        title = m.group(3)
        addPage(req, link, title)

def listURL_jav(req, url):
    txt = load(url)
    match = re.finditer(r'href="([^"]*)"[^<]*<img([^>]*)>', txt)
    for m in match:
        link = m.group(1)
        image = re.search(r'src="([^"]*)"', m.group(2)).group(1)
        title = re.search(r'alt="([^"]*)"', m.group(2)).group(1)
        addEntry(req, link, image, title)

def listURL_youtube(req, url):
    vid = ''
    txt = load(url)
    match = re.finditer(r'watch\?v=(.{11})">([^<]*)</a>', txt)
    for m in match:
        if m.group(1) != vid:
            vid = m.group(1)
            link = 'http://www.youtube.com/watch?v=%s' %(vid)
            title = m.group(2)
            addEntry(req, link, 'auto', title)

    match = re.finditer(r'pl-video yt-uix-tile ([^>]*)', txt)
    for m in match:
        link = 'http://www.youtube.com/watch?v='
        link += re.search(r'data-video-id="([^"]*)"', m.group()).group(1)
        title = re.search(r'data-title="([^"]*)"', m.group()).group(1)
        addEntry(req, link, 'auto', title)

def listURL_nbahd(req, url):
    txt = load(url)
    match = re.finditer(r'<h2 class="entry-title"><a href="([^"]*)"', txt)
    if match:
        req.write('<ul>')
        for m in match:
            url = m.group(1)
            req.write('<li class="li"><a href=%s%s>%s</a>' %('view.py?url=', url, url))
        req.write('</ul>')

def listURL(req, url, key):

    if url == 'nbahd':
        listURL_nbahd(req, 'http://nbahd.com/watch/nba-full-game/page/1/')
        listURL_nbahd(req, 'http://nbahd.com/watch/nba-full-game/page/2/')
        listURL_nbahd(req, 'http://nbahd.com/watch/nba-full-game/page/3/')
        return

    if url == 'dramaq-tw':
        return listURL_DramaQIndex(req, '台劇')

    if url == 'dramaq-kr':
        return listURL_DramaQIndex(req, '韓劇')

    if url == 'dramaq-jp':
        return listURL_DramaQIndex(req, '日劇')

    if url == 'dramaq-us':
        return listURL_DramaQIndex(req, '美劇')

    if url == 'dramaq-cn':
        return listURL_DramaQIndex(req, '陸劇')

    if re.search(r'youtube.com', url):
        return listURL_youtube(req, url)

    if re.search(r'xuite.net', url):
        return listURL_xuite(req, url, key)

    if re.search(r'dramaq.com', url):
        return listURL_dramaq(req, url)

    if re.search(r'movie.dodova.com/category/', url):
        listURL_dodova(req, url+'/page/1')
        listURL_dodova(req, url+'/page/2')
        listURL_dodova(req, url+'/page/3')
        listURL_dodova(req, url+'/page/4')
        listURL_dodova(req, url+'/page/5')
        return
 
    if re.search('jav(68|pub|cuteonline)',url):
        return listURL_jav(req, url)

    return listURL_def(req, url)
