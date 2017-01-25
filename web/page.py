#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import urllib
import json
import mangareader
import esl
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
    req.write('<h1>Index of %s</h1>\n' %(d))
    req.write('<div style="line-height:200%;font-size:20">\n')
    for dirName, subdirList, fileList in os.walk(d):
        for subdir in sorted(subdirList):
            if subdir[0] != '.':
                req.write('<li><img src="/icons/folder.gif"> <a href="view.py?d=%s/%s">%s</a>\n' %(dirName, subdir, subdir))
        for fname in sorted(fileList):
            if fname.lower().endswith(('.mkv', '.mp4', '.avi', '.flv', '.rmvb', '.rm', '.f4v', '.wmv', '.m3u', '.m3u8', '.ts')):
                req.write('<li><img src="/icons/movie.gif"> <a href="view.py?f=%s/%s">%s</a>\n' %(dirName, fname, fname))
        break
    req.write('</div>\n')
    req.write(html[1])

def load(url):
    return meta.load(url)

def loadLocal(url):
    return meta.load('http://127.0.0.1/vod/'+url)

def addEntry(req, link, title, image=None):
    req.write('\n<a href="%s">\n' %(link))
    req.write('<h2>%s</h2>\n' %(title))
    if image:
        req.write('<img src="%s" class="img" />\n' %(image))
    req.write('</a>\n')

def addPage(req, link, title, image=None):
    addEntry(req, 'view.py?p='+link, title, image)

def addVideo(req, link, title=None, image=None):
    if re.search(r'^//', link):
        link = re.sub('//', 'http://', link)
    addEntry(req, 'view.py?v='+link, title or link, image or meta.getImage(link))

def addAudio(req, url):
    req.write('<hr>\n')
    req.write('<audio controls preload=none style="width:800px;"><source src="%s" type="audio/mpeg"></audio>\n' %(url))
    req.write('<hr>\n')

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

def search_dbEntry(req, url, title0, q):
    for m in re.finditer(r'<a href="([^"]*)">(.*?)</a>', loadLocal(url), re.DOTALL|re.MULTILINE):
        link = m.group(1)
        title = meta.search(r'<h2>(.*?)</h2>', m.group(2))
        image = meta.search(r'src="([^"]*)"', m.group(2)) or 'Movies-icon.png'
        if re.search(q, title, re.IGNORECASE):
            addEntry(req, link, title0+'/'+title, image)

def search_db(req, q):
    for m in re.finditer(r'<a href=([^>]*)>(.*?)</a>', loadLocal('bookmark.html')):
        search_dbEntry(req, m.group(1), m.group(2), q)

def search(req, q, s):
    html = re.split('<!--result-->', loadFile('list.html'))
    req.write(html[0])

    s = s or 'yt'

    q1 = re.sub(' ', '+', q)

    req.write('<img onload="loadImage()" onclick="startDictation()" src="mic-icon.png" id="ximage" class="topright" />\n')

    req.write('<h1>\n')
    req.write('<a href=view.py>Home</a>&nbsp;&nbsp;&nbsp;\n')
    req.write('<a href=view.py?s=yt&q='+q1+'>YouTube</a>&nbsp;&nbsp;&nbsp;\n')
    req.write('<a href=view.py?s=pl&q='+q1+'>PlayList</a>&nbsp;&nbsp;&nbsp;\n')
    req.write('<a href=view.py?s=dm&q='+q1+'>DailyMotion</a>&nbsp;&nbsp;&nbsp;\n')
    req.write('</h1>\n')

    req.write('<br>\n')

    req.write('<form action="view.py" method="get" id="xform">\n')
    req.write('<input type="text" name="q" value="%s" class="input" id="xinput"\>\n' %(q))
    req.write('<input type="hidden" name="s" value="%s" class="input"\>\n' %(s))
    req.write('</form>\n')

    req.write('<br>\n')

    search_db(req, q1)

    if s == 'yt':
        search_yt(req, q1)
    elif s == 'pl':
        search_pl(req, q1)
    elif s == 'dm':
        search_dm(req, q1)
    elif s == 'bi':
        search_bi(req, q1)

    req.write(html[1])

def listURL_def(req, url):
    meta.findLink(req, url)

def listURL_xuite(req, url):
    if re.search(r'xuite.net/([a-zA-Z0-9]*)($)', url):
        listURL_xuiteDIR(req, url)
    else:
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

def listURL_litv(req, url):
    m = re.search(r'(\?|&)id=([a-zA-Z0-9]*)', url)
    if m:
        _contentId = m.group(2)
        _url = 'https://www.litv.tv/vod/ajax/getProgramInfo?contentId='+_contentId
        headers = [('Accept', 'application/json, text/javascript, */*; q=0.01')]
        programInfo = meta.load(_url, None, headers)
        for m in re.finditer(r'{"contentId":"([^"]*)",.*?}', programInfo, re.DOTALL):
            contentId = m.group(1)
            imageLink = None
            subtitle = re.search(r'"subtitle":"([^"]*)"', m.group())
            imageFile = re.search(r'"imageFile":"([^"]*)"', m.group())
            if imageFile:
                imageLink = imageFile.group(1)
            if subtitle:
                addVideo(req, re.sub(_contentId, contentId, url), subtitle.group(1), imageLink)
    else:
        meta.findVideoLink(req, url, True, True, 'data-img')

