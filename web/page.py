#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import urllib
import json
import mangareader
import eslpod
import meta

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
    html = re.split('<!--result-->', loadFile('list.html'))
    req.write(html[0])
    req.write('<h1>Index of %s</h1>' %(d))
    req.write('<div style="line-height:200%;font-size:20">')
    for dirName, subdirList, fileList in os.walk(d):
        for subdir in sorted(subdirList):
            if subdir[0] != '.':
                req.write('<li><img src="/icons/folder.gif"> <a href="view.py?d=%s/%s">%s</a>' %(dirName, subdir, subdir))
        for fname in sorted(fileList):
            if fname.lower().endswith(('.mkv', '.mp4', '.avi', '.flv', '.rmvb', '.rm', '.f4v', '.wmv', '.m3u', '.m3u8')):
                req.write('<li><img src="/icons/movie.gif"> <a href="view.py?f=%s/%s">%s</a>' %(dirName, fname, fname))
        break
    req.write('</div>')
    req.write(html[1])

def load(url):
    return meta.load(url)

def addEntry(req, link, title, image=None):
    req.write('<a href=%s>\n' %(link))
    req.write('<h2>%s</h2>\n' %(title))
    if image:
        req.write('<img src=%s class=img />\n' %(image))
    req.write('</a>\n')

def addPage(req, link, title, image=None):
    if re.search(r'&', link):
        addEntry(req, 'view.py?P='+urllib.quote(link), title, image)
    else:
        addEntry(req, 'view.py?p='+link, title, image)

def addVideo(req, link, title=None, image=None):
    if re.search(r'^//', link):
        link = re.sub('//', 'http://', link)
    addEntry(req, 'view.py?v='+link, title or link, image or meta.getImage(link))

def addYouTube(req, vid, title):
    link = 'https://www.youtube.com/watch?v='+vid
    image = 'http://img.youtube.com/vi/'+vid+'/0.jpg'
    addVideo(req, link, title, image)

def addPlayList(req, playlist, title, video=None):
    link = 'https://www.youtube.com/playlist?list='+playlist
    image = None
    if video:
        image = 'http://img.youtube.com/vi/'+video+'/0.jpg'
    addPage(req, link, title, image)

def addDailyMotion(req, vid, title):
    link = 'http://www.dailymotion.com/video/'+vid
    image = 'http://www.dailymotion.com/thumbnail/video/'+vid
    addVideo(req, link, title, image)

def search_yt(req, q):
    url = 'https://www.youtube.com/results?sp=CAISAiAB&q='+q
    for m in re.finditer(r'<a href="/watch\?v=(.{11})".*?>([^<]*)</a>', load(url)):
        addYouTube(req, m.group(1), m.group(2))

def search_pl(req, q):
    url = 'https://www.youtube.com/results?sp=EgIQAw%3D%3D&q='+q
    playlist = None
    for m in re.finditer(r'href="/watch\?v=(.{11})&amp;list=([^"]*)".*?>([^<]*)</a>', load(url)):
        if playlist != m.group(2):
            video, playlist, title = m.group(1), m.group(2), m.group(3)
            addPlayList(req, playlist, title, video)

def search_fx(req, q):
    url = 'https://www.youtube.com/results?sp=EgQYAiAB&q='+q
    for m in re.finditer(r'<a href="/watch\?v=(.{11})".*?>([^<]*)</a>', load(url)):
        addYouTube(req, m.group(1), m.group(2))

def search_dm(req, q):
    data = json.loads(load('https://api.dailymotion.com/videos?search=%s&page=1' %(q)))
    if 'list' in data:
        for d in data['list']:
            vid = d['id'].encode('utf8')
            title = d['title'].encode('utf8')
            addDailyMotion(req, vid, title)

def search_bi(req, q):
    url = 'http://search.bilibili.com/video?keyword=%s&order=click' %(urllib.quote(q))
    meta.findPage(req, url, True)

