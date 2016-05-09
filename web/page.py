#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, os, sys, time
import requests, urllib2
import subprocess
import mangareader
import eslpod

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
    req.write('\n\n<!-- ENTRY: %s -->\n' %(title))
    if title != '':
        req.write('<h2><a href=view.py?url=%s>%s</a></h2>\n' %(link, title))
    if image == 'auto':
        image = getImage(req, link)
    req.write('<a href=view.py?url=%s><img src=%s class="img"/></a>\n' %(link, image))

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
        if p and t:
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

def loadWord(req, url):
    eslpod.loadWord(req, url)

def listURL_def(req, url):

    vid = ''
    txt = load(url)
    cnt = 0
    link = ''
    title = ''

    match = re.finditer(r'http://(www.dailymotion.com|videomega.tv|videowood.tv)/([^"]*)', txt)
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
        image = re.search(r'src="([^"]*)"', m.group(2))
        title = re.search(r'title="([^"]*)"', m.group(2))
        if image and title:
            addEntry(req, link, 'http://vlog.xuite.net'+image.group(1), title.group(1))

def listURL_DramaQIndex(req, zone):

    home = 'http://www.dramaq.biz/'
    url = home + zone + '/'
    txt = load2(url)

    match = re.finditer(r'<a title="([^"]*)" href="([^"]*)"><img src="([^"]*)"', txt)
    for m in match:
        link = home + m.group(2)
        title = m.group(1)
        image = home + m.group(3)
        addPage(req, link, title)

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

def listURL_moviesunIndex(req, url, zone):

    txt = load2(url)
    state = 0

    if zone == '':
        state = 100

    zone = '>%s<' %(zone)

    for line in txt.splitlines():

        if state != 100:
            m = re.search(r'<h4 class="widget-title">(.*?)</h4>', line)
            if m:
                if re.search(zone, m.group()):
                    state = 1
                elif state == 1:
                    break
                else:
                    state = 0
                continue

            m = re.search(r'<h3 class="widget-title section-title">(.*?)</h3>', line)
            if m:
                if re.search(zone, m.group()):
                    state = 1
                elif state == 1:
                    break
                else:
                    state = 0
                continue

        if state >= 1:
            m = re.search(r'<p class="cp-widget-title"><a href="([^"]*)" title="([^"]*)">', line)
            if m:
                link = m.group(1)
                title = m.group(2)
                addPage(req, link, title)


def listURL_moviesun(req, url):
    txt = load(url)
    match = re.finditer(r'<li><strong><a href="([^"]*)" rel="bookmark" title="([^"]*)">', txt)
    for m in match:
        link = m.group(1)
        title = m.group(2)
        addEntry(req, link, 'auto', title)

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
        image = re.search(r'src="([^"]*)"', m.group(2))
        title = re.search(r'alt="([^"]*)"', m.group(2))
        if image and title:
            addEntry(req, link, image.group(1), title.group(1))

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
        link = re.search(r'data-video-id="([^"]*)"', m.group())
        title = re.search(r'data-title="([^"]*)"', m.group())
        if link and title:
            addEntry(req, 'http://www.youtube.com/watch?v='+link.group(1), 'auto', title.group(1))

def listURL_mangareader(req, url):
    txt = load(url)
    match = re.finditer(r'<a href="/one-piece/([^"]*)">([^"]*)</a>([^<]*)<', txt)
    for m in match:
        link = 'http://www.mangareader.net/one-piece/'+m.group(1)
        title = m.group(2)+m.group(3)
        addPage(req, link, title)

def listURL_nbahd(req, url):
    txt = load(url)
    match = re.finditer(r'<h2 class="entry-title"><a href="([^"]*)"', txt)
    if match:
        req.write('<ul>')
        for m in match:
            url = m.group(1)
            req.write('<li class="li"><a href=%s%s>%s</a>' %('view.py?url=', url, url))
        req.write('</ul>')

def listURL_letv(req, url):
    txt = load(url)
    fd = open('/tmp/letv.txt', 'w')
    fd.write(txt)
    fd.close
    match = re.finditer(r'<dt class="hd_pic">.*?</dt>', txt, re.DOTALL)
    for m in match:
        link = re.search(r'href="([^"]*)"', m.group())
        image = re.search(r'src="([^"]*)"', m.group())
        title = re.search(r'alt="([^"]*)"', m.group())
        if link and image and title:
            addEntry(req, link.group(1), image.group(1), title.group(1))

def listURL(req, url):

    if url == 'mangareader':
        listURL_mangareader(req, 'http://www.mangareader.net/one-piece')
        return

    if url == 'nbahd':
        listURL_nbahd(req, 'http://nbahd.com/page/1/')
        listURL_nbahd(req, 'http://nbahd.com/page/2/')
        listURL_nbahd(req, 'http://nbahd.com/page/3/')
        return

    if url == 'dramaq-tw':
        return listURL_DramaQIndex(req, 'tw')

    if url == 'dramaq-kr':
        return listURL_DramaQIndex(req, '')

    if url == 'dramaq-jp':
        return listURL_DramaQIndex(req, 'jp')

    if url == 'dramaq-us':
        return listURL_DramaQIndex(req, 'us')

    if url == 'dramaq-cn':
        return listURL_DramaQIndex(req, 'cn')

    if url == 'moviesun-kr':
        return listURL_moviesunIndex(req, 'http://moviesunkd.com/', '韓劇列表')

    if url == 'moviesun-jp':
        return listURL_moviesunIndex(req, 'http://moviesuntw.com/', '日劇')

    if re.search(r'youtube.com', url):
        return listURL_youtube(req, url)

    if re.search(r'xuite.net', url):
        return listURL_xuite(req, url)

    if re.search(r'dramaq', url):
        return listURL_dramaq(req, url)

    if re.search(r'moviesun', url):
        return listURL_moviesun(req, url)

    if re.search(r'mangareader.net', url):
        return mangareader.loadImage(req, url)

    if re.search(r'movie.dodova.com/category/', url):
        listURL_dodova(req, url+'/page/1')
        listURL_dodova(req, url+'/page/2')
        listURL_dodova(req, url+'/page/3')
        listURL_dodova(req, url+'/page/4')
        listURL_dodova(req, url+'/page/5')
        return
 
    if re.search('jav(68|pub|cuteonline)',url):
        return listURL_jav(req, url)

    if re.search('letv.com', url):
        return listURL_letv(req, url)

    return listURL_def(req, url)