def listURL_dramaq(req, url):
    if re.search(r'php', url):
        meta.findFrame(req, url)
    elif re.search(r'(biz|jp/|us/|cn/)$', url):
        meta.findPage(req, url)
        for m in re.finditer(r'<a class="mod-articles-category-title " href="([^"]*)">([^"]*)</a>', load(url)):
            if m.group(1)[-1] == '/':
                addPage(req, 'http://www.dramaq.biz'+m.group(1), m.group(2))
    else:
        for m in re.finditer(r'<li class="item-751"><a href="([^.]*).php"', load(url)):
            if re.search(r'ep', m.group(1)):
                link, title = url+m.group(1)+'.php', m.group(1)
                addPage(req, link, title)

def listURL_dodova(req, url):
    if re.search(r'imovie.dodova.com/category/', url):
        for i in range(1, 5):
            for m in re.finditer(r'<div class="mh-excerpt">([^<]*)<a href="([^"]*)" title="([^"]*)">', load(url+'/page/'+str(i))):
                link, title = m.group(2), m.group(3)
                addPage(req, link, title, None)
    elif re.search(r'imovie.dodova.com/', url):
        meta.findFrame(req, url)
        for m in re.finditer(r'<a href="([^"]*)" title="openload" target="_blank">', load(url)):
            meta.findLink(req, m.group(1).replace('&#038;', '&'))
    elif re.search(r'video.imovie.dodova.com/', url):
        meta.findLink(req, url)

def listURL_youtube(req, url):
    if re.search(r'/playlists($)', url):
        playlist = None
        for m in re.finditer(r'href="/playlist\?list=([^"]*)"*?>([^<]*)</a>', load(url)):
            if playlist != m.group(1):
                playlist, title = m.group(1), m.group(2)
                addPlayList(req, playlist, title)
    elif re.search(r'/channels($)', url):
        for m in re.finditer(r'class="yt-uix-sessionlink yt-uix-tile-link ([^>]*)', load(url)):
                link = re.search(r'href="([^"]*)"', m.group())
                title = re.search(r'title="([^"]*)"', m.group())
                if link and title:
                    addPage(req, 'https://www.youtube.com'+link.group(1), title.group(1))
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
        req.write('<h1><a href=%s>%s</a></h1>' %(url, url))
        m = re.search(r'podcast-([0-9]*)', url)
        if m:
            audio = 'https://traffic.libsyn.com/preview/secure/eslpod/DE%s.mp3' %(m.group(1))
            addAudio(req, audio)
        m = re.search(r'<div id="home" class="tab-pane fade in active">(.*?)</div>', txt, re.DOTALL|re.MULTILINE)
        if m:
            req.write('<font size=5><p>%s</p></font>' %(m.group(1)))
            esl.parseWord(req, m.group(1))
    elif re.search(r'/library/', url):
        for m in re.finditer(r'<a href="([^"]*)">([^<]*)</a>', txt):
            link, title = m.group(1), m.group(2)
            if re.search(r'/podcast/', link):
                addPage(req, link, title)

def listURL_dailyesl(req, url):
    txt = load(url)
    if url == 'http://www.dailyesl.com/':
        for m in re.finditer(r'<a href="(.*?)">(.*?)</a>', txt):
            addPage(req, 'http://www.dailyesl.com/'+m.group(1), m.group(2))
        return
    req.write('<h1><a href=%s>%s</a></h1>' %(url, url))
    for m in re.finditer(r'file: "([^"]*)"', txt):
        audio = 'http://www.dailyesl.com/'+m.group(1)
        addAudio(req, audio)
    for m in re.finditer(r'(</script>\n|</script>)</td></tr></table>(.*?)<p>', txt, re.DOTALL|re.MULTILINE):
        req.write('<font size=5><p>%s</p></font>' %(m.group(2)))
        esl.parseWord(req, m.group(2))

def listURL_mangareader(req):
    txt = load('http://www.mangareader.net/one-piece')
    for m in re.finditer(r'<a href="/one-piece/([^"]*)">([^"]*)</a>([^<]*)<', txt):
        link = 'http://www.mangareader.net/one-piece/'+m.group(1)
        title = m.group(2)+m.group(3)
        addPage(req, link, title)

def listURL_nbahd(req):
    for i in range(1, 3):
        for m in re.finditer(r'<h2 class="entry-title"><a href="([^"]*)"', load('http://nbahd.com/page/'+str(i))):
            addVideo(req, m.group(1), m.group(1))

def listURL(req, url):

    html = re.split('<!--result-->', loadFile('list.html'))
    req.write(html[0])

    if url == 'mangareader':
        listURL_mangareader(req)

    elif url == 'nbahd':
        listURL_nbahd(req)

    elif re.search(r'bilibili', url):
        listURL_bilibili(req, url)

    elif re.search(r'litv', url):
        listURL_litv(req, url);

    elif re.search(r'dramaq', url):
        listURL_dramaq(req, url)

    elif re.search(r'youtube', url):
        listURL_youtube(req, url)

    elif re.search(r'eslpod', url):
        listURL_eslpod(req, url)

    elif re.search(r'dailyesl', url):
        listURL_dailyesl(req, url)

    elif re.search(r'xuite', url):
        listURL_xuite(req, url)

    elif re.search(r'mangareader', url):
        mangareader.loadImage(req, url)

    elif re.search(r'imovie.dodova', url):
        listURL_dodova(req, url)

    elif re.search('(porn|jav)',url):
        meta.findImageLink(req, url, True, False)

    else:
        listURL_def(req, url)

    req.write(html[1])

