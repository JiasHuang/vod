#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import requests
import urllib2
import json
import mangareader
import eslpod

class Entry:
    def __init__(self, link=None, title=None, image=None):
        self.link = link
        self.title = title
        self.image = image

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
    html = loadFile('list.html')
    txt = ''
    txt += '<h1>Index of %s</h1>' %(d)
    txt += '<div style="line-height:200%;font-size:20">'
    txt += '<ul>'
    for dirName, subdirList, fileList in os.walk(d):
        for subdir in sorted(subdirList):
            if subdir[0] != '.':
                txt += '<li><img src="/icons/folder.gif"> <a href="view.py?url=%s/%s">%s</a>' %(dirName, subdir, subdir)
        for fname in sorted(fileList):
            if fname.lower().endswith(('.mkv', '.mp4', '.avi', '.flv', '.rmvb', '.rm', '.f4v', '.wmv', '.m3u', '.m3u8')):
                txt += '<li><img src="/icons/movie.gif"> <a href="view.py?url=%s/%s">%s</a>' %(dirName, fname, fname)
        break
    txt += '</ul>'
    txt += '</div>'
    html = re.sub('<!--result-->', txt, html)
    req.write(html)

def load(url):
    headers={'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/33.0'}
    r = requests.get(url, headers=headers)
    return r.text.encode('utf8')

