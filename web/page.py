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
    f = open(os.path.dirname(os.path.abspath(__file__))+'/'+filename, 'r')
    return f.read()

def render(req, filename, result):
    html = loadFile(filename+'.html')
    if result:
        txt = ''
        for obj in result:
            if obj.link and obj.title:
                txt += '<h2><a href=%s>%s</a></h2>\n' %(obj.link, obj.title)
            if obj.link and obj.image:
                txt += '<a href=%s><img src=%s class="img"/></a>\n' %(obj.link, obj.image)
        html = re.sub('<!--result-->', txt, html)
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

def image_yt(vid):
    return 'http://img.youtube.com/vi/'+vid+'/0.jpg'

def getImage(link):
    m = re.search(r'www.youtube.com/watch\?v=(.{11})', link)
    if m:
        return 'http://img.youtube.com/vi/%s/0.jpg' %(m.group(1))
    m = re.search(r'http://www.dailymotion.com/video/(.*)', link)
    if m:
        txt = load('https://api.dailymotion.com/video/%s?fields=thumbnail_large_url' %(m.group(1)))
        data = json.loads(txt)
        return data['thumbnail_large_url'].encode('utf8')
    return None

def entry_yt(vid, title):
    link = 'view.py?url=https://www.youtube.com/watch?v='+vid
    image = 'http://img.youtube.com/vi/'+vid+'/0.jpg'
    return Entry(link, title, image)

def entry_dm(vid, title):
    link = 'view.py?url=http://www.dailymotion.com/video/'+vid
    txt = load('https://api.dailymotion.com/video/%s?fields=thumbnail_large_url' %(vid))
    data = json.loads(txt)
    return Entry(link, title, data['thumbnail_large_url'].encode('utf8'))

def entry_p(link, title):
    return Entry('view.py?p='+link, title, None)

def entry_v(link, title, image):
    return Entry('view.py?url='+link, title, image)

def search_yt(q):
    result = []
    txt = load('https://www.youtube.com/results?filters=hd&search_query='+q)
    match = re.finditer(r'<a href="/watch\?v=(.{11})".*?>([^<]*)</a>', txt)
    for m in match:
        result.append(entry_yt(m.group(1), m.group(2)))
    return result

def search_dm(q):
    result = []
    txt = load('http://www.dailymotion.com/tw/relevance/universal/search/%s/1' %(q))
    match = re.finditer(r'href="/video/([^"]*)".*?>([^<]*)</a>', txt)
    for m in match:
        result.append(entry_dm(m.group(1), m.group(2)))
    return result

def search(q):
    q = re.sub(' ', '+', q)
    result = []
    result.extend(search_yt(q))
    result.extend(search_dm(q))
    return result

def loadWord(req, url):
    eslpod.loadWord(req, url)

def listURL_def(req, url):
    result = []
    vid = ''
    txt = load(url)
    match = re.finditer(r'http://(www.dailymotion.com|videomega.tv|videowood.tv)/([^"]*)', txt)
    for m in match:
        if m.group() != vid:
            vid = m.group()
            result.append(entry_v(vid, vid, getImage(vid)))
    match = re.finditer(r'http://www.youtube.com/embed/(.{11})', txt)
    for m in match:
        if m.group(1) != vid:
            vid = m.group(1)
            result.append(entry_yt(vid, vid))
    return result

def listURL_xuite(req, url):
    # http://vlog.xuite.net/isaac.ntnu*1
    # http://m.xuite.net/vlog/isaac.ntnu/
    result = []
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
            result.append(entry_v(link, title.group(1), 'http://vlog.xuite.net'+image.group(1)))
    return result

def listURL_DramaQIndex(req, zone):
    result = []
    home = 'http://www.dramaq.biz/'
    url = home + zone + '/'
    txt = load2(url)
    match = re.finditer(r'<a title="([^"]*)" href="([^"]*)"><img src="([^"]*)"', txt)
    for m in match:
        link = home + m.group(2)
        title = m.group(1)
        image = home + m.group(3)
        result.append(entry_p(link, title))
    return result

def listURL_dramaq(req, url):
    if re.search(r'php', url):
        return listURL_def(req, url)
    result = []
    txt = load(url)
    match = re.finditer(r'<li class="item-751"><a href="([^.]*).php"', txt)
    for m in match:
        if re.search(r'ep', m.group(1)):
            link = url+m.group(1)+'.php'
            title = m.group(1)
            result.append(entry_p(link, title))
    return result