def search(req, q, s):
    html = re.split('<!--result-->', loadFile('list.html'))
    req.write(html[0])

    s = s or 'yt'

    q1 = re.sub(' ', '+', q)

    req.write('<h1><pre>')
    req.write('<a href=view.py>Home</a>    ')
    req.write('<a href=view.py?s=yt&q='+q+'>YouTube</a>    ')
    req.write('<a href=view.py?s=pl&q='+q+'>PlayList</a>    ')
    req.write('<a href=view.py?s=fx&q='+q+'>Filter</a>    ')
    req.write('<a href=view.py?s=dm&q='+q+'>DailyMotion</a>    ')
    req.write('<a href=view.py?s=bi&q='+q+'>Bilibili</a>    ')
    req.write('</pre></h1>')

    req.write('<br>')

    req.write('<form action="view.py" method="get">')
    req.write('<input type="text" name="q" value="%s" class="input"\>' %(q))
    req.write('<input type="hidden" name="s" value="%s" class="input"\>' %(s))
    req.write('</form>')

    req.write('<br>')

    if s == 'yt':
        search_yt(req, q1)
    elif s == 'pl':
        search_pl(req, q1)
    elif s == 'fx':
        search_fx(req, q1)
    elif s == 'dm':
        search_dm(req, q1)
    elif s == 'bi':
        search_bi(req, q1)

    req.write(html[1])

def loadWord(req, url):
    html = re.split('<!--result-->', loadFile('list.html'))
    req.write(html[0])
    eslpod.loadWord(req, url)
    req.write(html[1])

def listURL_def(req, url):
    meta.findLink(req, url)

def listURL_xuite(req, url):
    meta.findVideo(req, url)

def listURL_xuiteDIR(req, url):

    m = re.search(r'xuite.net/([a-z0-9A-Z]*)($)', url)
    if not m:
        return

    user = m.group(1)

    m = re.search(r'userSn=([0-9]*)', load(url))
    if not m:
        return

    userSn = m.group(1)

    data = json.loads(load('http://vlog.xuite.net/default/media/widget?title=dir&userSn=%s' %(userSn)))
    if 'content' not in data:
        return

    for d in data['content']:
        t = d['TITLE'].encode('utf8')
        p = d['PARENT_SEQUENCE'].encode('utf8')
        l = 'http://vlog.xuite.net/%s?t=cat&p=%s&dir_num=0' %(user, p)
        addPage(req, l, t)
    return

def listURL_bilibili(req, url):
    if re.search(r'page=', url):
        meta.findPage(req, url)
        return
    txt = load(url)
    match = re.search(r'<select id=\'dedepagetitles\' .*?</select>', txt, re.DOTALL)
    if match:
        for m in re.finditer(r'<option value=\'([^\']*)\'>([^<]*)</option>', match.group(0)):
            addVideo(req, 'http://www.bilibili.com'+m.group(1), m.group(2))
    else:
        image = re.search(r'<img src="([^"]*)"', txt)
        if image:
            addVideo(req, url, url, image.group(1))
        else:
            addVideo(req, url, url)

def listURL_dramaq(req, url):
    if re.search(r'php', url):
        for m in re.finditer(r'(.*?)\n(.*?)<iframe (.*?)</iframe>', load(url)):
            src = re.search(r'src="([^"]*)"', m.group(3))
            pw = re.search(r':([^<]*)</font>', m.group(1))
            if src and pw:
                link = src.group(1)+'&ytdl_password='+re.split(' ', pw.group(1))[0]
                addEntry(req, 'view.py?V='+urllib.quote(link), src.group(1))
            elif src:
                addVideo(req, src.group(1))
        return

    if re.search(r'(biz|jp/|us/|cn/)$', url):
        meta.findPage(req, url)
        for m in re.finditer(r'<a class="mod-articles-category-title " href="([^"]*)">([^"]*)</a>', load(url)):
            if m.group(1)[-1] == '/':
                addPage(req, 'http://www.dramaq.biz'+m.group(1), m.group(2))
        return
    for m in re.finditer(r'<li class="item-751"><a href="([^.]*).php"', load(url)):
        if re.search(r'ep', m.group(1)):
            link = url+m.group(1)+'.php'
            title = m.group(1)
            addPage(req, link, title)

def listURL_dodova(req, url):
    for m in re.finditer(r'<div class="mh-excerpt">([^<]*)<a href="([^"]*)" title="([^"]*)">', load(url)):
        link = m.group(2)
        title = m.group(3)
        addPage(req, link, title, None)