def load2(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/33.0')]
    return opener.open(url).read()

def getImage(link):
    m = re.search(r'www.youtube.com/watch\?v=(.{11})', link)
    if m:
        return 'http://img.youtube.com/vi/%s/0.jpg' %(m.group(1))
    m = re.search(r'http://www.dailymotion.com/video/(.*)', link)
    if m:
        txt = load('https://api.dailymotion.com/video/%s?fields=thumbnail_large_url' %(m.group(1)))
        data = json.loads(txt)
        if 'thumbnail_large_url' in data:
            return data['thumbnail_large_url'].encode('utf8')
    return None

def addEntry(req, link, title, image=None):
    req.write('<a href=%s>\n' %(link))
    req.write('<h2>%s</h2>\n' %(title))
    if image:
        req.write('<img src=%s class=img/>\n' %(image))
    req.write('</a>\n')

def addEntry_p(req, link, title):
    addEntry(req, 'view.py?p='+link, title, None)

def addEntry_v(req, link, title, image):
    addEntry(req, 'view.py?v='+link, title, image)

def addEntry_yt(req, vid, title):
    link = 'https://www.youtube.com/watch?v='+vid
    image = 'http://img.youtube.com/vi/'+vid+'/0.jpg'
    addEntry_v(req, link, title, image)

def addEntry_dm(req, vid, title):
    link = 'http://www.dailymotion.com/video/'+vid
    image = 'http://www.dailymotion.com/thumbnail/video/'+vid
    addEntry_v(req, link, title, image)

def search_yt(req, q):
    txt = load('https://www.youtube.com/results?filters=hd&search_query='+q)
    match = re.finditer(r'<a href="/watch\?v=(.{11})".*?>([^<]*)</a>', txt)
    for m in match:
        addEntry_yt(req, m.group(1), m.group(2))

def search_dm(req, q):
    txt = load('https://api.dailymotion.com/videos?search=%s&page=1' %(q))
    data = json.loads(txt)
    if 'list' in data:
        for d in data['list']:
            addEntry_dm(req, d['id'].encode('utf8'), d['title'].encode('utf8'))

def search_bi(req, q):
    txt = load('http://search.bilibili.com/video?keyword='+q+'&order=click')
    match = re.finditer(r'<a href="([^"]*)".*?</a>', txt, re.DOTALL)
    for m in match:
        link = m.group(1)
        image = re.search(r'src="([^"]*)"', m.group(0))
        title = re.search(r'title="([^"]*)"', m.group(0))
        if title and image:
            addEntry_v(req, link, title.group(1), image.group(1))

def search(req, q, s=None):
    html = re.split('<!--result-->', loadFile('list.html'))
    req.write(html[0])

    req.write('<h1><pre>')
    req.write('<a href=view.py>Home</a>     ')
    req.write('<a href=view.py?q=%s>YouTube</a>     ' %(q))
    req.write('<a href=view.py?q=%s&s=dm>DailyMotion</a>     ' %(q))
    req.write('<a href=view.py?q=%s&s=bi>Bilibili</a>     ' %(q))
    req.write('</pre></h1><hr>')

    q = re.sub(' ', '+', q)

    if s == None:
        search_yt(req, q)
    elif s == 'dm':
        search_dm(req, q)
    elif s == 'bi':
        search_bi(req, q)

    req.write(html[1])

def loadWord(req, url):
    html = re.split('<!--result-->', loadFile('list.html'))
    req.write(html[0])
    eslpod.loadWord(req, url)
    req.write(html[1])

def listURL_def(req, url):
    vid = ''
    txt = load(url)
    match = re.finditer(r'http://(www.dailymotion.com|videomega.tv|videowood.tv)/([^"]*)', txt)
    for m in match:
        if m.group() != vid:
            vid = m.group()
            addEntry_v(req, vid, vid, getImage(vid))
    match = re.finditer(r'http://www.youtube.com/embed/(.{11})', txt)
    for m in match:
        if m.group(1) != vid:
            vid = m.group(1)
            addEntry_yt(req, vid, vid)

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
            addEntry_v(req, link, title.group(1), 'http://vlog.xuite.net'+image.group(1))

def listURL_DramaQIndex(req, zone):
    home = 'http://www.dramaq.biz/'
    url = home + zone + '/'
    txt = load2(url)
    match = re.finditer(r'<a title="([^"]*)" href="([^"]*)"><img src="([^"]*)"', txt)
    for m in match:
        link = home + m.group(2)
        title = m.group(1)
        addEntry_p(req, link, title)

def listURL_dramaq(req, url):
    if re.search(r'php', url):
        return listURL_def(req, url)
    txt = load(url)
    match = re.finditer(r'<li class="item-751"><a href="([^.]*).php"', txt)
    for m in match:
        if re.search(r'ep', m.group(1)):
            link = url+m.group(1)+'.php'
            title = m.group(1)
            addEntry_p(req, link, title)

def listURL_dodova(req, url):
    txt = load(url)
    match = re.finditer(r'<div class="mh-excerpt">([^<]*)<a href="([^"]*)" title="([^"]*)">', txt)
    for m in match:
        link = m.group(2)
        title = m.group(3)
        addEntry_v(req, link, title, None)

def listURL_jav(req, url):
    txt = load(url)
    match = re.finditer(r'href="([^"]*)"[^<]*<img([^>]*)>', txt)
    for m in match:
        link = m.group(1)
        image = re.search(r'src="([^"]*)"', m.group(2))
        title = re.search(r'alt="([^"]*)"', m.group(2))
        if image and title:
            addEntry_v(req, link, title.group(1), image.group(1))

def listURL_youtube(req, url):
    vid = ''
    txt = load(url)
    match = re.finditer(r'watch\?v=(.{11})">([^<]*)</a>', txt)
    for m in match:
        if m.group(1) != vid:
            vid = m.group(1)
            title = m.group(2)
            addEntry_yt(req, vid, title)
    match = re.finditer(r'pl-video yt-uix-tile ([^>]*)', txt)
    for m in match:
        vid = re.search(r'data-video-id="([^"]*)"', m.group())
        title = re.search(r'data-title="([^"]*)"', m.group())
        if vid and title:
            addEntry_yt(req, vid.group(1), title.group(1))

def listURL_mangareader(req, url):
    txt = load(url)
    match = re.finditer(r'<a href="/one-piece/([^"]*)">([^"]*)</a>([^<]*)<', txt)
    for m in match:
        link = 'http://www.mangareader.net/one-piece/'+m.group(1)
        title = m.group(2)+m.group(3)
        addEntry_p(req, link, title)

def listURL_nbahd(req, url):
    txt = load(url)
    match = re.finditer(r'<h2 class="entry-title"><a href="([^"]*)"', txt)
    for m in match:
        addEntry_p(req, m.group(1), m.group(1))

def listURL(req, url):

    html = re.split('<!--result-->', loadFile('list.html'))
    req.write(html[0])

    if url == 'mangareader':
        listURL_mangareader(req, 'http://www.mangareader.net/one-piece')

    elif url == 'nbahd':
        listURL_nbahd(req, 'http://nbahd.com/page/1/')
        listURL_nbahd(req, 'http://nbahd.com/page/2/')
        listURL_nbahd(req, 'http://nbahd.com/page/3/')

    elif url == 'dramaq-tw':
        listURL_DramaQIndex(req, 'tw')

    elif url == 'dramaq-kr':
        listURL_DramaQIndex(req, '')

    elif url == 'dramaq-jp':
        listURL_DramaQIndex(req, 'jp')

    elif url == 'dramaq-us':
        listURL_DramaQIndex(req, 'us')

    elif url == 'dramaq-cn':
        listURL_DramaQIndex(req, 'cn')

    elif re.search(r'youtube.com', url):
        listURL_youtube(req, url)

    elif re.search(r'xuite.net', url):
        listURL_xuite(req, url)

    elif re.search(r'dramaq', url):
        listURL_dramaq(req, url)

    elif re.search(r'mangareader.net', url):
        mangareader.loadImage(req, url)

    elif re.search(r'movie.dodova.com/category/', url):
        listURL_dodova(req, url+'/page/1')
        listURL_dodova(req, url+'/page/2')
        listURL_dodova(req, url+'/page/3')
        listURL_dodova(req, url+'/page/4')
        listURL_dodova(req, url+'/page/5')

    elif re.search('jav(68|pub|cuteonline)',url):
        listURL_jav(req, url)

    else:
        listURL_def(req, url)

    req.write(html[1])