def listURL_dodova(req, url):
    result = []
    txt = load(url)
    match = re.finditer(r'<div class="mh-excerpt">([^<]*)<a href="([^"]*)" title="([^"]*)">', txt)
    for m in match:
        link = m.group(2)
        title = m.group(3)
        result.append(entry_v(link, title, None))
    return result

def listURL_jav(req, url):
    result = []
    txt = load(url)
    match = re.finditer(r'href="([^"]*)"[^<]*<img([^>]*)>', txt)
    for m in match:
        link = m.group(1)
        image = re.search(r'src="([^"]*)"', m.group(2))
        title = re.search(r'alt="([^"]*)"', m.group(2))
        if image and title:
            result.append(entry_v(link, title.group(1), image.group(1)))
    return result

def listURL_youtube(req, url):
    result = []
    vid = ''
    txt = load(url)
    match = re.finditer(r'watch\?v=(.{11})">([^<]*)</a>', txt)
    for m in match:
        if m.group(1) != vid:
            vid = m.group(1)
            title = m.group(2)
            result.append(entry_yt(vid, title))
    match = re.finditer(r'pl-video yt-uix-tile ([^>]*)', txt)
    for m in match:
        vid = re.search(r'data-video-id="([^"]*)"', m.group())
        title = re.search(r'data-title="([^"]*)"', m.group())
        if vid and title:
            result.append(entry_yt(vid.group(1), title.group(1)))
    return result

def listURL_mangareader(req, url):
    result = []
    txt = load(url)
    match = re.finditer(r'<a href="/one-piece/([^"]*)">([^"]*)</a>([^<]*)<', txt)
    for m in match:
        link = 'http://www.mangareader.net/one-piece/'+m.group(1)
        title = m.group(2)+m.group(3)
        result.append(entry_p(link, title))
    return result

def listURL_nbahd(req, url):
    result = []
    txt = load(url)
    match = re.finditer(r'<h2 class="entry-title"><a href="([^"]*)"', txt)
    for m in match:
        result.append(entry_p(m.group(1), m.group(1)))
    return result

def listURL(req, url):

    result = []

    if url == 'mangareader':
        result.extend(listURL_mangareader(req, 'http://www.mangareader.net/one-piece'))

    elif url == 'nbahd':
        result.extend(listURL_nbahd(req, 'http://nbahd.com/page/1/'))
        result.extend(listURL_nbahd(req, 'http://nbahd.com/page/2/'))
        result.extend(listURL_nbahd(req, 'http://nbahd.com/page/3/'))

    elif url == 'dramaq-tw':
        result.extend(listURL_DramaQIndex(req, 'tw'))

    elif url == 'dramaq-kr':
        result.extend(listURL_DramaQIndex(req, ''))

    elif url == 'dramaq-jp':
        result.extend(listURL_DramaQIndex(req, 'jp'))

    elif url == 'dramaq-us':
        result.extend(listURL_DramaQIndex(req, 'us'))

    elif url == 'dramaq-cn':
        result.extend(listURL_DramaQIndex(req, 'cn'))

    elif re.search(r'youtube.com', url):
        result.extend(listURL_youtube(req, url))

    elif re.search(r'xuite.net', url):
        result.extend(listURL_xuite(req, url))

    elif re.search(r'dramaq', url):
        result.extend(listURL_dramaq(req, url))

    elif re.search(r'moviesun', url):
        result.extend(listURL_moviesun(req, url))

    elif re.search(r'mangareader.net', url):
        return mangareader.loadImage(req, url)

    elif re.search(r'movie.dodova.com/category/', url):
        result.extend(listURL_dodova(req, url+'/page/1'))
        result.extend(listURL_dodova(req, url+'/page/2'))
        result.extend(listURL_dodova(req, url+'/page/3'))
        result.extend(listURL_dodova(req, url+'/page/4'))
        result.extend(listURL_dodova(req, url+'/page/5'))

    elif re.search('jav(68|pub|cuteonline)',url):
        result.extend(listURL_jav(req, url))

    else:
        result.extend(listURL_def(req, url))

    render(req, 'list', result)