def listURL_youtube(req, url):
    if re.search(r'playlists($)', url):
        playlist = None
        for m in re.finditer(r'href="/playlist\?list=([^"]*)"*?>([^<]*)</a>', load(url)):
            if playlist != m.group(1):
                playlist, title = m.group(1), m.group(2)
                addPlayList(req, playlist, title)
    elif re.search(r'playlist\?', url):
        for m in re.finditer(r'pl-video yt-uix-tile ([^>]*)', load(url)):
            vid = re.search(r'data-video-id="([^"]*)"', m.group())
            title = re.search(r'data-title="([^"]*)"', m.group())
            if vid and title:
                addYouTube(req, vid.group(1), title.group(1))
    else:
        for m in re.finditer(r'watch\?v=(.{11})">([^<]*)</a>', load(url)):
            vid = m.group(1)
            addYouTube(req, m.group(1), m.group(2))

def listURL_eslpod(req, url):
    txt = load(url)
    if re.search(r'/podcast/', url):
        m = re.search(r'/podcast/esl-podcast-([0-9]*)', url)
        if m:
            src = 'https://traffic.libsyn.com/secure/eslpod/ESLPod%s.mp3' %(m.group(1))
            req.write('<h1><a href="view.py?v=%s" target="_blank">Load Media</a></h1>\n' %(src))
            req.write('<h1><a href="%s" target="_blank">Download Media</a></h1>\n' %(src))
        m = re.search(r'<div id="home" class="tab-pane fade in active">(.*?)</div>', txt, re.DOTALL|re.MULTILINE)
        if m:
            req.write('<br><hr><font size=4>')
            req.write(m.group(1))
            req.write('</font><hr><br>')
            eslpod.parseWord(req, m.group(1))
    elif re.search(r'/library/', url):
        for m in re.finditer(r'<a href="([^"]*)">([^<]*)</a>', txt):
            link, title = m.group(1), m.group(2)
            if re.search(r'/podcast/', link):
                addPage(req, link, title)

def listURL_mangareader(req, url):
    for m in re.finditer(r'<a href="/one-piece/([^"]*)">([^"]*)</a>([^<]*)<', load(url)):
        link = 'http://www.mangareader.net/one-piece/'+m.group(1)
        title = m.group(2)+m.group(3)
        addPage(req, link, title)

def listURL_nbahd(req, url):
    for m in re.finditer(r'<h2 class="entry-title"><a href="([^"]*)"', load(url)):
        addVideo(req, m.group(1), m.group(1))

def listURL_jav(req, url):
    meta.findVideo(req, url)

def listURL_cute(req, url):
    if url.endswith('/'):
        meta.findLink(req, url)
    else:
        meta.findImageLink(req, url, True, True)

def listURL_porn2tube(req, url):
        meta.findImageLink(req, url, True, False)

def listURL_adult_dodova(req, url):
    if url.endswith('/'):
        meta.findLink(req, url)
    else:
        meta.findPage(req, url, True)

def listURL(req, url):

    html = re.split('<!--result-->', loadFile('list.html'))
    req.write(html[0])

    if url == 'mangareader':
        listURL_mangareader(req, 'http://www.mangareader.net/one-piece')

    elif url == 'nbahd':
        listURL_nbahd(req, 'http://nbahd.com/page/1/')
        listURL_nbahd(req, 'http://nbahd.com/page/2/')
        listURL_nbahd(req, 'http://nbahd.com/page/3/')

    elif re.search(r'bilibili', url):
        listURL_bilibili(req, url)

    elif re.search(r'dramaq', url):
        listURL_dramaq(req, url)

    elif re.search(r'youtube.com', url):
        listURL_youtube(req, url)

    elif re.search(r'eslpod.com', url):
        listURL_eslpod(req, url)

    elif re.search(r'xuite.net', url):
        if re.search(r'xuite.net/([a-zA-Z0-9]*)($)', url):
            listURL_xuiteDIR(req, url)
        else:
            listURL_xuite(req, url)

    elif re.search(r'mangareader.net', url):
        mangareader.loadImage(req, url)

    elif re.search(r'movie.dodova.com/category/', url):
        listURL_dodova(req, url+'/page/1')
        listURL_dodova(req, url+'/page/2')
        listURL_dodova(req, url+'/page/3')

    elif re.search('jav(68|pub)',url):
        listURL_jav(req, url)

    elif re.search('javcuteonline',url):
        listURL_cute(req, url)

    elif re.search('porn2tube',url):
        listURL_porn2tube(req, url)

    elif re.search(r'adult.dodova.com', url):
        listURL_adult_dodova(req, url)

    else:
        listURL_def(req, url)

    req.write(html[1])

